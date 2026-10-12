# The Ultimate Anime Discord Theme
 A see-through anime theme for Discord with 179 characters from 30 series: the big gacha games, popular anime, and some highly rated niche picks.
 Each character gets their own colors, fonts and (where added) art. See [CHARACTERS.md](CHARACTERS.md) for the full list.

 It is 100% self reliant: fonts and images are hosted in this repo, so nobody can change them out from under you.

 Works on [BetterDiscord](https://betterdiscord.app/), [Vencord](https://vencord.dev/), [Vesktop](https://github.com/Vencord/Vesktop) and [Replugged](https://replugged.dev/).

 I welcome forks and stuff but be warned, if discord updates their stuff and you don't pull changes then you may lose the ability to use it.
 I will be updating this theme when discord breaks it.

## Download

 Grab the zip from the [latest release](https://github.com/VanillyNeko/The-Best-Anime-Discord-Theme/releases/latest), unzip it, and run `install.bat` (Windows) or `./install.sh` (Linux / macOS).
 It copies every character into Vencord, Vesktop and BetterDiscord (whichever you have), plus the character switcher plugin for BetterDiscord.
 Then open Discord settings > Themes and turn on one character.

## Picking a character

 Rather pick just one? Browse everyone with their art in the [gallery](https://vanillyneko.github.io/The-Best-Anime-Discord-Theme/gallery.html) or the list in [CHARACTERS.md](CHARACTERS.md), then either:

 - **Vencord / Vesktop:** paste the character's link into Themes > Online Themes, or download its `.theme.css` into your themes folder and turn it on in the Themes tab.
 - **BetterDiscord:** download the `.theme.css` files you want into your themes folder and turn one on. Install [`plugins/UltimateAnimeSwitcher.plugin.js`](plugins/UltimateAnimeSwitcher.plugin.js) to switch between them from a dropdown in its settings.
 - **Quick CSS:** paste these two lines and swap the second for any file in [`characters/`](characters/):
   ```css
   @import url("https://vanillyneko.github.io/The-Best-Anime-Discord-Theme/core.css");
   @import url("https://vanillyneko.github.io/The-Best-Anime-Discord-Theme/characters/spy-x-family/anya-forger.css");
   ```

 Only turn on one character at a time.

## Tweaking

 Put overrides after the theme (or in Quick CSS / Custom CSS). The knobs are listed at the top of [`core.css`](core.css), for example:
 ```css
 :root {
   --uadt-backdrop-dim: 70%;    /* darker background art */
   --uadt-glass-strength: 60%;  /* darker panels */
   --uadt-bubble-strength: 0%;  /* no message bubbles */
   --uadt-font-body: "gg sans"; /* Discord's normal font for message text */
 }
 ```

## Adding characters and art

 Everything in `characters/`, `themes/`, `CHARACTERS.md` and `gallery.html` is generated, so edit [`roster.json`](roster.json) and rebuild:
 ```sh
 python3 scripts/fetch_art.py   # pick animated art from Tenor for characters without locked art
 python3 scripts/build.py       # regenerate everything
 ```

 - **New character:** add an entry with an `id` (lowercase-with-dashes, unique across all series), `name`, `accent` and `alt` colors. Optional: `tint`, `text`, `textStrong`, `textMuted`, `link`, and `style` (`cute`, `clean` or `bold` fonts).
   Then run `python3 scripts/fetch_art.py <id>` to pick its art.
 - **Animated art:** `fetch_art.py` searches Tenor for clips of the character, skips anything tagged as AI-made, and saves the picks to [`art.json`](art.json). Check them in `gallery.html`.
   Don't like a pick? Paste a different Tenor GIF's media link into `art.json` and set `"locked": true` so the script never replaces it, or rerun the script for just that character.
 - **Your own art:** drop `background.jpg` (or png/webp/gif) and/or `home-icon.gif` (or png/jpg/webp) into `assets/characters/<series-id>/<character-id>/`. Files there always win over `art.json`.
   Images must come from this repo, Tenor, Giphy or Imgur: Vencord blocks every other site.

## Releasing

 Bump `version` in [`roster.json`](roster.json), run `python3 scripts/build.py`, commit and push, then tag that version:
 ```sh
 git tag v6.0.0
 git push origin v6.0.0
 ```
 GitHub Actions checks the generated files are up to date, packs the kit with `scripts/package.py` and publishes it as a release.
 Run `python3 scripts/package.py` yourself to get the same zip in `dist/`.

## Screenshots

 Friends Page:
 ![Friends Page](https://vanillyneko.github.io/The-Best-Anime-Discord-Theme/assets/screenshots/friends-page.png)

 Settings Page:
 ![Settings Page](https://vanillyneko.github.io/The-Best-Anime-Discord-Theme/assets/screenshots/settings.png)

 Server Announcements:
 ![Server Announcements Neko Family Server](https://vanillyneko.github.io/The-Best-Anime-Discord-Theme/assets/screenshots/discord-announcements.png)
