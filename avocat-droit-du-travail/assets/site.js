(function () {
  var doc = document.documentElement;
  requestAnimationFrame(function () { requestAnimationFrame(function () { doc.classList.add('loaded'); }); });
  var ARR = window.ARR || '';

  // keep ?id= / ?canton= when switching language
  if (location.search) {
    document.querySelectorAll('[data-keepquery]').forEach(function (a) { a.href = a.getAttribute('href').split('?')[0] + location.search; });
  }

  // menu
  var mb = document.querySelector('.menu-btn');
  if (mb) mb.addEventListener('click', function () {
    var open = document.body.classList.toggle('menu-open'); mb.setAttribute('aria-expanded', open);
  });

  // reveal on scroll, staggered per section
  document.querySelectorAll('section, footer, .bento, .cards').forEach(function (sec) {
    var i = 0; sec.querySelectorAll('[data-reveal]').forEach(function (k) { k.style.setProperty('--d', Math.min(i++, 8)); });
  });
  var els = document.querySelectorAll('[data-reveal]');
  if ('IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (en) { if (en.isIntersecting) { en.target.classList.add('in'); io.unobserve(en.target); } });
    }, { rootMargin: '0px 0px -6% 0px' });
    els.forEach(function (el) { io.observe(el); });
  } else els.forEach(function (el) { el.classList.add('in'); });

  // people rail
  var rail = document.getElementById('rail');
  document.querySelectorAll('[data-rail]').forEach(function (b) {
    b.addEventListener('click', function () { rail.scrollBy({ left: +b.dataset.rail * rail.clientWidth * 0.8, behavior: 'smooth' }); });
  });

  // home quick search: button label follows the chosen canton
  var q = document.querySelector('.quick');
  if (q) {
    var sel = q.querySelector('select'), btn = q.querySelector('button'), lab = btn.querySelector('.t');
    var counts = {};
    sel.querySelectorAll('option').forEach(function (o) { var m = o.textContent.match(/\((\d+)\)$/); if (m) counts[o.value] = +m[1]; });
    sel.addEventListener('change', function () {
      var v = sel.value;
      lab.textContent = !v ? btn.dataset.labelAll.replace('{n}', btn.dataset.total)
        : btn.dataset.labelC.replace('{n}', counts[v] || 0).replace('{c}', sel.options[sel.selectedIndex].textContent.replace(/\s*\(\d+\)$/, ''));
    });
  }

  function esc(s) { var d = document.createElement('div'); d.textContent = s || ''; return d.innerHTML; }
  function initials(n) { return n.split(/\s+/).slice(0, 2).map(function (w) { return w[0]; }).join(''); }

  // directory
  var list = document.getElementById('list');
  if (list && window.LAWYERS) {
    var form = document.getElementById('filters'), count = document.getElementById('count'), empty = document.getElementById('empty');
    var norm = function (s) { return (s || '').toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g, ''); };
    var params = new URLSearchParams(location.search);
    ['lastname', 'firstname', 'canton', 'gender'].forEach(function (k) { if (params.get(k)) form.elements[k].value = params.get(k); });
    if (params.get('result_type') === 'rand') form.querySelector('[value="rand"]').checked = true;
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
        var face = x.i ? '<img class="face" src="../img/lawyers/' + x.i + '" alt="" width="64" height="64" loading="lazy">' : '<span class="face none" aria-hidden="true">' + esc(initials(x.n)) + '</span>';
        return '<li style="--i:' + Math.min(i, 30) + '"><a class="lrow" href="' + PROFILE + '?id=' + x.id + '">' + face +
          '<span class="who"><b>' + esc(x.n) + '</b><span>' + esc(x.f) + '</span></span>' +
          '<span class="where"><b>' + esc(x.a.replace(/^\d{4}\s*/, '')) + '</b><span>' + esc(CANTONS[x.c] || x.c) + '</span></span><span class="circ">' + ARR + '</span></a></li>';
      }).join('');
      var qs = new URLSearchParams();
      ['lastname', 'firstname', 'canton', 'gender'].forEach(function (k) { if (form.elements[k].value) qs.set(k, form.elements[k].value); });
      if (mode === 'rand') qs.set('result_type', 'rand');
      history.replaceState(null, '', location.pathname + (qs.toString() ? '?' + qs : ''));
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
    if (!x) { prof.querySelector('h1').insertAdjacentHTML('afterend', '<p class="lead">' + esc(lab.notfound) + '</p>'); return; }
    document.title = x.name + ' · ' + document.title;
    var photo = x.img ? '<img class="p-photo" src="../img/lawyers/' + x.img + '" alt="' + esc(x.name) + '" width="440" height="550">'
      : '<div class="p-mono" aria-hidden="true">' + esc(initials(x.name)) + '</div>';
    function item(t, d) { return '<div><dt>' + esc(t) + '</dt><dd>' + d + '</dd></div>'; }
    var dl = item(lab.addr, esc(x.firm) + '<br>' + x.addr.map(esc).join('<br>'));
    dl += item(lab.canton_title, esc(CANTONS[x.canton] || x.canton));
    if (x.phone) dl += item(lab.phone, '<a href="tel:' + x.phone.replace(/[^\d+]/g, '') + '">' + esc(x.phone) + '</a>');
    if (x.fax) dl += item(lab.fax, esc(x.fax));
    if (x.email) dl += item(lab.email, '<a href="mailto:' + esc(x.email) + '">' + esc(x.email) + '</a>');
    if (x.web) dl += item(lab.web, '<a href="' + esc(x.web) + '" rel="noopener">' + esc(x.web.replace(/^https?:\/\//, '').replace(/\/$/, '')) + '</a>');
    prof.innerHTML = '<div>' + photo + '</div>' +
      '<div class="p-body"><h1 class="h-l">' + esc(x.name) + '</h1>' + (x.title ? '<p class="p-title">' + esc(x.title) + '</p>' : '') +
      '<p class="p-firm">' + esc(x.firm) + '</p><dl class="p-dl">' + dl + '</dl>' +
      '<p><a class="btn" href="' + LIST + '">' + esc(lab.back) + '<span class="arr">' + ARR + '</span></a></p></div>';
  }
})();
