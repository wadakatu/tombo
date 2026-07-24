// TOMBO stylelint config — the Baseline gate + a minimal set of genuine-error rules.
//
// The ignore* lists below are the "PE ledger": every CSS feature TOMBO uses that is
// NOT Baseline-widely, each with why it's allowed. It's pinned empirically — running
// `use-baseline` at "widely" flags exactly these, no more. Keep it honest: CI fails
// when a NEW non-widely feature appears until it's added here with a justification
// (or wrapped in @supports). tombo.css itself is never edited to satisfy the linter.
export default {
  plugins: ["stylelint-plugin-use-baseline"],
  rules: {
    "plugin/use-baseline": [true, {
      available: "widely",
      ignoreFunctions: [
        "light-dark",     // Baseline newly 2024 — the token foundation; the whole system is built on it
        "rect",           // legacy rect() in the .tombo-sr-only clip fallback (paired with clip-path)
      ],
      ignoreSelectors: [
        "has",            // :has() — Baseline newly 2023; opt-in scoping (glow/trim guards), degrades harmlessly
        "selection",      // ::selection — cosmetic highlight; degrades to the native selection color
      ],
      ignoreProperties: {
        "text-autospace":     ["/^.+$/"], // Limited (Chromium) — wholesale PE: unsupported → tight 和欧, degrades not breaks
        "print-color-adjust": ["exact"],  // print-only; the -webkit- alias covers the rest; makes mark backgrounds print
        "accent-color":       [],         // native checkbox/radio tint; degrades to the UA accent
        "orphans":            [],         // print pagination control; ignored on screen
        "widows":             [],         // print pagination control; ignored on screen
        "clip":               [],         // deprecated but universal — legacy .tombo-sr-only fallback, paired with clip-path
        "break-after":        ["avoid"],  // fragmentation control (keep a heading with its section); print PE
      },
      ignoreAtRules: [
        "page",           // @page margin — print-only, ignored by screen engines
      ],
    }],
    // Minimal genuine-error rules — real bugs only, not the stylistic standard config
    // (which would fight TOMBO's hand-authored formatting). All report zero on tombo.css.
    "color-no-invalid-hex": true,
    "declaration-block-no-duplicate-properties": true,
    "block-no-empty": true,
    "no-duplicate-selectors": true,
    "property-no-unknown": true,
    "unit-no-unknown": true,
  },
};
