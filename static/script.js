// PhishGuard site JS
(function () {
  // Day / night mode
  var toggle = document.getElementById('themeToggle');
  function currentTheme() {
    return document.documentElement.getAttribute('data-theme') || 'light';
  }
  if (toggle) {
    toggle.addEventListener('click', function () {
      var next = currentTheme() === 'dark' ? 'light' : 'dark';
      document.documentElement.setAttribute('data-theme', next);
      try { localStorage.setItem('pg-theme', next); } catch (e) {}
    });
  }

  // Mobile menu
  var burger = document.getElementById('hamburger');
  var menu = document.getElementById('mobileMenu');
  if (burger && menu) {
    burger.addEventListener('click', function () {
      var open = menu.classList.toggle('open');
      burger.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
    menu.querySelectorAll('a').forEach(function (a) {
      a.addEventListener('click', function () { menu.classList.remove('open'); });
    });
  }

  // Navbar shadow on scroll
  var nav = document.getElementById('navbar');
  window.addEventListener('scroll', function () {
    if (!nav) return;
    nav.style.boxShadow = window.scrollY > 10 ? '0 10px 30px rgba(0,0,0,.4)' : 'none';
  }, { passive: true });

  // Scanner: char count + samples + loading
  var ta = document.getElementById('smsInput');
  var cc = document.getElementById('charCount');
  function updateCount() { if (ta && cc) cc.textContent = ta.value.length; }
  if (ta) { ta.addEventListener('input', updateCount); updateCount(); }

  window.fillSample = function (k) {
    var samples = {
      safe: 'Hey, are we still meeting for lunch tomorrow at 1pm?',
      phish: "URGENT! You've WON a FREE iPhone. Click http://bit.ly/claim123 to verify your account now!"
    };
    if (ta) { ta.value = samples[k] || ''; updateCount(); ta.focus(); }
  };

  var form = document.getElementById('scanForm');
  if (form) {
    form.addEventListener('submit', function () {
      var btn = document.getElementById('scanBtn');
      var sp = document.getElementById('spinner');
      var ic = document.getElementById('scanIcon');
      var tx = document.getElementById('btnText');
      if (sp) sp.style.display = 'block';
      if (ic) ic.style.display = 'none';
      if (tx) tx.textContent = 'Scanning...';
      if (btn) btn.disabled = true;
    });
  }

  // Scroll reveal
  var els = document.querySelectorAll('.reveal');
  if ('IntersectionObserver' in window && els.length) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (e.isIntersecting) { e.target.classList.add('visible'); io.unobserve(e.target); }
      });
    }, { threshold: 0.12 });
    els.forEach(function (el) { io.observe(el); });
  } else {
    els.forEach(function (el) { el.classList.add('visible'); });
  }
})();
