<!--
SPDX-FileCopyrightText: 2021 Kirill Elagin <https://kir.elagin.me/>

SPDX-License-Identifier: MPL-2.0
-->

# Differential Privacy HW2

Return Noisy Max median.


## Install

This directory is a [Poetry] project, so you don’t need to do anything
special, just have Poetry installed. Or use [Nix], since this directory
is also a Nix flake.

## Usage

If you use [Nix], execute `nix run` in this directory – it will build
all the dependencies and launch the program.

Without Nix, execute `poetry run median-stats`.

The program outputs LaTeX tables, that you can just copy-paste into a
`tabular` environment or something like this. Unfortunately, it means
that the output is a bit hard to read on the terminal.


## Development

### Environment

With [Nix], run `nix develop` to get a shell with everything you need available.

Wihout Nix, make sure you have [Poetry] and run `poetry shell`.

Then use `python3 -m dpmedian` to run the program.


### Hacking

### Dependencies

Since this is a Poetry project, use `poetry` to add or remove Python
dependencies. If you are in a Nix development shell, you will have to restart
it if the dependencies change.

### Types

* Run `mypy .` to type-check `.py` files


## Contributing

Please, do not contribute to this project.


## License

[MPL-2.0] © [Kirill Elagin]


[Poetry]: https://python-poetry.org/
[Nix]: https://nixos.org/

[MPL-2.0]: https://spdx.org/licenses/MPL-2.0.html
[Kirill Elagin]: https://kir.elagin.me/
