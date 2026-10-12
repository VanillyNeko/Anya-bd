#!/bin/sh
# Copies every Ultimate Anime theme into each Discord client mod found on this computer.
# Usage: ./install.sh            install into Vencord, Vesktop and BetterDiscord, whichever exist
#        ./install.sh <folder>   install into a themes folder of your choice
set -eu

here=$(cd "$(dirname "$0")" && pwd)
count=$(find "$here/themes" -name '*.theme.css' | wc -l | tr -d ' ')
found=0

copy_themes() { # $1 = client name, $2 = themes folder
  mkdir -p "$2"
  cp "$here"/themes/*.theme.css "$2/"
  echo "Installed $count themes for $1: $2"
  found=1
}

install_client() { # $1 = client name, $2 = the client's settings folder
  [ -d "$2" ] || return 0
  copy_themes "$1" "$2/themes"
  if [ "$1" = "BetterDiscord" ]; then
    mkdir -p "$2/plugins"
    cp "$here/plugins/UltimateAnimeSwitcher.plugin.js" "$2/plugins/"
    echo "Installed the UltimateAnimeSwitcher plugin: $2/plugins"
  fi
}

if [ $# -gt 0 ]; then
  copy_themes "your folder" "$1"
  exit 0
fi

case "$(uname -s)" in
  Darwin) config="$HOME/Library/Application Support" ;;
  *) config="${XDG_CONFIG_HOME:-$HOME/.config}" ;;
esac

install_client "Vencord" "$config/Vencord"
install_client "Vesktop" "$config/vesktop"
install_client "Vesktop (Flatpak)" "$HOME/.var/app/dev.vencord.Vesktop/config/vesktop"
install_client "BetterDiscord" "$config/BetterDiscord"

if [ "$found" -eq 0 ]; then
  echo "Couldn't find Vencord, Vesktop or BetterDiscord."
  echo "Run ./install.sh <your themes folder>, or copy the files in themes/ there yourself."
  exit 1
fi

echo
echo "Done! Open Discord settings > Themes and turn on ONE character."
