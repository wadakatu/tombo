/*! TOMBO tombo.js v0.6.0 — wadakatu design system. Optional, zero-dependency. MIT. https://github.com/wadakatu/tombo */
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

  document.addEventListener("click", function (e) {
    var t = e.target.closest && e.target.closest("[data-tombo-theme]");
    if (t) { setTheme(t.getAttribute("data-tombo-theme")); }
  });

  function init() {
    apply(stored());
    var c = document.querySelectorAll(".tombo-themes[hidden]");
    for (var i = 0; i < c.length; i++) c[i].hidden = false;
    reflect();
  }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", init);
  else init();

  window.Tombo = { setTheme: setTheme, getTheme: getTheme };
})();
