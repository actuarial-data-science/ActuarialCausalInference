/* ===================================================================== *
 * figure-theme.js — make <img>-embedded SVG figures theme-reactive.
 * ---------------------------------------------------------------------
 * Jupyter Book embeds `{figure}` SVGs as <img src="*.svg">. The browser
 * renders those in an isolated context, so the page's dark-mode CSS can
 * never reach inside them and their own `@media (prefers-color-scheme)`
 * only follows the OS — not the book's light/dark toggle.
 *
 * This script swaps each such <img> for the inline <svg>, strips the
 * SVG's internal prefers-color-scheme block, and tags it `.themed-svg`
 * so the rules in `figure-theme.css` (keyed on the book toggle) take
 * over. Single source of truth; the toggle now drives every figure.
 * ===================================================================== */
(function () {
  "use strict";

  // Remove `@media (prefers-color-scheme: ...) { ... }` blocks so that only
  // the page-level (toggle-driven) CSS controls the figure's appearance.
  function stripColorSchemeMedia(svgText) {
    return svgText.replace(
      /@media[^{]*prefers-color-scheme[^{]*\{(?:[^{}]*\{[^{}]*\})*[^{}]*\}/gi,
      ""
    );
  }

  function inlineOne(img) {
    var src = img.getAttribute("src");
    if (!src || !/\.svg(\?.*)?$/i.test(src)) return;

    fetch(src)
      .then(function (resp) {
        if (!resp.ok) throw new Error("fetch failed: " + resp.status);
        return resp.text();
      })
      .then(function (text) {
        // Only inline figures that try to theme themselves via
        // prefers-color-scheme. Other SVGs (e.g. matplotlib graphs saved
        // with a transparent background) already look right on both themes
        // and are left as <img> so their intrinsic sizing is preserved.
        if (!/prefers-color-scheme/i.test(text)) return;

        var doc = new DOMParser().parseFromString(
          stripColorSchemeMedia(text),
          "image/svg+xml"
        );
        var svg = doc.querySelector("svg");
        if (!svg || doc.querySelector("parsererror")) return;

        // Preserve the responsive sizing applied by Jupyter Book to the <img>
        // (e.g. style="width: 90%;") and let the height follow the viewBox.
        var imgStyle = img.getAttribute("style");
        svg.removeAttribute("width");
        svg.removeAttribute("height");
        if (imgStyle) svg.setAttribute("style", imgStyle);
        svg.style.height = "auto";

        var cls = (svg.getAttribute("class") || "") + " themed-svg";
        if (img.className) cls += " " + img.className;
        svg.setAttribute("class", cls.trim());
        if (img.getAttribute("alt")) svg.setAttribute("role", "img");

        img.parentNode.replaceChild(svg, img);
      })
      .catch(function () {
        /* leave the <img> in place on any failure (e.g. file:// origin) */
      });
  }

  function run() {
    var scope = document.querySelector(".bd-article") || document.body;
    var imgs = scope.querySelectorAll('img[src$=".svg"], img[src*=".svg?"]');
    Array.prototype.forEach.call(imgs, inlineOne);
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", run);
  } else {
    run();
  }
})();
