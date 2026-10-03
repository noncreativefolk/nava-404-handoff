#!/usr/bin/env python3
"""
NAVA x 404 website handoff - package builder

Rebuilds the complete, deployable website package from public sources:
  1. downloads the approved page payloads from the public preview repo
  2. verifies md5 checksums against the project ledger (aborts on mismatch)
  3. swaps CDN image URLs back to local filenames
  4. downloads the 23 referenced images
  5. copies DEPLOYMENT-README.md into the package and zips it

Requires: Python 3.6+ (standard library only), internet access.
Usage:    python3 build.py
Output:   NAVA-404-website-handoff-v1/  and  NAVA-404-website-handoff-v1.zip
"""
import base64
import gzip
import hashlib
import json
import os
import sys
import time
import urllib.request
import zipfile

RAW = "https://raw.githubusercontent.com/noncreativefolk/nx4-site-previews/gh-pages"
OUT = "NAVA-404-website-handoff-v1"
ZIPNAME = OUT + ".zip"
WESERV = "https://images.weserv.nl/?url="
UA = {"User-Agent": "nava404-handoff-builder/1.0"}

# local filename -> hosted origin (uguu.se holds the original uploads;
# the previews reference the same files through the weserv.nl CDN proxy)
IMAGES = {
    "logo-lockup-white-sm.png": "n.uguu.se/KcgmnUBd.png",
    "nava-hero.jpg":            "n.uguu.se/hAgYjkVT.jpg",
    "c404-room.jpg":            "h.uguu.se/aOXHmthF.jpg",
    "f01-city.jpg":             "d.uguu.se/OBADdkbh.jpg",
    "f02-quay.jpg":             "h.uguu.se/oOoJwaDn.jpg",
    "f03-architecture.jpg":     "n.uguu.se/WCORaKpX.jpg",
    "f04-coffee.jpg":           "h.uguu.se/UWwDewwy.jpg",
    "f05-dining.jpg":           "h.uguu.se/xbRJpHxk.jpg",
    "f06-cocktails.jpg":        "d.uguu.se/YvgwQQqd.jpg",
    "f07-table.jpg":            "h.uguu.se/PYlEmWVv.jpg",
    "f08-spaces.jpg":           "d.uguu.se/HzTbpQFj.jpg",
    "f09-dj.jpg":               "d.uguu.se/EojQXVkx.jpg",
    "f10-crowd.jpg":            "d.uguu.se/JKKgxECB.jpg",
    "f11-party.jpg":            "d.uguu.se/MSEramzE.jpg",
    "f12-lights.jpg":           "h.uguu.se/KDmaurDO.jpg",
    "nava-room.jpg":            "n.uguu.se/eyQdKMXm.jpg",
    "scan-drink.jpg":           "h.uguu.se/cFScbEvG.jpg",
    "scan-eat.jpg":             "d.uguu.se/DkuKnwGC.jpg",
    "scan-live.jpg":            "h.uguu.se/fbdrSVUM.jpg",
    "scan-network.jpg":         "d.uguu.se/eexxOKky.jpg",
    "scan-socialise.jpg":       "n.uguu.se/LhUQVBpy.jpg",
    "scan-party.jpg":           "d.uguu.se/ZeQiGEze.jpg",
    "silhouette.jpg":           "n.uguu.se/KAitQARd.jpg",
}

# (output name, payload path, patch files, expected md5 of decoded HTML)
PAGES = [
    ("index.html",      "pre-launch/data/index.txt",      [],                                          "b9391e48f83ee0d1f0db6b079e5d7dd2"),
    ("nava.html",       "post-launch/data/nava.txt",      ["post-launch/data/nava.p1",
                                                             "post-launch/data/nava.p2"],               "ffc274ba6b421cab158dd6b2597cfdfe"),
    ("404.html",        "post-launch/data/404.txt",       [],                                          "66d5a2662a0fd4ac8e7e56b6d6e66856"),
    ("find-us.html",    "post-launch/data/find-us.txt",   [],                                          "7b828b107024025ade25feb3301ce1d6"),
    ("programmes.html", "post-launch/data/programmes.txt", [],                                         "b2486da5ca9650e2ad9f69d37a04de76"),
    ("careers.html",    "post-launch/data/careers.txt",   [],                                          "13a5e8f5d3167d32284e773fbd6de248"),
]

# after the URL swap, index.html must equal the approved pre-launch master
EXPECTED_LOCAL_INDEX = "a44c4b1d910c2261008992406caed35b"


def fetch(url, tries=4):
    last = None
    for i in range(tries):
        try:
            req = urllib.request.Request(url, headers=UA)
            with urllib.request.urlopen(req, timeout=180) as r:
                return r.read()
        except Exception as e:
            last = e
            time.sleep(3 * (i + 1))
    sys.exit("download failed: %s (%s)" % (url, last))


def md5(b):
    return hashlib.md5(b).hexdigest()


def decode_payload(path, patches):
    lines = fetch(RAW + "/" + path).decode("utf-8").split("\n")
    for p in patches:
        patch = json.loads(fetch(RAW + "/" + p).decode("utf-8"))
        for k, v in patch.items():
            lines[int(k) - 1] = v  # patch keys are 1-based line numbers
    clean = "".join("".join(lines).split())
    return gzip.decompress(base64.b64decode(clean))


def localise(html_bytes, name):
    html = html_bytes.decode("utf-8")
    for fn, origin in IMAGES.items():
        html = html.replace(WESERV + origin, fn)
    left = html.count("images.weserv.nl")
    if left:
        print("  WARNING: %d CDN image refs left in %s" % (left, name))
    return html


def main():
    os.makedirs(OUT, exist_ok=True)

    print("== pages ==")
    for name, path, patches, expect in PAGES:
        raw = decode_payload(path, patches)
        got = md5(raw)
        if got != expect:
            sys.exit("CHECKSUM MISMATCH on %s: got %s, expected %s - aborting" % (name, got, expect))
        html = localise(raw, name).encode("utf-8")
        if name == "index.html" and md5(html) != EXPECTED_LOCAL_INDEX:
            sys.exit("post-swap checksum mismatch on index.html - aborting")
        open(os.path.join(OUT, name), "wb").write(html)
        print("  %-24s md5 %s OK" % (name, got))

    raw = fetch(RAW + "/post-launch/index.html")
    html = localise(raw, "index-post-launch.html").encode("utf-8")
    open(os.path.join(OUT, "index-post-launch.html"), "wb").write(html)
    print("  %-24s md5 %s (local refs: %s)" % ("index-post-launch.html", md5(raw), md5(html)))

    print("== images ==")
    for fn, origin in IMAGES.items():
        data = None
        for url in ("https://" + origin, WESERV + origin):
            try:
                req = urllib.request.Request(url, headers=UA)
                with urllib.request.urlopen(req, timeout=180) as r:
                    data = r.read()
                if data:
                    break
            except Exception:
                time.sleep(2)
        if not data:
            sys.exit("image download failed: " + fn)
        open(os.path.join(OUT, fn), "wb").write(data)
        print("  %-24s %d bytes" % (fn, len(data)))

    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "DEPLOYMENT-README.md")
    if os.path.exists(src):
        with open(src, "rb") as f:
            open(os.path.join(OUT, "DEPLOYMENT-README.md"), "wb").write(f.read())

    with zipfile.ZipFile(ZIPNAME, "w", zipfile.ZIP_DEFLATED) as z:
        for fn in sorted(os.listdir(OUT)):
            z.write(os.path.join(OUT, fn), fn)

    print("== done ==")
    print("package folder: %s/" % OUT)
    print("package zip:    %s" % ZIPNAME)
    print("next step: see DEPLOYMENT-README.md")


if __name__ == "__main__":
    main()
