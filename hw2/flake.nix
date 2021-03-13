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

        src = ./.;
        app = poetry2nix.mkPoetryApplication {
          projectDir = src;
        };

      in rec {
        defaultPackage = app;

        defaultApp = {
          type = "app";
          program = "${defaultPackage}/bin/median-stats";
        };

        checks = {
          mypy = pkgs.runCommand "check-mypy" {
            nativeBuildInputs = [ app.dependencyEnv ];
          } ''
          cd "${src}"
          mypy . tee "$out"
          '';

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
