#! /usr/bin/env nix-shell
#! nix-shell -i python3 -p "python311.withPackages(p: with p; [ gitignore-parser ])"

import logging
import os
from glob import glob
from pathlib import Path
import sys

currentDir = Path(__file__).parent.absolute()
print(currentDir)
sys.path.append(str(currentDir))

from gitignore_parser import parse_gitignore

logging.basicConfig(level=logging.DEBUG)

matchers = []
root_path = os.getcwd()


def matches(path: str) -> bool:
    try:
        return any(matcher(path) for matcher in matchers)
    # Ignore if path does not belong to a matcher
    except ValueError:
        return False

#TODO:Add a cli to output to a file
#TODO:Add a note that says that this file was automatically generated and link the repo
for gitignore_path in glob("**/.gitignore", recursive=True):
    if matches(gitignore_path):
        logging.info(f"Ignore {gitignore_path}")
        continue

    logging.info(f"Evaluate {gitignore_path}")
    matchers.append(parse_gitignore(gitignore_path, base_dir=root_path))

    gitignore_dir_path = os.path.dirname(gitignore_path)
    with open(gitignore_path) as gitignore:
        print(f"# {gitignore_path}")

        for line in gitignore.readlines():
            line = line.strip()

            if not line or line.startswith("#"):
                continue

            if line.startswith("!"):
                print("!", end="")
                line = line[1:]

            if line.startswith("/"):
                print(f"{gitignore_dir_path}{line}")
                continue

            if "/" in line and line[-1] != "/":
                print(f"{gitignore_dir_path}/{line}")
                continue

            print(f"{gitignore_dir_path}/{line}")
            print(f"{gitignore_dir_path}/**/{line}")

        print()
