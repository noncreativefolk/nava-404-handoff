# NAVA × 404 — Website Deployment Handoff (v1, 2026-10-02)

Static website. **No build step, no server code, no database.** Plain HTML/CSS/JS — host it anywhere that serves static files over HTTPS.

---

## 1. What's in this package

| File | Purpose |
|---|---|
| `index.html` | **Pre-launch homepage — DEPLOY THIS ONE NOW.** Full gateway flow: 00 error → 01 scan → 02 findings → 03 LOCATION FOUND + brand panels → "find your way in →" → 04 ACCESS (four registration tracks). md5 `a44c4b1d910c2261008992406caed35b` |
| `index-post-launch.html` | **Post-launch homepage.** Normal-scroll landing: hero → split screen → quick links → 04 ACCESS. **Rename to `index.html` at opening (target 10 Dec 2026)** — that's the entire go-live switch. md5 `2ee6a46097e5c6d50934ca13b23c54d1` |
| `nava.html` | NAVA brand page (reserve & menus) |
| `404.html` | 404 Club Not Found brand page (reserve & line-up) |
| `find-us.html` | Location & contacts |
| `programmes.html` | Muse Society & Inner Circle |
| `careers.html` | Recruitment ("typical job description not found") |
| 24 image files (`.jpg`/`.png`) | All imagery, referenced by bare filename — **keep the flat structure**, do not move into subfolders |

**Total:** 31 files. Upload all of them to the web root as-is.

## 2. Deploy (any of these)

- **Netlify / Vercel / Cloudflare Pages:** drag-and-drop the folder, or connect a git repo containing these files. Done.
- **S3 / OSS / cPanel / nginx:** upload to the web root; serve `index.html` as the directory index (default everywhere).
- **Domain:** point `navax404.com` (and `www`) at the host; force HTTPS. The brand architecture reserves `nava.sg` and `404clubnotfound.sg` as separate future layers — out of scope for this package.
- No rewrites, headers, or redirects required. All navigation is same-folder relative links.

## 3. Forms — IMPORTANT (front-end only by design)

The three forms in 04 ACCESS **do not send anything anywhere**. On submit they show "interest noted — thank you" and disable the inputs (`window.noted()` in `index.html`). No data leaves the visitor's browser.

To capture leads before launch, wire each form to an endpoint — simplest options: Formspree/Basin (change `onsubmit` to `action` + `method="POST"`), or a small backend/Google Sheet webhook. The three forms:

| Track | Fields |
|---|---|
| Launch Access (waitlist) | email |
| Muse Society | name, whatsapp, instagram @ (optional) |
| Inner Circle — Co-Founders | name, whatsapp, instagram @ (optional) |

The pages already carry PDPA consent wording; keep it adjacent to whatever endpoint you add. **Copy is locked — add the plumbing, don't rewrite the text.**

**Mailto links** (no wiring needed, but the mailboxes must exist): `enquiries@`, `recruitment@`, `media@`, `marketing@`, `Cofounders@navax404.com` — used by reserve/access buttons, careers roles, and the find-us contact list.

## 4. External dependencies (only two, both font CDNs)

- Google Fonts: Space Grotesk, JetBrains Mono, Noto Sans SC (all pages)
- Fontshare: Clash Display (brand pages)

Requires internet access at view time — standard for font CDNs. Everything else (images, JS, CSS) is local/inline. No JS frameworks, no trackers, no cookies.

## 5. Reference previews (already public)

- Pre-launch: https://noncreativefolk.github.io/nx4-site-previews/pre-launch/
- Post-launch: https://noncreativefolk.github.io/nx4-site-previews/post-launch/

These render the same pages via a delivery workaround (proxied images); **your package contains the real local assets — ignore the preview internals entirely.** Use the previews only to eyeball the intended result.

## 6. Notes

- Built-in EN/中文 toggle — no action needed.
- `silhouettes.mp4` exists in the design workspace but is not referenced by any page; excluded from this package.
- Accessibility/mobile: responsive layout and viewport meta are in place; test on real devices as usual.
- Version ledger and full project state: see `00_STATE.md` (v5.13) in the project workspace.
