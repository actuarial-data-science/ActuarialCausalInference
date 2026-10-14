/* ===================================================================== *
 * figure-theme.js — make <img>-embedded SVG figures theme-reactive.
 * ---------------------------------------------------------------------
 * Jupyter Book embeds `{figure}` SVGs as <img src="*.svg">. The browser
 * renders those in an isolated context, so the page's dark-mode CSS can
 * never reach inside them and their own `@media (prefers-color-scheme)`
 * only follows the OS — not the book's light/dark toggle.
 *
 * This script swaps each such <img> for the inline <svg>, re-scopes the
 * SVG's internal prefers-color-scheme rules to the book's light/dark
 * toggle, and tags it `.themed-svg`. Combined with `figure-theme.css`
 * (also keyed on the toggle) the switch now drives every figure — both
 * the shared semantic classes and each figure's bespoke colour classes.
 * ===================================================================== */
(function () {
  "use strict";

  // Re-scope each `@media (prefers-color-scheme: dark) { ... }` block so its
  // rules follow the book's light/dark *toggle* (data-theme / data-mode on
  // <html>) rather than only the OS. An inlined figure renders in the page's
  // own context, so its original OS-only media query can never react to the
  // book toggle — without this rewrite a figure with bespoke colour classes
  // (e.g. flowchart chips) stays stuck on its light palette when the book is
  // switched to dark, and vice-versa.
  //
  // For every rule inside the block we emit two scoped copies: one keyed on the
  // explicit toggle, and an `auto` fallback that follows the OS only when no
  // explicit choice is set. Selectors are scoped under `.themed-svg` so they
  // (a) never leak onto the rest of the page and (b) sit just below the
  // specificity of figure-theme.css, which therefore still wins for the shared
  // semantic classes it owns (.node, .ink-t, …) while these rules cover the
  // figure-specific classes the stylesheet does not know about.
  function scopeColorSchemeMedia(svgText) {
    return svgText.replace(
      /@media[^{]*prefers-color-scheme[^{]*\{((?:[^{}]*\{[^{}]*\})*[^{}]*)\}/gi,
      function (_, inner) {
        var toggle = "";
        var auto = "";
        inner.replace(/([^{}]+)\{([^{}]*)\}/g, function (__, sels, decls) {
          var dark = [];
          var os = [];
          sels.split(",").forEach(function (raw) {
            var s = raw.trim();
            if (!s) return;
            dark.push('html[data-theme="dark"] .themed-svg ' + s);
            dark.push('html[data-mode="dark"] .themed-svg ' + s);
            os.push(
              'html:not([data-theme="light"]):not([data-mode="light"]) ' +
              ".themed-svg " + s
            );
          });
          toggle += dark.join(",") + "{" + decls + "}";
          auto += os.join(",") + "{" + decls + "}";
          return __;
        });
        return toggle + "@media (prefers-color-scheme: dark){" + auto + "}";
      }
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
          scopeColorSchemeMedia(text),
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
