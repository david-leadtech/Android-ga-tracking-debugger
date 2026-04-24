# Repository (canonical remote)

All development, CI, releases, and issues use this repository only:

**https://github.com/david-leadtech/Android-ga-tracking-debugger**

## Point your local clone at this repo

If `git remote -v` still shows another GitHub owner for `origin`, run:

```bash
git remote set-url origin https://github.com/david-leadtech/Android-ga-tracking-debugger.git
git fetch origin
```

You do not need a separate `fork` remote if `origin` is this URL: use `git push origin <branch>` and `git push origin v1.x.y` for tags.

## License and attribution

The software remains under the **Custom Shared-Profit License (CSPL)** in `LICENSE.txt`. Copyright notices in that file and in source headers refer to the original author; this repository is a maintained fork with additional changes documented in `CHANGELOG.md`.
