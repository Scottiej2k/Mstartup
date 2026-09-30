# Publishing chapter changes to the reader

The reader carries its chapters twice: built into the page (so it always renders) and as documents in the artifact database (so the **Update** button, top right, can pull the latest text without anyone reloading or republishing the page).

## After any chapter change
1. `python3 tools/build_reader.py`. This writes the page and `reader/db/cNN.json` + `reader/db/meta.json`.
2. `ArtifactData` **list** `chapters` on the artifact to get current `version`s.
3. `ArtifactData` **batch**: `set` each changed chapter (`doc_id` `cNN`, `file_path` `reader/db/cNN.json`, `if_version` from step 2; omit `if_version` for a new chapter), then `set` `meta/build` from `reader/db/meta.json` (list `meta` first for its version). Write `meta/build` **last**: the reader watches it and shows an "Update" dot when its stamp changes.
4. Also republish `reader/the-marriage-startup.html` (same file path; capabilities carry forward) so the built-in copy matches. This is required whenever `tools/reader_template.html` changed, and keeps the fallback fresh otherwise.
5. Commit and push.

## How it behaves for Scott
- On load the page compares its built-in build stamp with `meta/build`. If they differ it silently pulls the newer chapters.
- While the page is open, a change to `meta/build` lights a dot on **Update** and shows a toast. Pressing **Update** (or "Check for updates" under the chapter list) swaps in only the chapters whose hash changed, then re-applies highlights and pending direct edits.
- If a paragraph is mid-edit, that chapter is skipped until Scott finishes it.
- Only editors can write `chapters` and `meta` (access rules declared on the artifact). The page builds chapter text with escaped Markdown only, never raw HTML.

## If the page looks old
A tab opened before the Update button existed has no Update code. One hard refresh (or reopening the link) loads the current page; after that it pulls updates itself.
