 let
   nixpkgs = fetchTarball "https://github.com/NixOS/nixpkgs/tarball/nixos-23.11";
   pkgs = import nixpkgs { config = {}; overlays = []; };
 in

 pkgs.mkShell {
   packages = with pkgs; [
     nodejs_20
     git
     neovim
     python311
     python311Packages.pip
     pdm
   ];

   GIT_EDITOR = "${pkgs.neovim}/bin/nvim";
   shellHook = ''
       pdm install
   '';
}
