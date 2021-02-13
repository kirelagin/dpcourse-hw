# SPDX-FileCopyrightText: 2021 Kirill Elagin <https://kir.elagin.me/>
#
# SPDX-License-Identifier: MPL-2.0

{
  inputs = {
    flake-utils.url = "github:numtide/flake-utils";
    poetry.url = "github:nix-community/poetry2nix";
  };

  outputs = inputs@{ self, nixpkgs, flake-utils, poetry }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = import nixpkgs { inherit system; overlays = [ poetry.overlay ]; };
        inherit (pkgs) poetry2nix;

        overrides = self: super: {
          jupyterlab-widgets = super.jupyterlab-widgets.overridePythonAttrs (
            old: {
              buildInputs = (old.buildInputs or []) ++ [ self.jupyter-packaging ];
            }
          );
          #z3-solver = super.z3-solver.overridePythonAttrs (
          #  old: {
          #    propagatedBuildInputs = (old.propagatedBuildInputs or []) ++ [ pkgs.z3 ];
          #  }
          #);
        };

        src = ./.;
        poetryPython = poetry2nix.mkPoetryPackages {
          projectDir = src;
          overrides = [ poetry2nix.defaultPoetryOverrides overrides ];
        };
        env = poetryPython.python.withPackages (_: poetryPython.poetryPackages);

      in {
        defaultApp = {
          type = "app";
          program = toString (pkgs.writeShellScript "dpcourse-hw1-jupyter" ''
            ${env}/bin/jupyter notebook --notebook-dir=./dpcourse_hw1/notebooks
          '');
        };

        devShell = pkgs.mkShell {
          buildInputs = [
            env
          ];

          nativeBuildInputs = [
            poetryPython.python.pkgs.poetry
          ];

          shellHook = ''
            export PYTHONPATH=.

            echo 'To launch Jupyter, run:'
            echo '  $ jupyter notebook'
          '';
        };

        checks = {
          mypy = pkgs.runCommand "check-mypy" {
            nativeBuildInputs = [ env ];
          } ''
          cd "${src}"
          mypy ./dpcourse_hw1 | tee "$out"
          '';

          #mypy-nb = pkgs.runCommand "check-mypy-nb" {
          #  nativeBuildInputs = [ env ];
          #} ''
          #cd "${src}"
          #nbqa mypy ./dpcourse_hw1/notebooks/Solve.ipynb | tee "$out"
          #'';

          reuse = pkgs.runCommand "check-reuse" {
            nativeBuildInputs = [ pkgs.reuse ];
          } ''
          cd "${src}"
          reuse lint | tee "$out"
          '';
        };
      }
    );
}
