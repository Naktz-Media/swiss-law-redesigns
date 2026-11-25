(function () {
  var doc = document.documentElement;
  requestAnimationFrame(function () { requestAnimationFrame(function () { doc.classList.add('loaded'); }); });

  var mb = document.querySelector('.menu-btn');
  if (mb) mb.addEventListener('click', function () { var o = document.body.classList.toggle('menu-open'); mb.setAttribute('aria-expanded', o); });

  // staggered reveals per section
  document.querySelectorAll('section, footer, .bento, .cards, .team-grid').forEach(function (sec) {
    var i = 0; sec.querySelectorAll('[data-reveal]').forEach(function (k) { k.style.setProperty('--d', Math.min(i++, 8)); });
  });
  var els = document.querySelectorAll('[data-reveal]');
  if ('IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (es) { es.forEach(function (en) { if (en.isIntersecting) { en.target.classList.add('in'); io.unobserve(en.target); } }); }, { rootMargin: '0px 0px -6% 0px' });
    els.forEach(function (el) { io.observe(el); });
  } else els.forEach(function (el) { el.classList.add('in'); });

  // people rail
  var rail = document.getElementById('rail');
  document.querySelectorAll('[data-rail]').forEach(function (b) {
    b.addEventListener('click', function () { rail.scrollBy({ left: +b.dataset.rail * rail.clientWidth * 0.8, behavior: 'smooth' }); });
  });

  // team dialogs: open from a card, or from #m3 in the address
  function openDialog(id) { var d = document.getElementById(id); if (d && d.showModal) { d.showModal(); return true; } return false; }
  document.querySelectorAll('[data-open]').forEach(function (b) {
    b.addEventListener('click', function (ev) { if (openDialog(b.dataset.open)) ev.preventDefault(); });
  });
  document.querySelectorAll('.t-dialog').forEach(function (d) {
    d.addEventListener('click', function (ev) { if (ev.target === d) d.close(); });
  });
  if (/^#m\d+$/.test(location.hash)) openDialog(location.hash.slice(1));

  // services index: mark the section in view
  var links = document.querySelectorAll('.index a');
  if (links.length && 'IntersectionObserver' in window) {
    var map = {}; links.forEach(function (a) { map[a.getAttribute('href').slice(1)] = a; });
    var so = new IntersectionObserver(function (es) {
      es.forEach(function (en) { if (en.isIntersecting) { links.forEach(function (a) { a.classList.remove('on'); }); var a = map[en.target.id]; if (a) a.classList.add('on'); } });
    }, { rootMargin: '-30% 0px -60% 0px' });
    document.querySelectorAll('.svc').forEach(function (s) { so.observe(s); });
  }

  // contact form: compose an e-mail
  document.querySelectorAll('form.coupon').forEach(function (f) {
    f.addEventListener('submit', function (ev) {
      ev.preventDefault();
      var v = function (n) { return (f.elements[n] && f.elements[n].value || '').trim(); };
      var body = v('message') + '\n\n' + v('name') + (v('phone') ? '\n' + v('phone') : '') + (v('email') ? '\n' + v('email') : '');
      location.href = 'mailto:' + f.dataset.mailto + '?subject=' + encodeURIComponent(v('name') ? 'Anfrage / Request – ' + v('name') : 'Anfrage / Request') + '&body=' + encodeURIComponent(body);
    });
  });
})();
