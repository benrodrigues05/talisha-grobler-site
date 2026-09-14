/* ═══════════════════════════════════════════════════════════
   Talisha Grobler — media kit
   No dependencies. No build step.
   ═══════════════════════════════════════════════════════════ */
(function () {
  'use strict';

  /* ── Footer year ─────────────────────────────────────── */
  var yearEl = document.getElementById('year');
  if (yearEl) yearEl.textContent = new Date().getFullYear();

  /* ── Header shadow once you scroll ───────────────────── */
  var header = document.querySelector('.site-header');
  var onScroll = function () {
    header.classList.toggle('is-stuck', window.scrollY > 8);
  };
  onScroll();
  window.addEventListener('scroll', onScroll, { passive: true });

  /* ── Mobile nav ──────────────────────────────────────── */
  var toggle = document.getElementById('navToggle');
  var nav = document.getElementById('nav');

  var closeNav = function () {
    nav.classList.remove('is-open');
    toggle.setAttribute('aria-expanded', 'false');
  };

  toggle.addEventListener('click', function () {
    var open = nav.classList.toggle('is-open');
    toggle.setAttribute('aria-expanded', String(open));
  });

  nav.addEventListener('click', function (e) {
    if (e.target.tagName === 'A') closeNav();
  });

  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape') closeNav();
  });

  window.addEventListener('resize', function () {
    if (window.innerWidth >= 900) closeNav();
  });

  /* ═══════════════════════════════════════════════════════
     BRAND MARQUEE
     The markup holds ONE row of brands. Clone it until the track is at
     least twice the viewport width, then translate by half — that way a
     wide monitor never catches an empty gap at the loop point, and the
     row stays a single list to maintain.
     ═══════════════════════════════════════════════════════ */
  var marquee = document.querySelector('.marquee');

  if (marquee && !window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
    var track = marquee.querySelector('.marquee-track');
    var sourceRow = track.querySelector('.marquee-row');

    var buildLoop = function () {
      // Measure BEFORE tearing anything down. If the row can't be measured
      // right now — hidden, not laid out yet — leave the marquee exactly as
      // it is and try again later. Removing .is-looping first would kill the
      // animation permanently on any rebuild that came back with zero width.
      var rowWidth = sourceRow.getBoundingClientRect().width;
      if (!rowWidth) return;

      track.classList.remove('is-looping');

      // Back to a single row, so repeated rebuilds can't compound the clones.
      while (track.children.length > 1) track.removeChild(track.lastChild);

      // Even number of copies, enough that half the track still fills the screen.
      var copies = Math.ceil((window.innerWidth * 2) / rowWidth);
      if (copies < 2) copies = 2;
      if (copies % 2) copies++;

      for (var i = 1; i < copies; i++) {
        var clone = sourceRow.cloneNode(true);
        clone.setAttribute('aria-hidden', 'true'); // screen readers read the list once
        track.appendChild(clone);
      }

      // --marquee-speed is the time for ONE row to pass. Scale the duration
      // by how many rows a half-track holds so the speed never changes.
      var perRow = parseFloat(
        getComputedStyle(document.documentElement).getPropertyValue('--marquee-speed')
      ) || 42;
      track.style.animationDuration = (perRow * (copies / 2)) + 's';

      track.classList.add('is-looping');
    };

    buildLoop();

    // Webfonts land after first paint and change the row width, so measure again.
    if (document.fonts && document.fonts.ready) document.fonts.ready.then(buildLoop);

    var marqueeTimer;
    window.addEventListener('resize', function () {
      clearTimeout(marqueeTimer);
      marqueeTimer = setTimeout(buildLoop, 250);
    });
  }

  /* ═══════════════════════════════════════════════════════
     MOTION
     The .js-motion class is what unlocks every "starts hidden" rule in
     styles.css. Setting it here, rather than in the markup, means the
     page can only ever be left mid-animation if this script is actually
     running. No JS, or a throw before this line, and everything renders
     static and complete.
     ═══════════════════════════════════════════════════════ */
  var reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var finePointer = window.matchMedia('(hover: hover) and (pointer: fine)').matches;

  document.documentElement.classList.add('js-motion');

  /* One rAF loop for everything scroll-linked, so we never lay out twice
     in a frame or stack listeners. */
  var scrollJobs = [];
  var ticking = false;

  var runScrollJobs = function () {
    var y = window.pageYOffset || document.documentElement.scrollTop;
    for (var i = 0; i < scrollJobs.length; i++) scrollJobs[i](y);
    ticking = false;
  };

  window.addEventListener('scroll', function () {
    if (!ticking) {
      ticking = true;
      window.requestAnimationFrame(runScrollJobs);
    }
  }, { passive: true });

  /* ── Scroll progress ────────────────────────────────── */
  var bar = document.createElement('div');
  bar.className = 'scroll-progress';
  header.appendChild(bar);

  scrollJobs.push(function (y) {
    var max = document.documentElement.scrollHeight - window.innerHeight;
    bar.style.setProperty('--p', max > 0 ? Math.min(y / max, 1).toFixed(4) : 0);
  });

  /* ── Hero parallax ──────────────────────────────────── */
  var heroImg = document.querySelector('.hero-img');
  if (heroImg && !reduced) {
    scrollJobs.push(function (y) {
      // Only while the hero is still on screen, and capped so the photo
      // can never drift out of its own rounded frame.
      if (y > window.innerHeight) return;
      var shift = Math.min(y * 0.075, 26);
      heroImg.style.transform = 'translate3d(0,' + shift.toFixed(2) + 'px,0)';
    });
  }

  /* ── Reveal on scroll ───────────────────────────────── */
  var revealTargets = document.querySelectorAll(
    '.section-head, .stat, .about-grid > *, .small-brands, .video-card, ' +
    '.shop-band, .contact-copy, .form-card, .hero-copy, .hero-photo, ' +
    '.chart-card, .analytics-cta, .phone'
  );

  if ('IntersectionObserver' in window && !reduced) {
    Array.prototype.forEach.call(revealTargets, function (el, i) {
      el.classList.add('reveal');
      // Stagger inside a row, capped so a long grid never visibly lags.
      el.style.transitionDelay = Math.min(i % 6, 5) * 60 + 'ms';
    });

    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add('is-in');
          io.unobserve(entry.target);
        }
      });
    }, { rootMargin: '0px 0px -8% 0px', threshold: 0.08 });

    Array.prototype.forEach.call(revealTargets, function (el) { io.observe(el); });

    /* Second, independent path to the same result. An element that has
       scrolled into view gets revealed whether or not the observer fired.
       Without this, anything the observer misses stays at opacity 0 for
       good, which is the worst possible failure: invisible content. */
    var revealInView = function () {
      var vh = window.innerHeight;
      for (var i = 0; i < revealTargets.length; i++) {
        var el = revealTargets[i];
        if (el.classList.contains('is-in')) continue;
        if (el.getBoundingClientRect().top < vh * 0.92) el.classList.add('is-in');
      }
    };
    scrollJobs.push(revealInView);
    window.setTimeout(revealInView, 3000);
  }

  /* ── Counters ───────────────────────────────────────── */
  /* Ticks the number up once, the first time a tile is seen. The unit
     (K, M, %) lives in its own span, so only the leading text node is
     touched and the decimal places are preserved. */
  var countUp = function (el) {
    var node = el.firstChild;
    if (!node || node.nodeType !== 3) return;
    var raw = node.nodeValue.trim();
    var target = parseFloat(raw.replace(/,/g, ''));
    if (!isFinite(target)) return;

    var dp = (raw.split('.')[1] || '').length;
    var grouped = raw.indexOf(',') !== -1;
    var start = null;
    var DUR = 1100;

    var frame = function (ts) {
      if (start === null) start = ts;
      var t = Math.min((ts - start) / DUR, 1);
      var eased = 1 - Math.pow(1 - t, 4);          // easeOutQuart
      var val = (target * eased).toFixed(dp);
      node.nodeValue = grouped
        ? Number(val).toLocaleString('en-GB', { minimumFractionDigits: dp })
        : val;
      if (t < 1) window.requestAnimationFrame(frame);
      else node.nodeValue = raw;                    // land exactly on the real value
    };
    window.requestAnimationFrame(frame);
  };

  if ('IntersectionObserver' in window && !reduced) {
    var counters = document.querySelectorAll('.stat-value');
    var cio = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          countUp(entry.target);
          cio.unobserve(entry.target);
        }
      });
    }, { threshold: 0.6 });
    Array.prototype.forEach.call(counters, function (el) { cio.observe(el); });
  }

  /* ── Charts draw in ─────────────────────────────────── */
  var charts = document.querySelectorAll('.chart-card');
  if ('IntersectionObserver' in window && charts.length) {
    var chio = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add('is-drawn');
          chio.unobserve(entry.target);
        }
      });
    }, { threshold: 0.25 });
    Array.prototype.forEach.call(charts, function (el) { chio.observe(el); });

    // Safety net: if the observer never fires for any reason, the charts
    // must not sit empty. Draw anything still undrawn after 2.5s.
    window.setTimeout(function () {
      Array.prototype.forEach.call(charts, function (el) {
        el.classList.add('is-drawn');
      });
    }, 2500);
  }

  /* ── Buttons lean toward the cursor ─────────────────── */
  if (finePointer && !reduced) {
    Array.prototype.forEach.call(
      document.querySelectorAll('.btn-accent, .btn-dark'),
      function (btn) {
        btn.addEventListener('mousemove', function (e) {
          var r = btn.getBoundingClientRect();
          var dx = (e.clientX - (r.left + r.width / 2)) / r.width;
          var dy = (e.clientY - (r.top + r.height / 2)) / r.height;
          btn.style.transform = 'translate(' + (dx * 7).toFixed(1) + 'px,'
                              + (dy * 5).toFixed(1) + 'px)';
        });
        btn.addEventListener('mouseleave', function () {
          btn.style.transform = '';
        });
      }
    );
  }

  /* ── Glow inside the analytics bubbles ──────────────── */
  /* Deliberately contained: it lives inside each card and is clipped by
     it, rather than roaming the whole page. Scoped to the Numbers section,
     so the effect stays where the data is. */
  if (finePointer && !reduced) {
    var lit = document.querySelectorAll('#stats .stat, #stats .chart-card');
    Array.prototype.forEach.call(lit, function (card) {
      card.classList.add('spot');
      card.addEventListener('mousemove', function (e) {
        var r = card.getBoundingClientRect();
        card.style.setProperty('--mx', (e.clientX - r.left) + 'px');
        card.style.setProperty('--my', (e.clientY - r.top) + 'px');
      });
      card.addEventListener('mouseenter', function () { card.classList.add('is-lit'); });
      card.addEventListener('mouseleave', function () { card.classList.remove('is-lit'); });
    });
  }

  /* ── Nav follows the section you're reading ─────────── */
  var navLinks = Array.prototype.slice.call(nav.querySelectorAll('a[href^="#"]'))
    .filter(function (a) { return !a.classList.contains('nav-cta'); });
  var sections = navLinks
    .map(function (a) { return document.querySelector(a.getAttribute('href')); })
    .filter(Boolean);

  if (sections.length) {
    scrollJobs.push(function (y) {
      var line = y + window.innerHeight * 0.32;
      var current = -1;
      for (var i = 0; i < sections.length; i++) {
        if (sections[i].offsetTop <= line) current = i;
      }
      for (var j = 0; j < navLinks.length; j++) {
        navLinks[j].classList.toggle('is-current', j === current);
      }
    });
  }

  /* ═══════════════════════════════════════════════════════
     INQUIRY FORM
     Validation → Formspree POST → success state
     ═══════════════════════════════════════════════════════ */
  var form = document.getElementById('inquiryForm');
  if (!form) return;

  // Turn off native validation only now that JS is definitely running, so its
  // own messages take over. If this script never loads, the browser's built-in
  // required/email checks still apply and the form posts to Formspree normally.
  form.noValidate = true;

  var statusEl = document.getElementById('formStatus');
  var successEl = document.getElementById('formSuccess');
  var submitBtn = document.getElementById('submitBtn');
  var resetBtn = document.getElementById('resetForm');

  // True until the real Formspree ID is pasted into index.html.
  // This is a structural guard: rather than posting into the void and
  // showing a fake "thanks", the form says plainly that it isn't wired up.
  var NOT_CONNECTED = /YOUR_FORM_ID/.test(form.getAttribute('action'));

  var FALLBACK_MSG =
    'That didn’t send. Email management@talishagrobler.com instead and I’ll pick it up there.';

  var EMAIL_RE = /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/;

  var RULES = {
    name:    function (v) { return v.length >= 2 ? '' : 'Your name, please.'; },
    email:   function (v) { return EMAIL_RE.test(v) ? '' : "That email doesn't look right."; },
    company: function (v) { return v.length >= 2 ? '' : 'Which brand is this for?'; },
    message: function (v) { return v.length >= 12 ? '' : 'Give me a bit more to work with.'; }
  };

  var setError = function (input, msg) {
    var field = input.closest('.field');
    var err = field.querySelector('.err');
    field.classList.toggle('has-error', !!msg);
    err.textContent = msg;
    input.setAttribute('aria-invalid', msg ? 'true' : 'false');
  };

  var validateField = function (input) {
    var rule = RULES[input.name];
    if (!rule) return true;
    var msg = rule(input.value.trim());
    setError(input, msg);
    return !msg;
  };

  Object.keys(RULES).forEach(function (name) {
    var input = form.elements[name];
    if (!input) return;
    // Only nag after they've left the field once — not while typing the first letter.
    input.addEventListener('blur', function () { validateField(input); });
    input.addEventListener('input', function () {
      if (input.closest('.field').classList.contains('has-error')) validateField(input);
    });
  });

  var showStatus = function (msg, kind) {
    statusEl.textContent = msg;
    statusEl.className = 'form-status is-visible' + (kind ? ' ' + kind : '');
  };

  var clearStatus = function () {
    statusEl.textContent = '';
    statusEl.className = 'form-status';
  };

  form.addEventListener('submit', function (e) {
    e.preventDefault();
    clearStatus();

    var firstBad = null;
    Object.keys(RULES).forEach(function (name) {
      var input = form.elements[name];
      if (input && !validateField(input) && !firstBad) firstBad = input;
    });

    if (firstBad) {
      firstBad.focus();
      showStatus('Almost — check the fields above.', 'is-error');
      return;
    }

    if (NOT_CONNECTED) {
      showStatus(
        'Form not connected yet — add your Formspree ID in index.html (see README).',
        'is-note'
      );
      return;
    }

    submitBtn.classList.add('is-busy');
    submitBtn.textContent = 'Sending…';

    fetch(form.action, {
      method: 'POST',
      body: new FormData(form),
      headers: { Accept: 'application/json' }
    })
      .then(function (res) {
        if (res.ok) return res.json().catch(function () { return {}; });
        return res.json()
          .catch(function () { return null; })
          .then(function (data) { throw formspreeError(data); });
      })
      .then(function () {
        form.hidden = true;
        successEl.hidden = false;
        successEl.scrollIntoView({ behavior: 'smooth', block: 'center' });
      })
      .catch(function (err) {
        // Only show a message we wrote ourselves. A dropped connection throws
        // a raw TypeError ('Failed to fetch') — never put that in front of a
        // brand rep; give them the email address instead.
        var msg = (err && err.friendly) ? err.message : FALLBACK_MSG;
        showStatus(msg, 'is-error');
      })
      .then(function () {
        submitBtn.classList.remove('is-busy');
        submitBtn.textContent = 'Send inquiry';
      });
  });

  // Formspree returns { errors: [{ message }] } on a rejected submit —
  // e.g. the form was deactivated, or the free-tier quota is used up.
  // Those messages are worth showing; anything else falls back.
  function formspreeError(data) {
    var msg = FALLBACK_MSG;
    if (data && Array.isArray(data.errors) && data.errors.length) {
      msg = data.errors.map(function (e) { return e.message; }).join(' ');
    }
    var err = new Error(msg);
    err.friendly = true;
    return err;
  }

  if (resetBtn) {
    resetBtn.addEventListener('click', function () {
      form.reset();
      Object.keys(RULES).forEach(function (name) {
        var input = form.elements[name];
        if (input) setError(input, '');
      });
      clearStatus();
      successEl.hidden = true;
      form.hidden = false;
      form.elements.name.focus();
    });
  }
})();
