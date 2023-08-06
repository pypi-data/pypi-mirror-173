import subprocess
import sys
from os.path import isfile, join
from pprint import pprint

from repo_utils import find_definition


def install_def(def_name: str, install=True):
    """
    Install using install.sh, requirements.txt, and install.py
    at the definition folder (in that order).
    If install is False, install.sh and install.py won't be run
    """
    def_path = find_definition(def_name)
    if not def_path:
        print(f'Definition {def_name} not found.')
        return False

    if install:
        install_filepath = join(def_path, "install.sh")
        if isfile(install_filepath):
            try:
                subprocess.check_output(["sh", install_filepath])
            except subprocess.CalledProcessError as e:
                print(e.output, file=sys.stderr)
                return False
    reqs_filepath = join(def_path, "requirements.txt")
    if isfile(reqs_filepath):
        try:
            output = subprocess.check_output(["pip", "install", "-r", reqs_filepath])
            pprint(str(output))
        except subprocess.CalledProcessError as e:
            print(e.output, file=sys.stderr)
            return False
    if install:
        install_filepath = join(def_path, "install.py")
        if isfile(install_filepath):
            try:
                subprocess.check_output(["python", install_filepath])
            except subprocess.CalledProcessError as e:
                print(e.output, file=sys.stderr)
                return False
    return True
