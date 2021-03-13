<!--
SPDX-FileCopyrightText: 2021 Kirill Elagin <https://kir.elagin.me/>

SPDX-License-Identifier: MPL-2.0
-->

# Differential Privacy HW1

An attack on a non-so-differentially-private algorithm.

The code demostrates an attack
that is able to recover a big share of “private” information released
in a pretty insecure way.


## Install

This directory is a [Poetry] project, so, in theory, getting all the
dependencies should be as easy as running `poetry shell`. However, some of
the packages depend on C libraries (in particular, `jupyter`),
so you also need to make sure you have the following packages installed:

* `libzmq` ([ZeroMQ], required by Jupyter)

However, if you use [Nix], then you don’t need to do anything at all as
it will handle verything for you.


## Usage

If you use [Nix], execute `nix run` in this directory – it will build
all the dependencies and launch Jupyter.

Without Nix, assuming you installed all the required system packages (and [Poetry])
you can type `poetry run jupyter notebook`.

Either way, once you get the dependencies working and manage to get Jupyter running,
open the `Solution` notebook and try the code that it contains.


## Development

### Environment

With [Nix], run `nix develop` to get a shell with everything you need
(including Poetry) available.

Wihout Nix, make sure you have [Poetry] and all required system dependencies,
then run `poetry shell`.

### Dependencies

Since this is a Poetry project, use `poetry` to add or remove Python
dependencies. If you are in a Nix development shell, you will have to restart
it if the dependencies change.

### Structure

All code goes into the `dpcourse_hw1` directory.
Jupyter notebooks go to a separate `notebooks` subdirectory (because Jupyter
messes up `sys.path` in really bad ways).

Boring stuff belongs to simple `.py` files, interesting stuff – to Jupyter notebooks.

### Types

* Run `mypy ./dpcourse_hw1` to type-check `.py` files
* Run `nbqa mypy ./dpcourse_hw1/notebooks` to type-check notebooks


## Contributing

Please, do not contribute to this project.


## License

[MPL-2.0] © [Kirill Elagin]


[Poetry]: https://python-poetry.org/
[Nix]: https://nixos.org/
[ZeroMQ]: https://zeromq.org/

[MPL-2.0]: https://spdx.org/licenses/MPL-2.0.html
[Kirill Elagin]: https://kir.elagin.me/
