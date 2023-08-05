#!/usr/bin/env python
# coding: utf-8

"""
Creates needed directories and files to create a local package from your jupyter notebook

Executing 
    notebook_to_package("notebook_name.ipynb")

Will create
    notebooks/
    ├── src/
    │   └── <notebook_name>/
    │       ├── __init__.py
    │       └── <notebook_name>.py
    ├── bin/
    │   └── <notebook_name>.py #executable

And enable you to import functions from notebooks.src.<notebook_name>

Helper functions
    make_dirs
    clean_up_file
    notebook_to_executable

"""

import os
import pathlib
import shutil
import subprocess
import re
import argparse


def make_dirs(package_name, top_level_dir="notebooks"):
    """Makes any needed empty directories that don't exist"""

    toplevel_dir = pathlib.Path.cwd().joinpath(top_level_dir)
    source_dir = pathlib.Path.joinpath(toplevel_dir, "src")
    package_dir = pathlib.Path.joinpath(source_dir, package_name)
    executables_dir = pathlib.Path.joinpath(toplevel_dir, "bin")

    if not toplevel_dir.is_dir():
        toplevel_dir.mkdir()

    if not source_dir.is_dir():
        source_dir.mkdir()

    if not package_dir.is_dir():
        package_dir.mkdir()

    if not executables_dir.is_dir():
        executables_dir.mkdir()

    return package_dir, executables_dir


def clean_up_file(f_name, executable=False):
    """Remove the indicators for cells, extra space, and anything below a MARKDOWN cell
        that includes "# DO NOT ADD BELOW TO SCRIPT"
        If executable=False, the associated header is removed"""

    do_not_add_below_to_script = "# # DO NOT ADD BELOW TO SCRIPT"
    skip = 0
    cell_nums = re.escape("# In[") + r"*[0-9]*" + re.escape("]:")

    with open(f_name, "r") as f:
        lines = f.readlines()  # get a list of lines from the converted script

    with open(f_name, "w") as f:  # overwrite the original converted script

        for i, line in enumerate(lines):

            if not executable and i == 0 and re.search("#!", line.strip()):
                pass

            else:

                if re.search(cell_nums, line.strip()):  # don't include the '#In[##]:' lines
                    skip = 2

                elif skip > 0 and line == "\n":  # trim extra blank lines below #In[##]:' lines
                    skip -= 1

                elif re.search(do_not_add_below_to_script, line):  # don't include this or below
                    break

                else:
                    f.write(line)

    return True


def notebook_to_executable(notebook_name):
    convert_string = f'jupyter nbconvert --to script {notebook_name}'
    subprocess.run(convert_string.split(" "))


def notebook_to_package(notebook_name, top_level_dir="notebooks", cleanup=True):
    if not pathlib.Path(notebook_name).is_file():
        raise FileNotFoundError(f'{notebook_name} not found')

    notebook_to_executable(notebook_name)

    executable_name = notebook_name.lower().replace(" ", "_").replace(".ipynb", ".py")
    package_name = executable_name.replace(".py", "")

    package_dir, executables_dir = make_dirs(package_name, top_level_dir)
    init_file = pathlib.Path.joinpath(package_dir, "__init__.py")
    package_file = pathlib.Path.joinpath(package_dir, executable_name)

    executable_file_orig = pathlib.Path.cwd().joinpath(executable_name)
    executable_file_dest = executables_dir.joinpath(executable_name)

    shutil.copy(executable_file_orig, executable_file_dest)
    shutil.copy(executable_file_orig, package_file)

    init_file.touch()
    clean_up_file(executable_file_dest, True)
    clean_up_file(package_file, False)

    if cleanup:
        os.remove(executable_file_orig)

    return True


parser = argparse.ArgumentParser("notebook name")
parser.add_argument('--nb', type=str, help='notebook to convert', required=True)
args = parser.parse_args()

notebook_to_package(args.nb)
