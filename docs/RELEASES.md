# Releases

## Version source of truth

The application version is `__version__` in `main.py` (window title and JSON export `app_version`). **Git tags use the same number** with a `v` prefix: `1.0.0` → tag `v1.0.0`.

## Versioning model (this fork)

1. **`v1.0.0`** — First GitHub release: documents the product **as it is today** (baseline for this repo).
2. **Ongoing work** — Commits and PRs on `main` (or feature branches merged via PR).
3. **`v1.1.0`** (and later `1.2.0`, etc.) — When you ship a meaningful batch of changes:
   - bump `__version__` in `main.py`
   - move notes from `## [Unreleased]` to a new `## [x.y.z]` section in `CHANGELOG.md`
   - tag `vx.y.z` and push the tag so the Release workflow runs.

Patch releases (`1.0.1`) are for small fixes on the same minor line without new features.

## Publish a release (example: first release `v1.0.0`)

1. Confirm `__version__` in `main.py` matches the changelog section you are releasing.
2. Merge your work to the default branch (`main`) if it is not already there.
3. Create and push an annotated tag from that commit:

   ```bash
   git tag -a v1.0.0 -m "Release v1.0.0"
   git push origin v1.0.0
   ```

4. The **Release** workflow (`.github/workflows/release.yml`) runs on tag push and creates a GitHub Release with auto-generated notes. You can edit the release on GitHub afterward.

## Next release example (`v1.1.0`)

After new features or fixes are merged:

1. Set `__version__ = "1.1.0"` in `main.py`.
2. In `CHANGELOG.md`, add `## [1.1.0] - YYYY-MM-DD` and list changes; leave `## [Unreleased]` for the next cycle.
3. Commit to `main`, then:

   ```bash
   git tag -a v1.1.0 -m "Release v1.1.0"
   git push origin v1.1.0
   ```
