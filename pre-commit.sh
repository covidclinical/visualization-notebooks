#!/bin/sh

# This is a pre-commit git hook to clear notebook output.
# See the README.md for how to move this file to .git/hooks/pre-commit

if git rev-parse --verify HEAD >/dev/null 2>&1
then
	against=HEAD
else
	# Initial commit: diff against an empty tree object
	against=$(git hash-object -t tree /dev/null)
fi

# Find notebooks to be committed
NBS=`git diff-index --cached $against --name-only | grep '.ipynb$' | uniq`

# Remove outputs and re-stage the clean file
for NB in $NBS ; do
    echo "Removing outputs from $NB"
    jupyter nbconvert --ClearOutputPreprocessor.enabled=True -y --inplace "$NB"
    git add "$NB"
done

# If there are whitespace errors, print the offending file names and fail.
exec git diff-index --check --cached $against --
