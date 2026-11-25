(function () {
  var doc = document.documentElement;
  requestAnimationFrame(function () { requestAnimationFrame(function () { doc.classList.add('loaded'); }); });

  var mb = document.querySelector('.menu-btn'), tabs = document.getElementById('tabs');
  if (mb) mb.addEventListener('click', function () { var o = tabs.classList.toggle('open'); mb.setAttribute('aria-expanded', o); });

  // staggered reveals per section
  document.querySelectorAll('section, footer, article, .mgroup').forEach(function (sec) {
    var i = 0; sec.querySelectorAll('[data-reveal]').forEach(function (k) { k.style.setProperty('--d', Math.min(i++, 8)); });
  });
  var els = document.querySelectorAll('[data-reveal]');
  if ('IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (es) { es.forEach(function (en) { if (en.isIntersecting) { en.target.classList.add('in'); io.unobserve(en.target); } }); }, { rootMargin: '0px 0px -6% 0px' });
    els.forEach(function (el) { io.observe(el); });
  } else els.forEach(function (el) { el.classList.add('in'); });

  // team: index with preview + dialog
  var prev = document.getElementById('t-preview');
  document.querySelectorAll('.t-row').forEach(function (row) {
    function show() {
      if (!prev || prev.getAttribute('src') === row.dataset.img) return;
      prev.classList.add('swap');
      setTimeout(function () { prev.src = row.dataset.img; prev.classList.remove('swap'); }, 120);
    }
    row.addEventListener('mouseenter', show); row.addEventListener('focus', show);
    row.addEventListener('click', function () { var d = document.getElementById(row.dataset.dialog); if (d && d.showModal) d.showModal(); });
  });
  document.querySelectorAll('.t-dialog').forEach(function (d) {
    d.addEventListener('click', function (ev) { if (ev.target === d) d.close(); });
  });

  // services index: mark the section in view
  var links = document.querySelectorAll('.index a');
  if (links.length && 'IntersectionObserver' in window) {
    var map = {}; links.forEach(function (a) { map[a.getAttribute('href').slice(1)] = a; });
    var so = new IntersectionObserver(function (es) {
      es.forEach(function (en) { if (en.isIntersecting) { links.forEach(function (a) { a.classList.remove('on'); }); var a = map[en.target.id]; if (a) a.classList.add('on'); } });
    }, { rootMargin: '-30% 0px -60% 0px' });
    document.querySelectorAll('.svc').forEach(function (s) { so.observe(s); });
  }

  // coupon: compose an e-mail
  document.querySelectorAll('form.coupon').forEach(function (f) {
    f.addEventListener('submit', function (ev) {
      ev.preventDefault();
      var v = function (n) { return (f.elements[n] && f.elements[n].value || '').trim(); };
      var body = v('message') + '\n\n' + v('name') + (v('phone') ? '\n' + v('phone') : '') + (v('email') ? '\n' + v('email') : '');
      location.href = 'mailto:' + f.dataset.mailto + '?subject=' + encodeURIComponent(v('name') ? 'Anfrage / Request – ' + v('name') : 'Anfrage / Request') + '&body=' + encodeURIComponent(body);
    });
  });
})();
