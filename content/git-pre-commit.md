Title: Git pre-commit hook for Python projects
Date: 2022-11-24
Category: git
Tags: git; python
Status: published
Summary: A Git pre-commit hook for Python projects


For my future self, and other interested parties, below is my pre-commit hook for Python projects. It tests that all changed files are properly formatted, following Black's formatting style, and ensures that Pyflakes finds no problems with the committed files. It is a bash script, but could be any type of runnable file. Just make sure it has the proper hash-bang (`#! /bin/bash` in this casae), is stored as `.git/hooks/pre-commit`, and that it is executable (`chmod ugo+x .git/hooks/pre-commit`). See below for the full script.

It only checks for changed files that are added; the `git diff --name-only --cached --diff-filter=ACMR` part takes care of that, while the `[[ $fname == *.py ]]` takes care that only Python files are checked.

Often, you let a shell script fail early with the `set -euo pipefail`: the `-e` option exits immediately when any error (non-zero exit code) is caused by a command in the script, `-o pipefail` ensures this also works for parts of a pipe (instead of just the exit code in the last command of a pipe), and `-u` treats unset variables as an error. Usually, there would also be a `-x` option, which echos all commands run, but that doesn't make sense here. For this particular pre-commit, however, I want to let it test all files, issue a note for any problematic file, and finally exit with an error if there was any error along the way.

All output from Black and Pyflakes, both standard output and standard error, are ignored, and custom warning messages are issued, when a problem is encountered.

Since Pyflakes doesn't read its configuration from a `pyproject.toml` file yet, I'm using the small `pyproject-flake8` package to handle that part. We need to tweak one setting, the maximum line length, since Black uses 88, while Pyflakes follows PEP 8 here and has a default maximum line length of 80. The relevant parts of my `pyproject.toml` file are 

```
[tool.poetry.group.dev.dependencies]
black = "^22.10.0"
pyproject-flake8 = "^5.0.4.post1"

[tool.flake8]
# Match Black's line length
max-line-length = 88
```

Since this project uses Poetry, I run Black and Pyflakes with Poetry, through the development virtual environment set up by Poetry.

The code for the actual pre-commit script is as follows:

```
#! /bin/bash

# Don't exit early, so we get to see the echo messages
#set -euo pipefail

# black and pflake8 are installed through Poetry,
# thus we need to run them as such as well. Don't assume
# that Black and pflake8 are installed in the default
# developer setup.

retcode=0

# Test only staged files
for fname in $(git diff --name-only --cached --diff-filter=ACMR)
do
	# Test only Python files
	if [[ $fname == *.py ]]
	then

		poetry run black --check $fname > /dev/null 2>&1
		if [[ "$?" -ne 0 ]]
		then
			echo "Pre-commit hook: Black formatting check failed for $fname"
			echo "Run \`poetry run black --diff $fname\` to see where the problem is"
			echo
			retcode=1
		fi

		poetry run pflake8 $fname > /dev/null 2>&1
		if [[ "$?" -ne 0 ]]
		then
			echo "Pre-commit hook: Flake8 linting failed"
			echo "Run \`poetry run pflake8 $fname\` to see what failed"
			echo
			retcode=1
		fi
	fi
done

exit $retcode
```
