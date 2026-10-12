# The Ultimate Anime Discord Theme
 A see-through anime theme for Discord with 179 characters from 30 series: the big gacha games, popular anime, and some highly rated niche picks.
 Each character gets their own colors, fonts and (where added) art. See [CHARACTERS.md](CHARACTERS.md) for the full list.

 It is 100% self reliant: fonts and images are hosted in this repo, so nobody can change them out from under you.

 Works on [BetterDiscord](https://betterdiscord.app/), [Vencord](https://vencord.dev/), [Vesktop](https://github.com/Vencord/Vesktop) and [Replugged](https://replugged.dev/).

 I welcome forks and stuff but be warned, if discord updates their stuff and you don't pull changes then you may lose the ability to use it.
 I will be updating this theme when discord breaks it.

## Picking a character

 Browse everyone with their art in the [gallery](https://vanillyneko.github.io/Anya-bd/gallery.html) or the list in [CHARACTERS.md](CHARACTERS.md), then either:

 - **Vencord / Vesktop:** paste the character's link into Themes > Online Themes, or download its `.theme.css` into your themes folder and turn it on in the Themes tab.
 - **BetterDiscord:** download the `.theme.css` files you want into your themes folder and turn one on. Install [`plugins/UltimateAnimeSwitcher.plugin.js`](plugins/UltimateAnimeSwitcher.plugin.js) to switch between them from a dropdown in its settings.
 - **Quick CSS:** paste these two lines and swap the second for any file in [`characters/`](characters/):
   ```css
   @import url("https://vanillyneko.github.io/Anya-bd/core.css");
   @import url("https://vanillyneko.github.io/Anya-bd/characters/spy-x-family/anya-forger.css");
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

## Screenshots

 Friends Page:
 ![Friends Page](https://vanillyneko.github.io/Anya-bd/assets/screenshots/friends-page.png)

 Settings Page:
 ![Settings Page](https://vanillyneko.github.io/Anya-bd/assets/screenshots/settings.png)

 Server Announcements:
 ![Server Announcements Neko Family Server](https://vanillyneko.github.io/Anya-bd/assets/screenshots/discord-announcements.png)
