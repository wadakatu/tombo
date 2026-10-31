# Upgrading a vendored TOMBO copy

TOMBO is copied into consuming projects; merging a change here does not update
those copies. Keep the source revision and SHA-256 hashes next to the vendored
CSS, optional JS, and license. The banner alone is not a content identity:
unreleased main-branch changes can still carry the previous release's version.

## Unreleased changes since v0.14.1

This section describes the current development line, not a published release.
Do not change a consumer's pin to a tag until that tag exists. Review the source
diff as well as this guide when selecting an update.

| Area | Changed behavior | Check in the consuming app |
| --- | --- | --- |
| Navigation | Empty or `false` aria-current no longer shows a current-position marker. | Use `page`, `step`, or another appropriate current value only on the current item. Remove empty-attribute workarounds. |
| Row headers | `th[scope="row"]` preserves letter case and uses table text size and data-row borders. | Check row height and identifiers; inspect consumer overrides before removing them. Column headings retain their existing style. |
| Code focus | Code controls use code-green for focus; the pre outline is inset to avoid clipping. | Tab to Copy and pre, check both themes, then scroll the code with arrow keys. |
| Compact controls | Theme and copy controls have a minimum 24×24 CSS pixel target. | Check caption height, alignment and narrow layouts with customized labels. |
| Theme state | `getTheme()` reports this page's active selection even when storage fails. Invalid setting names are ignored. | Call `Tombo.setTheme()` instead of writing storage directly. Out-of-band storage writes are not a synchronization API; reload to read persisted changes. |
| Copy failure | A rejected/unavailable clipboard call selects the code and focuses pre before announcing manual-copy instructions. | Check the fallback with your syntax highlighter and focus handling. Keep pre focusable. |
| Skip link | New optional `.tombo-skip-link` pattern. | Adoption requires a first link and matching focusable main target; copying the CSS alone does not add it. See [layout](layout.md#skip-repeated-navigation). |

No existing class or token is removed by these changes. There are visible and
behavioral differences, so this is not a promise of pixel-identical rendering.
The example-page heading/landmark improvements and AI documentation do not alter
markup in consuming applications automatically.

## Consumer update procedure

1. Record the current tag or commit, hashes, and any local edits. Compare local
   edits before replacing files; keep product-specific overrides in consumer CSS.
2. Choose an existing release tag and read the references from that same tag.
   The main-branch `llms.txt` links point to main and can describe newer behavior.
3. In a reviewable application branch, copy CSS and LICENSE from the selected
   tag using the [vendoring instructions](../README.md#quick-start). If the app
   uses `tombo.js`, update that copy from the same tag. Do not add JS to an app
   that does not need its optional behaviors.
4. Compute fresh SHA-256 hashes from the copied bytes and update the app's pins.
   Verify its CI checks those hashes. Do not reuse hashes from a different tag
   or from this repository's working tree.
5. Run the application's checks and review the actual affected pages, using the
   table above. At minimum check narrow and wide layouts, both themes, keyboard
   focus and relevant error states. TOMBO's own gate does not test application
   overrides or runtime data.
6. Review the application diff before deployment. Preserve the previous files
   and pin record in version control so they can be restored together.

For rollback, revert the application's vendored files, license, hash/version pin
record and any coupled markup or override changes as one reviewed change. Run
the same application checks again. Reverting only the pin text does not restore
an older stylesheet, and reverting TOMBO's upstream main does not update an app.

## Maintainer release preparation

A release requires a coordinated version change and tag; a documentation PR is
not a release. Keep current Quick start commands pointing to the existing tag
until the release is ready to be made available.

- Review the CSS/JS diff against the last release and the consumer-facing changes
  above. Additions such as the skip-link class should be reflected in the chosen
  release version and release notes.
- Update both file banners and all three vendoring examples in README.md,
  index.html and ja/index.html together. Update the site's visible REV labels.
  `package.json` is private tooling, not an npm distribution version.
- Regenerate agent docs with `python3 scripts/build_agent_docs.py`, then run
  `npm run check`. Confirm the tag name with the banner check before tagging,
  for example by setting `GITHUB_REF=refs/tags/vX.Y.Z` to the chosen actual version
  when invoking `python3 scripts/check_banner.py`.
- Review and approve publication before creating/pushing the tag or a release.
  Do not leave public Quick start instructions pointing at a nonexistent tag.
- After publication, confirm the tag resolves to the intended commit and that
  tagged CSS/JS/license bytes match the reviewed artifacts. Verify the tag CI and
  published documentation. Only then propose updates to consuming applications.

The ordinary CI workflow verifies pushes/PRs/tags; it does not create a tag,
publish an npm package, or update consumers. Release publication and consumer
rollout are separate operations with their own review.
