(function () {
  var doc = document.documentElement;
  requestAnimationFrame(function () { requestAnimationFrame(function () { doc.classList.add('loaded'); }); });

  var sc = function () { doc.classList.toggle('scrolled', window.scrollY > 40); };
  window.addEventListener('scroll', sc, { passive: true }); sc();

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

  // explore: the hovered or focused page shows its photo
  var ex = document.querySelectorAll('.ex-list a');
  ex.forEach(function (a) {
    var go = function () {
      var i = a.dataset.ex;
      ex.forEach(function (b) { b.classList.toggle('on', b === a); });
      document.querySelectorAll('.ex-media img').forEach(function (m) { m.classList.toggle('on', m.dataset.ex === i); });
    };
    a.addEventListener('mouseenter', go); a.addEventListener('focus', go);
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

  // services on phones: each area opens in full on demand
  document.querySelectorAll('.svc-more').forEach(function (b) {
    var lbl = b.textContent, svc = b.closest('.svc');
    var set = function (o) { svc.classList.toggle('open', o); b.setAttribute('aria-expanded', o); b.textContent = o ? b.dataset.less : lbl; };
    b.addEventListener('click', function () {
      var o = !svc.classList.contains('open'); set(o);
      if (!o && svc.getBoundingClientRect().top < 0) svc.scrollIntoView({ block: 'start' });
    });
    svc._open = set;
    var fit = function () { var bd = svc.querySelector('.svc-b'); b.hidden = !svc.classList.contains('open') && bd.scrollHeight <= bd.clientHeight + 24; if (b.hidden) bd.style.maskImage = bd.style.webkitMaskImage = 'none'; else bd.style.maskImage = bd.style.webkitMaskImage = ''; };
    fit(); window.addEventListener('resize', fit);
  });
  var openHash = function () { var t = location.hash && document.getElementById(location.hash.slice(1)); if (t && t._open) t._open(true); };
  window.addEventListener('hashchange', openHash); openHash();

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
