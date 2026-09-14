#!/usr/bin/env python3
"""
Pull cover images for the six TikTok videos straight from TikTok's public
oEmbed endpoint, and save them into assets/videos/.

Run it whenever you swap a video out:

    python3 scripts/fetch-thumbnails.py

Edit VIDS below to match the cards in index.html. The number is the card
position (1-6), so card 3 gets assets/videos/video-3.jpg.

The thumbnail URLs TikTok hands back are signed and expire, which is why
this downloads the files rather than linking to them.
"""
import json, os, urllib.request

DEST = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                    "assets", "videos")
UA = {"User-Agent": ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                     "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120 Safari/537.36")}

HANDLE = "talishagrobler"

VIDS = [
    (1, "Hisense",          "7681315116561861909"),
    (2, "Nails by Kriston", "7628630760215465236"),
    (3, "Nivea",            "7644617608817282325"),
    (4, "Garnier",          "7572256756525567240"),
    (5, "Darry Ring",       "7471207367858785541"),
    (6, "CellConnect ZA",   "7677642153060781332"),
]


def fetch(n, brand, video_id):
    oembed = (f"https://www.tiktok.com/oembed?url="
              f"https://www.tiktok.com/@{HANDLE}/video/{video_id}")
    meta = json.load(urllib.request.urlopen(
        urllib.request.Request(oembed, headers=UA), timeout=25))

    url = meta.get("thumbnail_url")
    if not url:
        raise RuntimeError("no thumbnail_url in the oEmbed response")

    data = urllib.request.urlopen(
        urllib.request.Request(url, headers=UA), timeout=45).read()

    if data[:3] != b"\xff\xd8\xff":
        raise RuntimeError(f"not a JPEG (starts {data[:12]!r})")

    path = os.path.join(DEST, f"video-{n}.jpg")
    with open(path, "wb") as fh:
        fh.write(data)
    return path, len(data), (meta.get("title") or "").strip()


def main():
    os.makedirs(DEST, exist_ok=True)
    failures = 0
    for n, brand, video_id in VIDS:
        try:
            path, size, title = fetch(n, brand, video_id)
            print(f"ok   video-{n}.jpg  {size:>8,}b  {brand:<17} | {title[:48]}")
        except Exception as exc:
            failures += 1
            print(f"FAIL video-{n}.jpg  {brand:<17} | {exc}")
    if failures:
        print(f"\n{failures} failed. A deleted or private video has no "
              f"thumbnail, so check the link still opens.")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
