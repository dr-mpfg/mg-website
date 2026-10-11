/* Matteo Giordano — site.js. Nav toggle, reveal-on-scroll, config wiring, writing list. No network requests except data/writing.json. */
(function () {
  'use strict';
  document.documentElement.className += ' js';
  var cfg = window.MG_CONFIG || {};
  var reduceMotion = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  function applyConfig() {
    var email = cfg.CONTACT_EMAIL || '';
    if (/\S+@\S+\.\S+/.test(email)) {
      var m = document.querySelectorAll('[data-mailto]');
      for (var i = 0; i < m.length; i++) {
        var subject = m[i].getAttribute('data-subject');
        m[i].setAttribute('href', 'mailto:' + email + (subject ? '?subject=' + encodeURIComponent(subject) : ''));
        if (m[i].hasAttribute('data-show-email')) m[i].textContent = email;
      }
    }
    var links = document.querySelectorAll('[data-link]');
    for (var j = 0; j < links.length; j++) {
      var key = links[j].getAttribute('data-link');
      if (typeof cfg[key] === 'string' && /^https:\/\//.test(cfg[key])) links[j].setAttribute('href', cfg[key]);
    }
  }

  function initNav() {
    var toggle = document.querySelector('.nav__toggle');
    var links = document.querySelector('.nav__links');
    if (!toggle || !links) return;
    function setOpen(open) {
      links.classList.toggle('is-open', open);
      document.body.classList.toggle('nav-open', open);
      toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
      toggle.querySelector('.nav__toggle-label').textContent = open ? 'Close' : 'Menu';
    }
    toggle.addEventListener('click', function () { setOpen(toggle.getAttribute('aria-expanded') !== 'true'); });
    links.addEventListener('click', function (e) { if (e.target.closest('a')) setOpen(false); });
    document.addEventListener('keydown', function (e) { if (e.key === 'Escape') setOpen(false); });
  }

  function initReveal() {
    var els = document.querySelectorAll('.reveal');
    if (!els.length) return;
    if (reduceMotion || !('IntersectionObserver' in window)) {
      for (var i = 0; i < els.length; i++) els[i].classList.add('is-visible');
      return;
    }
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) { if (en.isIntersecting) { en.target.classList.add('is-visible'); io.unobserve(en.target); } });
    }, { threshold: 0.1, rootMargin: '0px 0px -30px 0px' });
    for (var j = 0; j < els.length; j++) io.observe(els[j]);
  }

  function renderLatest(items) {
    var slot = document.getElementById('latest-note');
    if (!slot || !items.length || !items[0].title) return;
    var it = items[0];
    var t = slot.querySelector('.latest__title'), m = slot.querySelector('.latest__meta');
    if (!t) return;
    var a = document.createElement('a'); a.textContent = it.title;
    if (it.href && /^https:\/\//.test(it.href)) { a.setAttribute('href', it.href); a.setAttribute('rel', 'noopener'); a.setAttribute('target', '_blank'); }
    t.textContent = ''; t.appendChild(a);
    if (m && it.date) m.textContent = it.date + ' · Cargo & Collateral';
  }

  function initWriting() {
    var list = document.getElementById('writing-list');
    var empty = document.getElementById('writing-empty');
    var latest = document.getElementById('latest-note');
    if ((!list || !empty) && !latest) return;
    if (!window.fetch) return;
    fetch('/data/writing.json', { cache: 'no-cache' }).then(function (r) { return r.json(); }).then(function (items) {
      if (!Array.isArray(items) || !items.length) return;
      renderLatest(items);
      if (!list || !empty) return;
      items.forEach(function (it) {
        if (!it || !it.title) return;
        var li = document.createElement('li'); li.className = 'writing__item';
        var d = document.createElement('span'); d.className = 'writing__date'; d.textContent = it.date || '';
        var t = document.createElement(it.href && /^https:\/\//.test(it.href) ? 'a' : 'span'); t.className = 'writing__title'; t.textContent = it.title;
        if (t.tagName === 'A') { t.setAttribute('href', it.href); t.setAttribute('rel', 'noopener'); t.setAttribute('target', '_blank'); }
        li.appendChild(d); li.appendChild(t); list.appendChild(li);
      });
      if (list.children.length) { list.removeAttribute('hidden'); empty.setAttribute('hidden', ''); }
    }).catch(function () { /* keep the static fallback */ });
  }

  function init() { applyConfig(); initNav(); initReveal(); initWriting(); }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init); else init();
})();
