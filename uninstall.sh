#!/usr/bin/env bash
# Remove what install.sh installs. Takes the same variant: wave, dragon or lotus.
exec "$(dirname "${BASH_SOURCE[0]}")/install.sh" --uninstall "$@"
