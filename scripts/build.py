#!/usr/bin/env python3
"""Generate characters/, themes/ and CHARACTERS.md from roster.json.

Run from anywhere: python3 scripts/build.py
characters/ and themes/ are wiped and rebuilt on every run, so edit roster.json, never the generated files.

Art is picked up automatically from assets/characters/<series>/<character>/:
  background.(jpg|jpeg|png|webp|gif)  full-window backdrop
  home-icon.(gif|png|jpg|jpeg|webp)   replaces Discord's logo on the home button
A character can also point "background" / "homeIcon" at any other repo path.
"""

import json
import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BASE_URL = "https://vanillyneko.github.io/Anya-bd/"
THEME_PREFIX = "Ultimate Anime - "
IMAGE_EXTS = ("jpg", "jpeg", "png", "webp", "gif")
HEX = re.compile(r"^#[0-9a-fA-F]{6}$")
SLUG = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
GENERATED_NOTE = "Generated from roster.json by scripts/build.py - edit roster.json instead."

META = """\
 * @author VanillyNeko
 * @version {version}
 * @description The Ultimate Anime Discord Theme: {name} from {series}. Enable only one Ultimate Anime character at a time.
 * @donate https://paypal.me/vanillyneko
 * @website https://www.vanillyneko.com/
 * @invite bptEdGMNfW
 * @source https://github.com/VanillyNeko/Anya-bd"""


def fail(message):
    sys.exit(f"roster.json: {message}")


def find_asset(folder, stem):
    for ext in IMAGE_EXTS:
        path = folder / f"{stem}.{ext}"
        if path.is_file():
            return path.relative_to(ROOT).as_posix()
    return None


def url(repo_path):
    if not (ROOT / repo_path).is_file():
        fail(f"{repo_path} does not exist")
    return f"url({BASE_URL}{repo_path})"


def character_css(series, char, styles):
    art = ROOT / "assets" / "characters" / series["id"] / char["id"]
    background = char.get("background") or find_asset(art, "background")
    home_icon = char.get("homeIcon") or find_asset(art, "home-icon")

    lines = [
        f"/* {char['name']} - {series['name']} */",
        f"/* {GENERATED_NOTE} */",
        ":root {",
        f"  --uadt-background-image: {url(background) if background else 'none'};",
        f"  --uadt-home-icon: {url(home_icon) if home_icon else 'none'};",
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
    return "\n".join(lines) + "\n", bool(background)


def theme_css(series, char, version):
    meta = META.format(version=version, name=char["name"], series=series["name"])
    return (
        f"/**\n * @name {THEME_PREFIX}{char['name']} ({series['name']})\n{meta}\n */\n\n"
        f'@import url("{BASE_URL}core.css");\n'
        f'@import url("{BASE_URL}characters/{series["id"]}/{char["id"]}.css");\n'
    )


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
    validate(roster)

    for folder in ("characters", "themes"):
        shutil.rmtree(ROOT / folder, ignore_errors=True)

    listing = [
        "# Characters",
        "",
        f"<!-- {GENERATED_NOTE} -->",
        "",
        "Add a theme link under Themes > Online Themes in Vencord or Vesktop, or download the file into your BetterDiscord / Vencord themes folder.",
        "Characters marked with art have a background image; the rest use a gradient in their colors until art is added.",
        "",
    ]
    total = with_art = 0

    for category in dict.fromkeys(s["category"] for s in roster["series"]):
        listing += [f"## {category}", ""]
        for series in (s for s in roster["series"] if s["category"] == category):
            listing += [f"### {series['name']}", ""]
            for char in series["characters"]:
                css, has_art = character_css(series, char, roster["styles"])
                char_path = ROOT / "characters" / series["id"] / f"{char['id']}.css"
                theme_path = ROOT / "themes" / series["id"] / f"{char['id']}.theme.css"
                for path, content in ((char_path, css), (theme_path, theme_css(series, char, roster["version"]))):
                    path.parent.mkdir(parents=True, exist_ok=True)
                    path.write_text(content, encoding="utf-8")

                theme_rel = theme_path.relative_to(ROOT).as_posix()
                art = " (art)" if has_art else ""
                listing.append(f"- **{char['name']}**{art}: [`{theme_rel}`]({theme_rel}) - `{BASE_URL}{theme_rel}`")
                total += 1
                with_art += has_art
            listing.append("")

    (ROOT / "CHARACTERS.md").write_text("\n".join(listing), encoding="utf-8")
    print(f"Built {total} characters in {len(roster['series'])} series ({with_art} with art).")


if __name__ == "__main__":
    main()
