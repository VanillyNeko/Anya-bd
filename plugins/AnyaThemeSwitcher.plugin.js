/**
 * @name AnyaThemeSwitcher
 * @author VanillyNeko
 * @version 1.0.0
 * @description Pick your Anya-BD character from a dropdown. Needs the Anya-BD theme files from the repo's themes folder in your themes folder.
 * @donate https://paypal.me/vanillyneko
 * @website https://www.vanillyneko.com/
 * @invite bptEdGMNfW
 * @source https://github.com/VanillyNeko/Anya-bd
 */

const THEME_PREFIX = "Anya-BD";

module.exports = class AnyaThemeSwitcher {
  start() {}
  stop() {}

  getCharacterThemes() {
    return BdApi.Themes.getAll().filter((theme) => theme.name?.startsWith(THEME_PREFIX));
  }

  activate(id) {
    for (const theme of this.getCharacterThemes()) {
      if (theme.id === id) BdApi.Themes.enable(theme.id);
      else if (BdApi.Themes.isEnabled(theme.id)) BdApi.Themes.disable(theme.id);
    }
  }

  getSettingsPanel() {
    const panel = document.createElement("div");
    panel.style.cssText = "display: flex; flex-direction: column; gap: 8px; color: var(--text-default);";

    const themes = this.getCharacterThemes();
    if (!themes.length) {
      panel.textContent = "No Anya-BD themes installed. Copy the .theme.css files from the repo's themes folder into your BetterDiscord themes folder.";
      return panel;
    }

    const label = document.createElement("label");
    label.textContent = "Character";

    const select = document.createElement("select");
    select.style.cssText =
      "padding: 8px; border-radius: 8px; border: 1px solid var(--border-subtle); background: var(--input-background-default); color: var(--text-default);";
    select.add(new Option("Off", ""));
    for (const theme of themes) {
      const character = theme.name.slice(THEME_PREFIX.length).trim() || "Anya (classic)";
      const enabled = BdApi.Themes.isEnabled(theme.id);
      select.add(new Option(character, theme.id, enabled, enabled));
    }
    select.addEventListener("change", () => this.activate(select.value));

    label.append(select);
    label.style.cssText = "display: flex; flex-direction: column; gap: 6px;";
    panel.append(label);
    return panel;
  }
};
