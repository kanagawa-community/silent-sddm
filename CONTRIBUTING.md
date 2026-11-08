# Contributing to Kanagawa for SilentSDDM

Thanks for helping. This port follows the
[Kanagawa community contributing guide](https://github.com/kanagawa-community/.github/blob/main/.github/CONTRIBUTING.md),
which explains conventional commits, the checks every pull request runs, and how
changes are reviewed. This page covers only what is specific to this port.

## Where to report what

- Problems with the theme in SilentSDDM, such as wrong colors, poor
  contrast, or a missing variant, belong in this repository's
  [issue tracker](https://github.com/kanagawa-community/silent-sddm/issues).
- Problems in SilentSDDM itself belong with its maintainers, not here. Start
  from the [application's page](https://github.com/uiriansan/SilentSDDM).
- Changes to the colors themselves belong in the
  [shared palette](https://github.com/kanagawa-community/.github/blob/main/docs/PALETTE.md),
  not in this port. Open an issue in the
  [.github repository](https://github.com/kanagawa-community/.github/issues)
  so every port stays in step.

## Colors

Take colors from the shared [palette](https://github.com/kanagawa-community/.github/blob/main/docs/PALETTE.md)
and follow the [style guide](https://github.com/kanagawa-community/.github/blob/main/docs/STYLE-GUIDE.md).
Do not sample colors from screenshots or add new ones. Every change must work in
Wave, Dragon, and Lotus.

To read the colors from a script, use the machine-readable
[palette.json](https://raw.githubusercontent.com/kanagawa-community/.github/main/palette.json).

## Working on this port

`themes/` is generated from the shared palette by `scripts/generate.py`, using the templates
`scripts/sddm-dark.conf.in` (Wave and Dragon) and `scripts/sddm-light.conf.in` (Lotus),
where `@role@` markers stand for palette roles. Do not edit `themes/` by hand. Run
`scripts/generate.py` and commit its output with every change; CI fails if a committed
file differs.

`backgrounds/` are copies of wallpapers made by `scripts/wallpapers.py` in the
[KDE port](https://github.com/kanagawa-community/kde). Change them there, then copy them
again.

SDDM runs as its own user, so the preset can only use fonts installed system-wide. To try
a change, run `./install.sh <variant>`, or copy SilentSDDM's theme folder somewhere, add the
preset and its background, point `ConfigFile` in its `metadata.desktop` at the preset, and
run `./test.sh` there.

## Pull requests

- Keep each pull request to one change, and include a screenshot of each variant
  it affects.
- Update the README when installation or usage changes.
