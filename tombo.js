/*! TOMBO tombo.js v0.9.0 — wadakatu design system. Optional, zero-dependency. MIT. https://github.com/wadakatu/tombo */
(function () {
  "use strict";
  var KEY = "tombo-theme";
  var VALID = { system: 1, tombo: 1, hotaru: 1 };

  function stored() {
    try { var t = localStorage.getItem(KEY); return (t === "tombo" || t === "hotaru") ? t : "system"; }
    catch (e) { return "system"; }
  }
  function apply(setting) {
    var root = document.documentElement;
    if (setting === "tombo" || setting === "hotaru") root.dataset.theme = setting;
    else delete root.dataset.theme;
  }
  function reflect() {
    var cur = stored(), btns = document.querySelectorAll("[data-tombo-theme]");
    for (var i = 0; i < btns.length; i++)
      btns[i].setAttribute("aria-pressed", String(btns[i].getAttribute("data-tombo-theme") === cur));
  }
  function setTheme(setting) {
    if (!VALID[setting]) return;
    try { if (setting === "system") localStorage.removeItem(KEY); else localStorage.setItem(KEY, setting); }
    catch (e) {}
    apply(setting); reflect();
  }
  function getTheme() { return stored(); }

  var live;
  function ensureLive() {
    if (live) return;
    live = document.createElement("div");
    live.className = "tombo-sr-only";
    live.setAttribute("role", "status");
    live.setAttribute("aria-live", "polite");
    document.body.appendChild(live);
  }
  function announce(msg) { ensureLive(); live.textContent = ""; live.textContent = msg; }
  function injectCopy() {
    var blocks = document.querySelectorAll(".tombo-code:not([data-tombo-copy='off'])");
    for (var i = 0; i < blocks.length; i++) {
      var fig = blocks[i];
      if (fig.querySelector(".tombo-copy")) continue;
      var cap = fig.querySelector("figcaption");
      if (!cap) { cap = document.createElement("figcaption"); fig.insertBefore(cap, fig.firstChild); }
      var btn = document.createElement("button");
      btn.type = "button"; btn.className = "tombo-copy";
      btn.setAttribute("aria-label", "Copy code"); btn.textContent = "COPY ⧉";
      cap.appendChild(btn);
    }
  }
  function copyFrom(btn) {
    var fig = btn.closest(".tombo-code"); if (!fig) return;
    var pre = fig.querySelector("pre"); if (!pre) return;
    var done = function () {
      btn.textContent = "COPIED ✓"; announce("Copied");
      setTimeout(function () { btn.textContent = "COPY ⧉"; }, 1500);
    };
    var fail = function () { announce("Press Ctrl or Cmd + C to copy"); };
    try {
      if (navigator.clipboard && navigator.clipboard.writeText)
        navigator.clipboard.writeText(pre.textContent).then(done, fail);
      else fail();
    } catch (e) { fail(); }
  }

  document.addEventListener("click", function (e) {
    if (!e.target.closest) return;
    var t = e.target.closest("[data-tombo-theme]");
    if (t) { setTheme(t.getAttribute("data-tombo-theme")); return; }
    var c = e.target.closest(".tombo-copy");
    if (c) { copyFrom(c); }
  });

  function init() {
    ensureLive();
    apply(stored());
    var c = document.querySelectorAll(".tombo-themes[hidden]");
    for (var i = 0; i < c.length; i++) c[i].hidden = false;
    reflect();
    injectCopy();
  }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", init);
  else init();

  window.Tombo = { setTheme: setTheme, getTheme: getTheme };
})();
