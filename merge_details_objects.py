#!/usr/bin/env python
#
# Copies output/Details and output/Objects into output/Objects_new, concatenating any
# duplicate stg files.

import os
import sys
import shutil
import pathlib

if __name__ == "__main__":

    if not os.path.isdir(os.path.join("output", "Objects")):
        sys.stderr.write("output/Objects not found.\n")
        sys.exit(1)
    if not os.path.isdir(os.path.join("output", "Details")):
        sys.stderr.write("output/Details not found.\n")
        sys.exit(1)

    # Create output directory
    try:
        os.mkdir(os.path.join("output", "Objects_new"))
    except OSError:
        sys.stderr.write("output/Objects_new must not already exist.\n")
        sys.exit(1)

    # Copy files and directories from output/Objects
    for root, dirs, files in os.walk(os.path.join("output", "Objects")):
        for fname in files:
            splitroot = root.split(os.path.sep)
            # Gives relative path of parent directory under output/Objects
            relroot = os.path.join(splitroot[2], splitroot[3])
            # Create the parent directory structure under the output directory (like mkdir -p)
            destroot = os.path.join("output", "Objects_new", relroot)
            pathlib.Path(destroot).mkdir(parents=True, exist_ok=True)
            # Copy the file
            shutil.copy(os.path.join(root, fname), destroot)

    # Copy files and directories from output/Details
    for root, dirs, files in os.walk(os.path.join("output", "Details")):
        for fname in files:
            splitroot = root.split(os.path.sep)
            relroot = os.path.join(splitroot[2], splitroot[3])
            destroot = os.path.join("output", "Objects_new", relroot)
            if not os.path.isdir(destroot):
                pathlib.Path(destroot).mkdir(parents=True, exist_ok=True)
            # If the file exists and is an stg, append rather than overwriting. If not
            # an stg, issue a warning.
            if os.path.isfile(os.path.join(destroot, fname)):
                if not fname.endswith(".stg"):
                    print("Warning: {:s}/{:s} already exists - not overwriting!".format(
                          destroot, fname))
                else:
                    print("Appending to {:s}/{:s}.".format(destroot, fname))
                    f1 = open(os.path.join(destroot, fname), 'a')
                    f2 = open(os.path.join(root, fname))
                    for line in f2:
                        f1.write(line)
                    f1.close()
                    f2.close()
            else:
                shutil.copy(os.path.join(root, fname), destroot)
