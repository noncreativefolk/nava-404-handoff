# NAVA × 404 — Website Handoff

Complete, approved website package for **navax404.com** — pre-launch homepage, post-launch homepage, five brand pages, and all imagery. Static site: no build step, no server code, no database.

## Get the package

**Option A — rebuild from source (this repo):**

```
python3 build.py
```

This produces `NAVA-404-website-handoff-v1/` and `NAVA-404-website-handoff-v1.zip`. The script downloads the approved page payloads and images from public sources, **verifies md5 checksums against the project ledger** (aborts on any mismatch), and swaps CDN image URLs to local filenames. Requires Python 3.6+ (standard library only) and internet access.

**Option B — ready-made zip:** the identical package (`NAVA-404-website-handoff-v1.zip`, 3.4 MB) is already built and available from the project owner.

## Then deploy

Follow **DEPLOYMENT-README.md** (included in the package): upload the folder contents to any static host as-is; rename `index-post-launch.html` to `index.html` at opening (target 10 Dec 2026) — that is the entire go-live switch. Forms are front-end-only by design; wiring options are documented in the README.

## Package contents

| File | Purpose |
|---|---|
| `index.html` | Pre-launch homepage — deploy now. Full 00→04 gateway flow |
| `index-post-launch.html` | Post-launch homepage — rename to `index.html` at opening |
| `nava.html` / `404.html` | Brand pages (reserve & menus / reserve & line-up) |
| `find-us.html` / `programmes.html` / `careers.html` | Location & contacts / Muse Society & Inner Circle / recruitment |
| 23 image files | All imagery, referenced by bare filename — keep the flat structure |

Note: the workspace zip additionally carries `logo-nava-black-sm.png`, an unused spare asset no page references; it is omitted here.

## Reference previews (eyeball only)

- Pre-launch: https://noncreativefolk.github.io/nx4-site-previews/pre-launch/
- Post-launch: https://noncreativefolk.github.io/nx4-site-previews/post-launch/

Previews render the same pages via a delivery workaround (proxied images) — the package contains the real local assets.

---
Handoff v1 · NAVA × 404 project state v5.14
