#!/usr/bin/env bash
# Install a Kanagawa preset into the SilentSDDM theme and select it. Needs root for the
# theme folder, so it uses sudo. Set SILENT_SDDM_THEME if the theme is elsewhere.
# ./uninstall.sh removes the presets again (and leaves ConfigFile in metadata.desktop alone).
#
# Usage: ./install.sh [--uninstall] wave|dragon|lotus
set -euo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")"
theme="${SILENT_SDDM_THEME:-/usr/share/sddm/themes/silent}"
declare -A background=(
  [wave]=kanagawa-wave-great-wave-dim
  [dragon]=kanagawa-dragon-great-wave-crest
  [lotus]=hokusai-great-wave-restored
)

uninstall=false
if [[ "${1:-}" == --uninstall ]]; then
  uninstall=true
  shift
fi
v="${1:-}"
if [[ -z "${background[$v]:-}" || $# -ne 1 ]]; then
  echo "usage: $0 [--uninstall] wave|dragon|lotus" >&2
  exit 2
fi
[[ -f "$theme/metadata.desktop" ]] || { echo "SilentSDDM not found in $theme" >&2; exit 1; }

if [[ "$uninstall" == true ]]; then
  sudo rm -f "$theme/configs/kanagawa-$v.conf" "$theme/backgrounds/${background[$v]}.jpg"
  echo "Removed kanagawa-$v"
else
  sudo install -m 644 "themes/kanagawa-$v.conf" "$theme/configs/"
  sudo install -m 644 "backgrounds/${background[$v]}.jpg" "$theme/backgrounds/"
  sudo sed -i "s|^ConfigFile=.*|ConfigFile=configs/kanagawa-$v.conf|" "$theme/metadata.desktop"
  echo "Installed kanagawa-$v"
fi
