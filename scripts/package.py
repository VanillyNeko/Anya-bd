#!/usr/bin/env python3
"""Pack the release kit: one zip with every theme, the BetterDiscord plugin and installers.

Run after build.py: python3 scripts/package.py
Writes dist/The-Best-Anime-Discord-Theme-v<version>.zip and dist/RELEASE_NOTES.md.
Installer templates live in release/.
"""

import json
import shutil
import sys
import zipfile
from pathlib import Path

from build import BASE_URL, ROOT

NAME = "The-Best-Anime-Discord-Theme"
DIST = ROOT / "dist"
# Windows tools choke on LF-only batch files, so these ship with CRLF line endings.
CRLF_SUFFIXES = (".bat", ".ps1", ".txt")


def fail(message):
    sys.exit(f"package: {message}")


def add_text(kit, arcname, text, executable=False):
    if arcname.endswith(CRLF_SUFFIXES):
        text = text.replace("\r\n", "\n").replace("\n", "\r\n")
    info = zipfile.ZipInfo(f"{NAME}/{arcname}", date_time=(2026, 1, 1, 0, 0, 0))
    info.compress_type = zipfile.ZIP_DEFLATED
    info.external_attr = (0o755 if executable else 0o644) << 16
    kit.writestr(info, text)


def main():
    roster = json.loads((ROOT / "roster.json").read_text(encoding="utf-8"))
    version = roster["version"]
    series_count = len(roster["series"])
    ids = [char["id"] for series in roster["series"] for char in series["characters"]]

    themes = sorted((ROOT / "themes").glob("*/*.theme.css"))
    if sorted(path.name for path in themes) != sorted(f"{char_id}.theme.css" for char_id in ids):
        fail("themes/ doesn't match roster.json; run python3 scripts/build.py first")

    shutil.rmtree(DIST, ignore_errors=True)
    DIST.mkdir()
    zip_path = DIST / f"{NAME}-v{version}.zip"
    release = ROOT / "release"
    fill = {"version": f"v{version}", "total": len(ids), "series": series_count, "base_url": BASE_URL}

    with zipfile.ZipFile(zip_path, "w") as kit:
        add_text(kit, "INSTALL.txt", (release / "INSTALL.txt").read_text(encoding="utf-8").format(**fill))
        add_text(kit, "install.sh", (release / "install.sh").read_text(encoding="utf-8"), executable=True)
        add_text(kit, "install.ps1", (release / "install.ps1").read_text(encoding="utf-8"))
        add_text(kit, "install.bat", (release / "install.bat").read_text(encoding="utf-8"))
        add_text(kit, "CHARACTERS.md", (ROOT / "CHARACTERS.md").read_text(encoding="utf-8"))
        add_text(kit, "plugins/UltimateAnimeSwitcher.plugin.js",
                 (ROOT / "plugins" / "UltimateAnimeSwitcher.plugin.js").read_text(encoding="utf-8"))
        # Client mods only look at the top level of their themes folder, so the kit ships them flat.
        for theme in themes:
            add_text(kit, f"themes/{theme.name}", theme.read_text(encoding="utf-8"))

    (DIST / "RELEASE_NOTES.md").write_text(
        f"{len(ids)} characters from {series_count} series.\n\n"
        f"**Download `{zip_path.name}`** below, unzip it, then run `install.bat` (Windows) or `./install.sh` "
        "(Linux / macOS). It copies every character into Vencord, Vesktop and BetterDiscord, whichever you have. "
        "Then open Discord settings > Themes and turn on one character.\n\n"
        f"Browse the characters in the [gallery]({BASE_URL}gallery.html). "
        "Prefer not to download anything? Paste a character's link from "
        "[CHARACTERS.md](https://github.com/VanillyNeko/The-Best-Anime-Discord-Theme/blob/main/CHARACTERS.md) "
        "into Themes > Online Themes in Vencord or Vesktop.\n",
        encoding="utf-8")

    print(f"Packed {len(themes)} themes into {zip_path.relative_to(ROOT)} "
          f"({zip_path.stat().st_size // 1024} KB)")


if __name__ == "__main__":
    main()
