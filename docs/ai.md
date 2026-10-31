# Using TOMBO with AI agents

TOMBO is a vendored, framework-independent CSS design system, not an npm UI
package. Start with this guide, then read only the reference needed for the task.
The repository's `llms.txt` is a small index; `llms-full.txt` combines the current
reference for clients that cannot follow links. Automatic discovery depends on
the agent: explicitly provide the file or URL when necessary.

## Source and version

- `tombo.css` is authoritative for tokens, selectors and current behavior.
- The top-level `docs/*.md` references and `examples/components.html` describe
  supported usage. `docs/superpowers/` contains historical decisions, not the
  current API contract; do not implement a historical proposal without checking
  the current stylesheet.
- Main-branch documentation can contain unreleased changes. When working on an
  existing application, inspect its vendored CSS/JS banner and recorded hash,
  and use the matching release tag. Do not silently upgrade a consuming app.
- Copy CSS and LICENSE from the same release as described in [README](../README.md).
  Copy `tombo.js` only when theme persistence or copy buttons are needed.
  Do not invent an npm install command, CDN URL, React import or build step.

## Choose a reference by task

| Task | Read | Working example |
| --- | --- | --- |
| Colors, typography, themes | [Foundations](foundations.md) | [Catalog](../examples/components.html) |
| Containers, spacing, responsive content | [Layout](layout.md) | [Docs](../examples/docs.html) |
| Brand marks and visual intensity | [Signatures](signatures.md) | [Landing page](../examples/lp.html) |
| Inputs and validation | [Forms](forms.md) | [Catalog forms](../examples/components.html#c17) |
| Application header and navigation | [Topbar](topbar.md) | [App](../examples/app.html) |
| Charts and data alternatives | [Charts](charts.md) | [Catalog charts](../examples/components.html#c19) |
| Theme control and clipboard | [Behavior](tombo-js.md) | [Catalog](../examples/components.html) |
| Printing | [Print](print.md) | [Docs](../examples/docs.html) |

For complete compositions, start with [integration recipes](recipes.md): a settings
form with an error-state replacement and a keyboard-scrollable data table.

## Implementation contract

Reuse the documented HTML and class names before writing custom CSS. Inspect
`tombo.css` for any class or token not shown in a reference; never infer that a
utility exists from its name. Use consumer styles for page layout and keep
vendored files intact.

- Keep body text in the body voice and instrument labels/numbers in mono.
  Use the display voice for Latin display headings, not Japanese headings.
- Shu is the current-position line, not a filled primary button. Use the existing
  green primary button. Preserve the docs/app/LP intensity choices in the examples.
- Reuse space and type tokens. Use `padding-block` rather than a padding shorthand
  on `.tombo-shell`, so consumer styles do not erase its horizontal gutters.
- Use native links for navigation and buttons for actions. `aria-current="page"`
  marks a current navigation link; a tab widget needs its own keyboard behavior
  and `aria-selected`. CSS does not implement that behavior.
- Wire labels, required fields, help and errors as shown in the forms reference.
  Give scrollable tables a focusable, named region; give code `pre` elements
  `tabindex="0"`. Do not remove focus outlines.
- Avoid assuming every foreground works on every surface. Read the supported
  contrast combinations, especially on raised and glowing backgrounds.
- Keep optional JavaScript optional: the page must remain usable without it.

## Verify the result

For a consuming app, run that app's checks and open its real pages. Check narrow
and wide screens, both themes, keyboard focus, overflow, and relevant error states.
Do not treat TOMBO's token contrast gate as certification of a composed page.
For this repository, run `npm ci` and `npm run check`; inspect changed components
in the local examples. Report any browser or assistive-technology checks not run.

Example request to an agent:

> Read docs/ai.md and docs/forms.md from the same TOMBO revision as our vendored
> stylesheet. Build the settings form using native controls and existing tokens.
> Preserve the vendored files. Verify labels, errors, keyboard focus and both themes.

## Maintaining agent documentation

Edit the source Markdown, then run `python3 scripts/build_agent_docs.py`.
Commit the updated `llms.txt` and `llms-full.txt`. CI runs the generator with
`--check` and rejects stale output, missing indexed sources, or broken local Markdown
link targets in the exported reference. External URLs and fragment IDs are not
validated; the local check also accepts existing directories. The full export
includes only the current reference, not design history or executable source.
No model API, MCP server, or extra package is required.

The generated files use main-branch source URLs; they describe the checkout used
to generate them and are not a versioned release service. For a release, fetch
these files and the references from that tag instead.

## Design rationale and research (2026-11-01)

- [shadcn/ui's actual index](https://ui.shadcn.com/llms.txt) groups links by task.
  TOMBO adopts selective retrieval so agents need not load the entire history.
- [Astro's AI guide](https://docs.astro.build/en/guides/build-with-ai/) provides
  both index and full documentation. TOMBO adopts both access patterns while
  generating them from existing Markdown to avoid a separate, drifting manual.
- [The llms.txt proposal](https://llmstxt.org/) describes a concise Markdown entry
  point with links. It is a documentation convention, not a guarantee that every
  agent discovers or follows it. TOMBO also links the entry point from its README.
- TOMBO-specific choice: retain CSS and native HTML as the API. A tool server or
  framework-specific registry would add maintenance without being necessary to
  retrieve this small static reference. This decision can be revisited if actual
  integrations require executable discovery or installation tools.
