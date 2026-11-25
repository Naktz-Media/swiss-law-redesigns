(function () {
  var doc = document.documentElement;
  requestAnimationFrame(function () { requestAnimationFrame(function () { doc.classList.add('loaded'); }); });

  // keep ?id= / ?canton= when switching language
  if (location.search) {
    document.querySelectorAll('[data-keepquery]').forEach(function (a) { a.href = a.getAttribute('href').split('?')[0] + location.search; });
  }

  // menu
  var mb = document.querySelector('.menu-btn'), menu = document.getElementById('menu');
  if (mb) mb.addEventListener('click', function () {
    var open = menu.classList.toggle('open'); mb.setAttribute('aria-expanded', open);
  });

  // reveal on scroll, staggered per section
  var els = document.querySelectorAll('[data-reveal]');
  document.querySelectorAll('section, footer, figure').forEach(function (sec) {
    var kids = sec.querySelectorAll(':scope [data-reveal]'); var i = 0;
    kids.forEach(function (k) { if (!k.style.getPropertyValue('--d')) k.style.setProperty('--d', Math.min(i++, 10)); });
  });
  if ('IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (en) { if (en.isIntersecting) { en.target.classList.add('in'); io.unobserve(en.target); } });
    }, { rootMargin: '0px 0px -8% 0px' });
    els.forEach(function (el) { io.observe(el); });
  } else els.forEach(function (el) { el.classList.add('in'); });

  // fit the giant hero word to the width
  var big = document.querySelector('.home .hero-big');
  function fit() {
    if (!big) return;
    if (window.innerWidth <= 640) { big.style.removeProperty('--big'); big.style.fontSize = ''; return; }
    big.style.fontSize = '100px';
    var w = big.firstElementChild.getBoundingClientRect().width;
    var avail = big.parentElement.getBoundingClientRect().width;
    var size = Math.min(100 * avail / w * 0.99, window.innerHeight * 0.42);
    big.style.fontSize = size + 'px';
  }
  if (big) { fit(); document.fonts && document.fonts.ready.then(fit); window.addEventListener('resize', fit); }

  // home quick search: button label follows the chosen canton
  var q = document.querySelector('.quick');
  if (q) {
    var sel = q.querySelector('select'), btn = q.querySelector('button');
    var counts = {};
    sel.querySelectorAll('option').forEach(function (o) { var m = o.textContent.match(/\((\d+)\)$/); if (m) counts[o.value] = +m[1]; });
    sel.addEventListener('change', function () {
      var v = sel.value;
      if (!v) btn.textContent = btn.dataset.labelAll.replace('{n}', btn.dataset.total);
      else btn.textContent = btn.dataset.labelC.replace('{n}', counts[v] || 0).replace('{c}', sel.options[sel.selectedIndex].textContent.replace(/\s*\(\d+\)$/, ''));
    });
  }

  // directory
  var list = document.getElementById('list');
  if (list && window.LAWYERS) {
    var form = document.getElementById('filters'), count = document.getElementById('count'), empty = document.getElementById('empty');
    var norm = function (s) { return (s || '').toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g, ''); };
    var params = new URLSearchParams(location.search);
    ['lastname', 'firstname', 'canton', 'gender'].forEach(function (k) { if (params.get(k)) form.elements[k].value = params.get(k); });
    if (params.get('result_type') === 'rand') form.querySelector('[value="rand"]').checked = true;
    function initials(n) { return n.split(/\s+/).slice(0, 2).map(function (w) { return w[0]; }).join(''); }
    function esc(s) { var d = document.createElement('div'); d.textContent = s || ''; return d.innerHTML; }
    function render() {
      var last = norm(form.elements.lastname.value), first = norm(form.elements.firstname.value);
      var c = form.elements.canton.value, g = form.elements.gender.value;
      var mode = form.querySelector('[name="result_type"]:checked').value;
      var res = LAWYERS.filter(function (x) {
        var parts = norm(x.n).split(/\s+/);
        if (last && !parts.some(function (p, i) { return i < 2 && p.indexOf(last) === 0; }) && norm(x.n).indexOf(last) !== 0) return false;
        if (first && !parts.slice(1).some(function (p) { return p.indexOf(first) === 0; })) return false;
        if (c && x.c !== c) return false;
        if (g && x.g !== g) return false;
        return true;
      });
      if (mode === 'rand') { res = res.slice().sort(function () { return Math.random() - .5; }).slice(0, 8); }
      count.textContent = res.length === 1 ? count.dataset.one : count.dataset.many.replace('{n}', res.length);
      empty.hidden = res.length > 0;
      list.innerHTML = res.map(function (x, i) {
        var face = x.i ? '<img class="face" src="../img/lawyers/' + x.i + '" alt="" width="56" height="56" loading="lazy">' : '<span class="face none" aria-hidden="true">' + esc(initials(x.n)) + '</span>';
        return '<li style="--i:' + Math.min(i, 30) + '"><a href="' + PROFILE + '?id=' + x.id + '">' + face +
          '<span class="who"><b>' + esc(x.n) + '</b><span>' + esc(x.f) + '</span></span>' +
          '<span class="where"><b>' + esc(x.a.replace(/^\d{4}\s*/, '')) + '</b>' + esc(x.c) + '</span></a></li>';
      }).join('');
      var q = new URLSearchParams();
      ['lastname', 'firstname', 'canton', 'gender'].forEach(function (k) { if (form.elements[k].value) q.set(k, form.elements[k].value); });
      if (mode === 'rand') q.set('result_type', 'rand');
      history.replaceState(null, '', location.pathname + (q.toString() ? '?' + q : ''));
      document.querySelectorAll('[data-keepquery]').forEach(function (a) { a.href = a.getAttribute('href').split('?')[0] + location.search; });
    }
    form.addEventListener('input', render);
    form.addEventListener('change', render);
    form.addEventListener('submit', function (ev) { ev.preventDefault(); render(); list.scrollIntoView({ behavior: 'smooth', block: 'start' }); });
    form.addEventListener('reset', function () { setTimeout(render, 0); });
    render();
  }

  // profile
  var prof = document.getElementById('profile');
  if (prof && window.PEOPLE) {
    var id = new URLSearchParams(location.search).get('id'), x = PEOPLE[id], lab = JSON.parse(prof.dataset.labels);
    function e2(s) { var d = document.createElement('div'); d.textContent = s || ''; return d.innerHTML; }
    if (!x) { prof.querySelector('h1').insertAdjacentHTML('afterend', '<p class="p-body">' + e2(lab.notfound) + '</p>'); return; }
    document.title = x.name + ' · ' + document.title;
    var photo = x.img ? '<img class="p-photo" src="../img/lawyers/' + x.img + '" alt="' + e2(x.name) + '" width="440" height="550">'
      : '<div class="p-mono" aria-hidden="true">' + e2(x.name.split(/\s+/).slice(0, 2).map(function (w) { return w[0]; }).join('')) + '</div>';
    var dl = '';
    dl += '<dt>' + e2(lab.addr) + '</dt><dd>' + e2(x.firm) + '<br>' + x.addr.map(e2).join('<br>') + '</dd>';
    dl += '<dt>' + e2(lab.canton_title) + '</dt><dd>' + e2(CANTONS[x.canton] || x.canton) + '</dd>';
    if (x.phone) dl += '<dt>' + e2(lab.phone) + '</dt><dd><a href="tel:' + x.phone.replace(/[^\d+]/g, '') + '">' + e2(x.phone) + '</a></dd>';
    if (x.fax) dl += '<dt>' + e2(lab.fax) + '</dt><dd>' + e2(x.fax) + '</dd>';
    if (x.email) dl += '<dt>' + e2(lab.email) + '</dt><dd><a href="mailto:' + e2(x.email) + '">' + e2(x.email) + '</a></dd>';
    if (x.web) dl += '<dt>' + e2(lab.web) + '</dt><dd><a href="' + e2(x.web) + '" rel="noopener">' + e2(x.web.replace(/^https?:\/\//, '').replace(/\/$/, '')) + '</a></dd>';
    prof.innerHTML = '<h1 class="phead-h">' + e2(x.name) + '</h1>' + '<div>' + photo + '</div>' +
      '<div class="p-body">' + (x.title ? '<p class="p-title">' + e2(x.title) + '</p>' : '') +
      '<p class="p-firm">' + e2(x.firm) + '</p><dl class="p-dl">' + dl + '</dl>' +
      '<p><a class="btn btn-ink" href="' + LIST + '">' + e2(lab.back) + '</a></p></div>';
  }
})();
