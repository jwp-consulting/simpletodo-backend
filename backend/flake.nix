{
  description = "Flake file for Projectify backend";

  inputs = {
    flake-utils.url = "github:numtide/flake-utils";
    nixpkgs.url = "github:NixOS/nixpkgs/24.05";
    poetry2nix = {
      url = "github:nix-community/poetry2nix/master";
      inputs.nixpkgs.follows = "nixpkgs";
    };
  };

  outputs = { self, nixpkgs, flake-utils, poetry2nix }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        # see https://github.com/nix-community/poetry2nix/tree/master#api for more functions and examples.
        pkgs = nixpkgs.legacyPackages.${system};
        inherit (poetry2nix.lib.mkPoetry2Nix { inherit pkgs; }) mkPoetryApplication mkPoetryEnv defaultPoetryOverrides;
        projectDir = self;
        postgresql = pkgs.postgresql_15;
        python = pkgs.python311;
        # Thanks to
        # https://github.com/nix-community/poetry2nix/blob/master/docs/edgecases.md#modulenotfounderror-no-module-named-packagename
        pypkgs-build-requirements = {
          django-anymail = [ "hatchling" ];
          django-cloudinary-storage = [ "setuptools" ];
          django-debug-toolbar = [ "hatchling" "setuptools" ];
          django-pgtrigger = [ "poetry" ];
          django-ratelimit = [ "setuptools" ];
          django-test-migrations = [ "poetry" ];
          editables = [ "flit-core" ];
          sqlparse = [ "hatchling" ];
          twisted = [ "hatchling" "hatch-fancy-pypi-readme" ];
          types-stripe = [ "setuptools" ];
        };
        overrides = defaultPoetryOverrides.extend (self: super: {
          psycopg-c = super.psycopg-c.overridePythonAttrs (
            old: {
              nativeBuildInputs = (old.nativeBuildInputs or [ ]) ++ [
                postgresql
              ];
              buildInputs = (old.buildInputs or [ ]) ++ [
                super.setuptools
                super.tomli
              ];
            }
          );
          cryptography = super.cryptography.overridePythonAttrs (old: rec {
            cargoDeps = pkgs.rustPlatform.fetchCargoTarball {
              inherit (old) src;
              name = "${old.pname}-${old.version}";
              sourceRoot = "${old.pname}-${old.version}/${cargoRoot}";
              sha256 = "sha256-qaXQiF1xZvv4sNIiR2cb5TfD7oNiYdvUwcm37nh2P2M=";
            };
            cargoRoot = "src/rust";
          });
        } // (builtins.mapAttrs
          (package: build-requirements: (
            (builtins.getAttr package super).overridePythonAttrs (old: {
              buildInputs = (old.buildInputs or [ ]) ++ (builtins.map (pkg: if builtins.isString pkg then builtins.getAttr pkg super else pkg) build-requirements);
            })
          ))
          pypkgs-build-requirements));
        poetryEnv = mkPoetryEnv {
          inherit projectDir;
          inherit overrides;
          inherit python;
          pyproject = ./pyproject.toml;
          poetrylock = ./poetry.lock;
          groups = [ "dev" "test" ];
        };
        projectify-backend = mkPoetryApplication {
          inherit projectDir;
          inherit overrides;
          inherit python;
          pyproject = ./pyproject.toml;
          poetrylock = ./poetry.lock;
          groups = [ ];
          checkGroups = [ ];
          outputs = [ "out" "static" ];
          postInstall = ''
            mkdir -p $out/bin $out/etc
            cp manage.py "$out/bin"

            cp gunicorn.conf.py gunicorn-error.log $out/etc/

            mkdir -p $static
            env \
              DJANGO_SETTINGS_MODULE=projectify.settings.collect_static \
              DJANGO_CONFIGURATION=CollectStatic \
              STATIC_ROOT=$static \
              python $out/bin/manage.py collectstatic --no-input
          '';
          # Disable checking runtime dependencies
          # https://github.com/nix-community/poetry2nix/issues/1441
          dontCheckRuntimeDeps = true;
        };
        # Workaround, since dependencyEnv accidentally forgets any other
        # outputs
      in
      {
        packages = {
          projectify-backend = projectify-backend;
          default = projectify-backend;
          container = pkgs.dockerTools.buildLayeredImage {
            name = "projectify-backend";
            tag = "latest";
            contents = [
              projectify-backend
            ];
            # Here and below we use relative paths
            extraCommands = ''
              mkdir -p var/projectify/static
              cp -a ${projectify-backend.static}/. var/projectify/static
            '';
            config = {
              Env = [
              ];
              Cmd = [
                "gunicorn"
                "--config"
                "${./gunicorn.conf.py}"
                "--log-config"
                "${./gunicorn-error.log}"
              ];
              ExposedPorts = {
                "8000/tcp" = { };
              };
            };
          };
        };
        # Run with `nix run`
        apps = {
          default = {
            type = "app";
            program = "${projectify-backend}/bin/projectify-backend";
          };
        };
        devShell = poetryEnv.env.overrideAttrs (oldattrs: {
          buildInputs = [
            postgresql
            pkgs.heroku
            pkgs.openssl
          ];
        });
      });
}
