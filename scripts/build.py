#!/usr/bin/env python3
"""Generate characters/, themes/, CHARACTERS.md and gallery.html from roster.json and art.json.

Run from anywhere: python3 scripts/build.py
characters/ and themes/ are wiped and rebuilt on every run, so edit roster.json, never the generated files.

Art for each character comes from the first of these that exists:
  1. "background" / "homeIcon" in roster.json (a repo path or an allowed URL)
  2. files in assets/characters/<series>/<character>/:
       background.(jpg|jpeg|png|webp|gif)  full-window backdrop
       home-icon.(gif|png|jpg|jpeg|webp)   replaces Discord's logo on the home button
  3. art.json, filled in by scripts/fetch_art.py
"""

import html
import json
import re
import shutil
import sys
import urllib.parse
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BASE_URL = "https://vanillyneko.github.io/The-Best-Anime-Discord-Theme/"
THEME_PREFIX = "Ultimate Anime - "
IMAGE_EXTS = ("jpg", "jpeg", "png", "webp", "gif")
HEX = re.compile(r"^#[0-9a-fA-F]{6}$")
SLUG = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
GENERATED_NOTE = "Generated from roster.json by scripts/build.py - edit roster.json instead."

# Vencord and Vesktop only load images from an allowlist of hosts; anything else silently fails.
ALLOWED_HOST_SUFFIXES = (".tenor.com", ".giphy.com", ".github.io")
ALLOWED_HOSTS = ("i.imgur.com",)

META = """\
 * @author VanillyNeko
 * @version {version}
 * @description The Ultimate Anime Discord Theme: {name} from {series}. Enable only one Ultimate Anime character at a time.
 * @donate https://paypal.me/vanillyneko
 * @website https://www.vanillyneko.com/
 * @invite bptEdGMNfW
 * @source https://github.com/VanillyNeko/The-Best-Anime-Discord-Theme"""


def fail(message):
    sys.exit(f"build: {message}")


def find_asset(folder, stem):
    for ext in IMAGE_EXTS:
        path = folder / f"{stem}.{ext}"
        if path.is_file():
            return path.relative_to(ROOT).as_posix()
    return None


def resolve(location):
    """Turn a repo path or URL into an absolute URL Vencord will load."""
    if re.match(r"^https?://", location):
        host = urllib.parse.urlparse(location).hostname or ""
        if not (host in ALLOWED_HOSTS or host.endswith(ALLOWED_HOST_SUFFIXES)):
            fail(f"{location} is not on a host Vencord allows ({', '.join(ALLOWED_HOSTS + ALLOWED_HOST_SUFFIXES)})")
        return location
    if not (ROOT / location).is_file():
        fail(f"{location} does not exist")
    return BASE_URL + location


def character_art(series, char, art):
    folder = ROOT / "assets" / "characters" / series["id"] / char["id"]
    picked = art.get(char["id"], {})
    background = char.get("background") or find_asset(folder, "background") or picked.get("background")
    home_icon = char.get("homeIcon") or find_asset(folder, "home-icon") or picked.get("homeIcon") or background
    sources = {
        "background": picked.get("backgroundSource") if background == picked.get("background") else None,
        "home icon": picked.get("homeIconSource") if home_icon == picked.get("homeIcon") else None,
    }
    return (resolve(background) if background else None,
            resolve(home_icon) if home_icon else None,
            {label: link for label, link in sources.items() if link})


def character_css(series, char, styles, background, home_icon):
    lines = [
        f"/* {char['name']} - {series['name']} */",
        f"/* {GENERATED_NOTE} */",
        ":root {",
        f"  --uadt-background-image: {f'url({background})' if background else 'none'};",
        f"  --uadt-home-icon: {f'url({home_icon})' if home_icon else 'none'};",
        f"  --uadt-home-logo: {'hidden' if home_icon else 'visible'};",
        "",
        f"  --uadt-accent: {char['accent']};",
        f"  --uadt-accent-alt: {char['alt']};",
    ]
    for key, prop in (("tint", "tint"), ("text", "text"), ("textStrong", "text-strong"),
                      ("textMuted", "text-muted"), ("link", "link")):
        if key in char:
            lines.append(f"  --uadt-{prop}: {char[key]};")

    style = styles[char.get("style", "cute")]
    lines += [
        "",
        f'  --uadt-font-body: "{style["body"]}";',
        f'  --uadt-font-heading: "{style["heading"]}";',
        f'  --uadt-font-button: "{style["button"]}";',
        "}",
    ]
    return "\n".join(lines) + "\n"


def theme_css(series, char, version):
    meta = META.format(version=version, name=char["name"], series=series["name"])
    return (
        f"/**\n * @name {THEME_PREFIX}{char['name']} ({series['name']})\n{meta}\n */\n\n"
        f'@import url("{BASE_URL}core.css");\n'
        f'@import url("{BASE_URL}characters/{series["id"]}/{char["id"]}.css");\n'
    )


def gallery_card(series, char, background, home_icon, theme_rel):
    e = html.escape
    tint = char.get("tint", "#0c0a10")
    images = ""
    if background:
        images += f'<img class="bg" loading="lazy" src="{e(background)}" alt="">'
    if home_icon:
        images += f'<img class="icon" loading="lazy" src="{e(home_icon)}" alt="">'
    return (
        f'<article style="--accent:{char["accent"]};--alt:{char["alt"]};--tint:{tint}">'
        f'<div class="art">{images}</div>'
        f'<h3>{e(char["name"])}</h3>'
        f'<p><span class="swatch" style="background:{char["accent"]}"></span>'
        f'<span class="swatch" style="background:{char["alt"]}"></span>'
        f'<code>{e(char["id"])}</code></p>'
        f'<input readonly value="{e(BASE_URL + theme_rel)}" onclick="this.select()">'
        f'</article>'
    )


GALLERY_PAGE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>The Ultimate Anime Discord Theme - Characters</title>
<!-- {note} -->
<style>
  body {{ margin: 0; padding: 24px; background: #0c0a10; color: #eee; font: 15px/1.4 system-ui, sans-serif; }}
  h1 {{ margin-top: 0; }}
  h2 {{ margin: 32px 0 12px; border-bottom: 1px solid #333; padding-bottom: 6px; }}
  .grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(240px, 1fr)); gap: 16px; }}
  article {{ background: color-mix(in srgb, var(--accent) 12%, #16131c); border: 1px solid color-mix(in srgb, var(--accent) 35%, transparent); border-radius: 12px; overflow: hidden; }}
  .art {{ position: relative; aspect-ratio: 16 / 9; background: radial-gradient(circle at 15% 10%, color-mix(in srgb, var(--accent) 45%, transparent), transparent 55%), radial-gradient(circle at 85% 90%, color-mix(in srgb, var(--alt) 40%, transparent), transparent 55%), color-mix(in srgb, var(--accent) 16%, #0c0a10); }}
  .bg {{ width: 100%; height: 100%; object-fit: cover; display: block; }}
  .icon {{ position: absolute; left: 10px; bottom: 10px; width: 48px; height: 48px; object-fit: cover; border-radius: 16px; border: 2px solid var(--accent); background: #000; }}
  h3 {{ margin: 10px 12px 4px; font-size: 16px; color: color-mix(in srgb, var(--accent) 30%, white); }}
  p {{ margin: 0 12px 8px; display: flex; gap: 6px; align-items: center; }}
  .swatch {{ width: 16px; height: 16px; border-radius: 4px; display: inline-block; }}
  code {{ opacity: .6; font-size: 12px; }}
  input {{ width: calc(100% - 24px); margin: 0 12px 12px; padding: 6px; border-radius: 6px; border: 1px solid #333; background: #0006; color: #ccc; font-size: 11px; }}
</style>
</head>
<body>
<h1>The Ultimate Anime Discord Theme</h1>
<p>{total} characters. Click a link to select it, then paste it under Themes &gt; Online Themes in Vencord or Vesktop. Animated art is hotlinked from Tenor.</p>
{sections}
</body>
</html>
"""


def validate(roster):
    styles = roster["styles"]
    seen_series, seen_chars = set(), {}
    for series in roster["series"]:
        if not SLUG.match(series["id"]) or series["id"] in seen_series:
            fail(f"series id {series['id']!r} is invalid or duplicated")
        seen_series.add(series["id"])
        for char in series["characters"]:
            where = f"{series['id']}/{char.get('id')}"
            if not SLUG.match(char.get("id", "")):
                fail(f"{where}: id must be lowercase-with-dashes")
            if char["id"] in seen_chars:
                fail(f"{where}: id also used in {seen_chars[char['id']]}; theme files share one folder, so ids must be unique")
            seen_chars[char["id"]] = series["id"]
            for key in ("accent", "alt", "tint", "text", "textStrong", "textMuted", "link"):
                if key in char and not HEX.match(char[key]):
                    fail(f"{where}: {key} must be a #rrggbb color")
            if char.get("style", "cute") not in styles:
                fail(f"{where}: unknown style {char['style']!r}")


def main():
    roster = json.loads((ROOT / "roster.json").read_text(encoding="utf-8"))
    art_file = ROOT / "art.json"
    art = json.loads(art_file.read_text(encoding="utf-8")) if art_file.exists() else {}
    validate(roster)

    for folder in ("characters", "themes"):
        shutil.rmtree(ROOT / folder, ignore_errors=True)

    listing = [
        "# Characters",
        "",
        f"<!-- {GENERATED_NOTE} -->",
        "",
        f"See them all with their art in the [gallery]({BASE_URL}gallery.html).",
        "Add a theme link under Themes > Online Themes in Vencord or Vesktop, or download the file into your BetterDiscord / Vencord themes folder.",
        "Characters without art use a gradient in their colors. Animated art is hotlinked from Tenor; the source links credit the uploaders.",
        "",
    ]
    sections = []
    total = with_background = with_icon = 0
    no_art = []

    for category in dict.fromkeys(s["category"] for s in roster["series"]):
        listing += [f"## {category}", ""]
        for series in (s for s in roster["series"] if s["category"] == category):
            listing += [f"### {series['name']}", ""]
            cards = []
            for char in series["characters"]:
                background, home_icon, sources = character_art(series, char, art)
                char_path = ROOT / "characters" / series["id"] / f"{char['id']}.css"
                theme_path = ROOT / "themes" / series["id"] / f"{char['id']}.theme.css"
                for path, content in ((char_path, character_css(series, char, roster["styles"], background, home_icon)),
                                      (theme_path, theme_css(series, char, roster["version"]))):
                    path.parent.mkdir(parents=True, exist_ok=True)
                    path.write_text(content, encoding="utf-8")

                theme_rel = theme_path.relative_to(ROOT).as_posix()
                credits = ", ".join(f"[{label}]({link})" for label, link in sources.items())
                credits = f" (art: {credits})" if credits else ""
                listing.append(f"- **{char['name']}**: [`{theme_rel}`]({theme_rel}) - `{BASE_URL}{theme_rel}`{credits}")
                cards.append(gallery_card(series, char, background, home_icon, theme_rel))

                total += 1
                with_background += bool(background)
                with_icon += bool(home_icon)
                if not background and not home_icon:
                    no_art.append(char["id"])
            listing.append("")
            sections.append(f'<h2>{html.escape(series["name"])}</h2>\n<div class="grid">{"".join(cards)}</div>')

    (ROOT / "CHARACTERS.md").write_text("\n".join(listing), encoding="utf-8")
    (ROOT / "gallery.html").write_text(
        GALLERY_PAGE.format(note=GENERATED_NOTE, total=total, sections="\n".join(sections)), encoding="utf-8")

    print(f"Built {total} characters in {len(roster['series'])} series: "
          f"{with_background} with a background, {with_icon} with a home icon.")
    if no_art:
        print("No art yet: " + ", ".join(no_art))


if __name__ == "__main__":
    main()
