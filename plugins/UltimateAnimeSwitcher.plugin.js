/**
 * @name UltimateAnimeSwitcher
 * @author VanillyNeko
 * @version 2.0.0
 * @description Pick your Ultimate Anime Discord Theme character from a dropdown. Needs the character .theme.css files from the repo's themes folder in your themes folder.
 * @donate https://paypal.me/vanillyneko
 * @website https://www.vanillyneko.com/
 * @invite bptEdGMNfW
 * @source https://github.com/VanillyNeko/Anya-bd
 */

const THEME_PREFIX = "Ultimate Anime - ";
const SERIES_PATTERN = /^(.*) \(([^()]+)\)$/;

module.exports = class UltimateAnimeSwitcher {
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
      panel.textContent = "No Ultimate Anime characters installed. Copy .theme.css files from the repo's themes folder into your BetterDiscord themes folder.";
      return panel;
    }

    const bySeries = new Map();
    for (const theme of themes) {
      const label = theme.name.slice(THEME_PREFIX.length);
      const [, character = label, series = "Other"] = label.match(SERIES_PATTERN) ?? [];
      if (!bySeries.has(series)) bySeries.set(series, []);
      bySeries.get(series).push({ character, theme });
    }

    const select = document.createElement("select");
    select.style.cssText =
      "padding: 8px; border-radius: 8px; border: 1px solid var(--border-subtle); background: var(--input-background-default); color: var(--text-default);";
    select.add(new Option("Off", ""));
    for (const series of [...bySeries.keys()].sort()) {
      const group = document.createElement("optgroup");
      group.label = series;
      for (const { character, theme } of bySeries.get(series).sort((a, b) => a.character.localeCompare(b.character))) {
        const enabled = BdApi.Themes.isEnabled(theme.id);
        group.append(new Option(character, theme.id, enabled, enabled));
      }
      select.append(group);
    }
    select.addEventListener("change", () => this.activate(select.value));

    const label = document.createElement("label");
    label.style.cssText = "display: flex; flex-direction: column; gap: 6px;";
    label.append("Character", select);
    panel.append(label);
    return panel;
  }
};
