# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2023 JWP Consulting GK
# Nix Flakes file
{
  description = "Projectify frontend";
  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-24.05";
    flake-utils.url = "github:numtide/flake-utils";
  };
  outputs = { self, nixpkgs, flake-utils }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = nixpkgs.legacyPackages.${system};
        nodejs = pkgs.nodejs_20;
        mkFrontend =
          { wsEndpoint ? "/ws"
          , apiEndpoint ? "/api"
          , apiEndpointRewriteTo ? "/api"
          , projectifyDomain ? "https://www.projectify.com"
          , adapter ? "node"
          , visualize ? false
          }:
          # TODO make WS_ENDPOINT, API_ENDPOINT and PROJECITYF_DOMAIN arguments
          # to this derivation
          pkgs.buildNpmPackage {
            name = "projectify-frontend";
            srcs = [
              ./.
              ../LICENSES
            ];
            sourceRoot = "frontend";
            npmDepsHash = "sha256-Ge2lPPKy2vZAieiZcZqbBzIVYfb3qq9lu0/KF/Ihjjk=";
            buildInputs = [
              nodejs
            ];
            prePatch = ''
              # Patch LICENSES folder into here, removing the symlink first
              rm LICENSES
              cp -r ../LICENSES .
            '';

            preConfigure = ''
              export VITE_WS_ENDPOINT=${wsEndpoint}
              export VITE_API_ENDPOINT=${apiEndpoint}
              export VITE_API_ENDPOINT_REWRITE_TO=${apiEndpointRewriteTo}
              export VITE_PROJECTIFY_DOMAIN=${projectifyDomain}
              export VITE_GIT_COMMIT_DATE=${self.lastModifiedDate}
              export VITE_GIT_BRANCH_NAME=nix
              export VITE_GIT_COMMIT_HASH=${self.rev or "dirty"}
              export PROJECTIFY_FRONTEND_ADAPTER=${adapter}
              export NODE_ENV=production
            '';
            npmBuildFlags = if visualize then "-- --mode staging" else "";

            postBuild =
              if adapter == "node" then ''
                cp -a package.json node_modules build/
              '' else "";

            installPhase =
              if visualize then ''
                mkdir -p $out
                cp .svelte-kit/output/client/bundle.html $out/client-bundle.html
                cp .svelte-kit/output/server/bundle.html $out/server-bundle.html
              '' else ''
                mkdir -p $out
                cp -a build/. $out/
              '';
            meta = with pkgs.lib; {
              description = "Frontend for the Projectify project management software";
              homepage = "https://www.projectifyapp.com";
              license = with licenses; [ agpl3Only mit ];
              maintainers = [
                {
                  name = "Justus Perlwitz";
                  email = "justus@jwpconsulting.net";
                }
              ];
            };
          };
        projectify-frontend-static = mkFrontend { adapter = "static"; };
        projectify-frontend-node =
          let
            frontend = (mkFrontend { adapter = "node"; });
          in
          pkgs.writeShellApplication {
            name = "projectify-frontend-node";
            runtimeInputs = [
              frontend
              nodejs
            ];
            text = ''
              exec node ${frontend}
            '';
          };
      in
      {
        inherit self nixpkgs;
        lib = {
          inherit mkFrontend;
        };
        packages = {
          inherit projectify-frontend-static;
          inherit projectify-frontend-node;
          projectify-frontend-bundle-viz = mkFrontend {
            adapter = "node";
            visualize = true;
          };
        };
        devShell = pkgs.mkShell {
          buildInputs = [
            nodejs
          ];
        };
      });
}
