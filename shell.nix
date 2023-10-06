{ pkgs ? import <nixpkgs> {} }: pkgs.mkShell {
  buildInputs =
    let python3' = pkgs.python3.withPackages(p: with p; [ gitignore-parser ]);
    in [ python3' ];
}
