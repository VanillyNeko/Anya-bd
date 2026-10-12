# Anya Better Discord Theme
 A Spy x Family theme for Discord, starring Anya, with Yor, Loid and Bond as alternate characters.
 It is 100% self reliant: fonts and images are hosted in this repo, so nobody can change them out from under you.

 Anya BD works on [BetterDiscord](https://betterdiscord.app/), [Vencord](https://vencord.dev/), [Vesktop](https://github.com/Vencord/Vesktop) and [Replugged](https://replugged.dev/). Will be adding Aliucord later on down the line!

 I welcome forks and stuff but be warned, if discord updates their stuff and you don't pull changes then you may lose the ability to use it.
 I will be updating this theme when discord breaks it.

## Picking a character

 **BetterDiscord, Vencord, Replugged:** download the theme files from [`themes/`](themes/) into your themes folder, then turn on the one you want in the Themes tab. Only turn on one Anya-BD theme at a time.

 **BetterDiscord dropdown:** also install [`plugins/AnyaThemeSwitcher.plugin.js`](plugins/AnyaThemeSwitcher.plugin.js) and pick a character from its settings.

 **Vencord and Vesktop online themes:** add one of these links in Themes > Online Themes:
 - `https://vanillyneko.github.io/Anya-bd/themes/Anya.theme.css`
 - `https://vanillyneko.github.io/Anya-bd/themes/Yor.theme.css`
 - `https://vanillyneko.github.io/Anya-bd/themes/Loid.theme.css`
 - `https://vanillyneko.github.io/Anya-bd/themes/Bond.theme.css`

 **Quick CSS:** paste these two lines and change `anya` to the character you want:
 ```css
 @import url("https://vanillyneko.github.io/Anya-bd/core.css");
 @import url("https://vanillyneko.github.io/Anya-bd/characters/anya.css");
 ```

## Tweaking

 Put overrides after the imports. The knobs are listed at the top of [`core.css`](core.css), for example:
 ```css
 :root {
   --anya-bd-glass-strength: 60%;  /* darker panels */
   --anya-bd-bubble-strength: 0%;  /* no message bubbles */
   --anya-bd-font-body: "gg sans"; /* Discord's normal font for message text */
 }
 ```

## Adding a character

 1. Copy [`characters/anya.css`](characters/anya.css) to `characters/<name>.css` and change the colors.
 2. Put art in `assets/characters/<name>/` and point `--anya-bd-background-image` and `--anya-bd-home-icon` at its `https://vanillyneko.github.io/Anya-bd/...` URL.
    Images from other sites get blocked by Vencord, so keep them in this repo.
 3. Copy [`themes/Anya.theme.css`](themes/Anya.theme.css) to `themes/<Name>.theme.css` and change the `@name` (keep the `Anya-BD` prefix so the switcher plugin finds it) and the character import.

## Screenshots

 Friends Page:
 ![Friends Page](https://vanillyneko.github.io/Anya-bd/assets/screenshots/friends-page.png)

 Settings Page:
 ![Settings Page](https://vanillyneko.github.io/Anya-bd/assets/screenshots/settings.png)

 Server Announcements:
 ![Server Announcements Neko Family Server](https://vanillyneko.github.io/Anya-bd/assets/screenshots/discord-announcements.png)
