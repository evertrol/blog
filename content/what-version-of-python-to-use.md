Title: What Python version to use
Date: 2022-10-17
Category: Python
Status: draft


# What Python version should I use

The most recent available minor version, with a few caveats and clarifications:

- minor version means the digit(s) after the first period: 3.10 is different than 3.9, but 3.10.6 is similar to 3.10.5. The last (set of) digit(s) indicate bugfix or security releases. See below for an extra note on the latter.

- if the most recent minor version was released less than one or two months ago, you may want to wait, so that additional Python packages that you may want to install, are available in in binary (precompiled) format. Most of the time, this will already have been done before the release of a new Python version

- your system might have an older Python version installed that is still current. But be aware that time can go quickly, and it may become unavailable / unsupported (by packages)  in the future.


To see how long your current Python will last, have a look at https://endoflife.date/python .

# Why the most recent Python version?

Because time travels one way, and at some point, you'll be writing outdated code. The good thing is that newer Python version are compatible with older code, that is, they can run older code without a problem. But definitely not the other way around: if you run newer code with an older Python version, things may break. (And that all is within the same major version: don't mix Python 2 and 3, that is likely to break either forwards or backwards)

There is one exception that I know of: when `async` become a keyword in version 3.5, older code that used `async` as, for example, a function keyword argument, resulted in syntax error. But the `match` statement introduced in 3.10 doesn't have this problem, since the syntax parser recognises the context and can distinguish between `match` (or `case`) as a keyword argument, variable name or part of the match statement.

(There are deprecation plans for future minor Python versions, 3.12 and beyond, of outdated, unmaintained or rarely used modules in the standard library. Such deprecations are also not backwards compatible, but done out of security concern. Generally, deprecations are preceeded by warnings in the one or two versions before that happens.)


# A stable environment

Using the most recent version of anything doesn't directly guarantee a stable environment. That is why I make a difference between developing code, and using code:

- for developing, use the most recent versions. Both of Python, and packages used.

  Occasionally, test with older versions of Python, and probably some of the packages as well.

  Once your code is ready for release, fix the version numbers that work, both for Python *and* the packages. So all of these have a range of valid working versions. If you can, allow for a range of version numbers; this is harder to test for, but allows more flexibility for complex installations. You'd probably want to test for the oldest and newest supported version of each package (note: there are cases where a single bugfix release turned out to be incompatible because of a bug. But most package managers will also have ways to exclude specific versions of a package.)

- for using code, use the current environment where it needs to be installed, if possible. If that feels too outdated (or will quickly become outdated), install a new version of Python and packages, and keep that fixed on the system (except for bugfix releases). Probably in a virtual or Conda environment.


# Python 2

Sadly, Python 2 is still being used. Sometimes, because old systems, where 2 is the default, are still being used (CentOS 7 is an example); other times, because old code that has not been converted to Python 3, needs to be run. (Note that I regard unconverted code as unmaintained, and shouldn't be used. But in reality, this may not be an option.)

There are two parts here

- if you develop Python code, write as if it's for Python 3, then use `from __future__` imports to make it Python 2 compatible if that needs to be supported (preferably not). For imports of renamed packages, use a `try: import <Python 3 name> except ImportError: import <Python 2 name>` You can also use a helper package like `six` or `future`, though I doubt it is really needed(*). Try and avoid checking specifically on the Python version.

  There will be some newer Python facilities that you'll miss out on this way, such as asyncio, the match statement, and f-strings.

- if you have to use Python 2 code for which there is no Python 3 version, there are two options:

  - try and convert it yourself. Ideally, you can run the `2to3` tool and be done with. But if things are more complicated, you'll be stuck with the other option

  - install and use (the latest version of) Python 2. Try and use it only for this code, for example in a Conda environment. (Note: I have not been able to find a Miniconda installer anymore that runs with Python 2. It looks like Python 2 is not supported anymore.)

  Be aware of dependencies here. If you install old code, but the dependencies are not properly limited (using the `>=x.y.z,<=p.q.r` syntax style or similar), you may end up with dependencies that are Python 3 only. In that case, you'll have to try and install older version of the dependencies yourself, or edit e.g. `setup.py` to set an upper limit on the dependency versions. This is something where Conda can come in handy. See below for some information on this.


(*) I've mostly seen six being used for checking on the Python version, which I don't recommend, and replacing `my_dict.items()` (Python 3) or `my_dict.iteritems()` with `six.iteritems(my_dict)`. I think you can easily juse use `my_dict.items()` in both 3 and 2: I doubt that the difference with (Python 2 only) `my_dict.iteritems()` is noticeable, unless you have large dictionaries. In which case, it is likely that some other structure, like a numpy recarray or a Pandas series, is better suited. For checking the Python version, using a `try-except` import and the like feels better: import the module (or run the functionality), and if it fails (because of an `ImportError` or `SyntaxError` etc), try the Python variant. This may eventually guarantee Python 4 compatibility. (Python 4 unlikely to happen anywhere in the near-ish future, after the Pyhon 2-3 debacle. But I've seen similar examples causing installations to break, because there was no forward compatibility: an if-else case was used to check for PowerPC or Intel platform (on a Mac), but there was no part that could handle the Apple Arm architecture. It used something like `if powerpc: ... else: ...`, instead of `if powerpc: ... elif intel: ... else: raise ValueError("platform not supported")`. Predicting the future is hard, but try to keep the options open.)


# Conda

Conda, in particular the Miniconda variant, can be convenient when having to run software with a specific Python version (or a package version). Create an environment for just that software, with the relevant Python version (e.g., `conda create --name old_software python==3.6`), and install the packages. This can also work for Python 2, although you may first need to install Miniconda2 for that. Conda should take care that the installed packages are compatible with the Python version (and with each other), so that you don't have to specify the package version each time yourself.

Note that a virtual environment doesn't really handle the use of different Python versions, since it will use the Python version of the software that created the virtual environment. (There are ways around that, but that requires installing multiple Python versions, which is already handled below.)

For development, I don't really recommend Conda, except perhaps for testing for various Python versions (which amounts to running your code in a environment, as described above). Instead, install a recent version of Python, and use that to develop, as well as for generic usage.


# PyEnv

PyEnv is my current favourite tool to test softare with various different Python versions. Carefully follow the guide in the README to install it, locally in your home directory, install the necessary versions with `pyenv install x.y.z`, and then set a directory (and subdirectories) local version with `pyenv local 3.10.6`. You can have one local Python version per directory, but you can easily set another version in another directory, or quickly switch to another version with the same command. You can also have a global (for your user account) Python version, different than the system Python version: it won't override or hamper the system in any way (I do absolutely recommend using a user-only installation, not a system installation, of pyenv, as that is largely how it is intended to be run).

The short gist is that you first install the necessary packages that are used to compile and install Python itself from scratch. Then, you clone and use the PyEnv repository to get the scripts that handle this compilation for you (and that fetch the relevant source code); I cloned it into `$HOME/.pyenv`. Set up your shell environment so that the `pyenv` executable can be found, and you're off. Occasionally, you need to update the repository, by going into the directory where you cloned it to, and run `git merge`; that way, your local version of `pyenv` knows about the latest Python versions. To see a list of all versions PyEnv knows about, use `pyenv install --list` (followed by `pyenv install x.y.z` for an installation). To see the list of all Python versions that already are installed locally, use `pyenv versions`, while just `pyenv version` shows the locally set version (applicable to this directory and its subdirectories). `pyenv global` shows the global version for your user account (set with `pyenv global x.y.z`); if you see two versions, one of them will likely be Python 2, accessible with the `python2` command.

The trick that PyEnv uses for a per-directory Python version, is that it creates a `.python-version` file that is a one-line text file containing the Python version. If the file is not found, PyEnv will look one directory up, and so on, until it finds a `.python-version`, or nothing, in which case it uses the global version.

There are (easy?) ways to use virtual environments with PyEnv, as well as ways to use `Tox` with PyEnv. `Tox` is a tester program, or perhaps a meta-tester program, that can use available Python versions to run unit tests for different versions, to check for compatibility across these Python versions.



# Further notes

## The security and bug-fix releases (that third number)

While it is good to have the most recent bugfix release version
installed and keep it updated, there will be no essential changes to
the Python version. And the majority of security and bug fixes are
unlikely to affect you, so you don't immediately need to
upgrade. Unless you happen to be a system administrator on, but then
you'll know what to do anyway (and you would use the system Python
version, and let the system handle the updates). Any bugfix or
security release will also not require re-installing all your packages
and code, so you can always safely overwrite the same minor Python
versions: 3.10.5 and 3.10.6 are completely compatible with eachother
(unless you happened to run into that specifc bug that was fixed in
3.10.6).

Essentially, the overarching numbering system is called [semantic versioning ("semver")](https://semver.org/), and should apply to other software as well. This is, however, not always the case: some software makes breaking changes in minor or even bugfix releases, and other software follows a completely different versioning scheme. The latter might be by date, in which case it is impossible to see from the version number whether versions are compatible; and some software uses the (shortened) hash calculated by their versioning software (recognisible as a hexadecimal number). The the date and hash variants are, occasionally, also attached to the full semantic version, as an extra. For example, 2.5.6v45fa96 or 1.2.3v20220304. You should be able to ignore the second part, but it makes it easier to track the repository version or see how recent a version is.


## Testing

I have mentioned testing various times, including Tox and unit tests. Since you want to avoid running all tests manually every time you may a change (it's annoying, costs lots of time, and it's too easy to make a mistake), this is where continuous integration comes into play (the abbrevation CI is what is usually written, since it's a very well know abbreviation in software development). CI is a tool, or a set of tools, that near-automatically detects changes in the software and then runs a series of tests. Or it runs tests at scheduled times. The tests are often unit tests, very simply and quick tests, to ensure the code functionality hasn't changed. It will also test the installation, since most CI software sets up a virtual machine for you, where it installs the software from scratch. This way, you'll know if dependencies work, and often, you can set which virtual machines (i.e., which platforms) you want to test on (platforms that require a paid license may more difficult to test against, or you'll indeed have to pay for it). A simple test of the installation and a quick run or a few unit tests can already be enough to detect some easily overlooked errors (example: C++ code with a new class implementation, but a header file that isn't checked in to the repository. As a developer, you won't notice, because the header file is there, locally on your machine. But a fresh installation, done automatically, which likely fail on the compilation step, once the class definition can't be found.)

Testing is a large subject, and even CI, just part of it, can take some time to learn or teach about. So I mention it here, but may defer an actual explanation to another post.
