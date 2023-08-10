Title: How to install new or manage multiple Python versions
Date: 2022-09-25
Tags: python, versions
Category: python
Authors: Evert
Slug: manage-multiple-python-versions
Summary: Use pyenv to easily install new or switch between multiple Python verions.

# How to install new or manage multiple Python versions


Prerequisities:

- A reasonably new Ubuntu or Ubuntu-derived system. This helps matching the required system packages to be installed, that are used to build Python form source later on.
- Single user usage of Python packages. That is, you are not the system administrator that installs packages for multiple users.

- Don't use `sudo` to install Python or a Python packages. There is no need for it, and it can only mess up your system. `sudo` is only to be used to update the system, or install helper packages (libraries, compilers) to build Python or any package (such as NUmPy) from source, through the system package manager (such as `apt`, `dnf` or `pacman`).

That also means there is no need to install (system) packages such as `python(3)-numpy` or `python(3)-scipy`, or even `python(3)-pip`. In fact, these could possibly even be uninstalled, and no harm would come from it. But if they are installed, let them be. They should not interfere with user-installed versions later on.

Note that virtual environments are only good for handling different Python package versions. Not for handling different Python versions. You could use Conda instead for handling different Python versions, but I've never been a fan of Conda, nor am I likely to be (though it will absolutely work for a lot of people). If you do use Conda, use it through https://docs.conda.io/en/latest/miniconda.html and install packages and/or specific Python versions yourself in a Conda environment.

Don't install Python from e.g. the official site, e.g. https://www.python.org . There are more convenient ways to do that, plus these installations may suggest to use `sudo`; see point 0.

My favourite Python version handler / installer is [pyenv](https://github.com/pyenv/pyenv-virtualenv). The name is a bit of a misnomer: pyversions might be better (there also doesn't seem to be any capital letter(s) in its name). It can install many different Python versions, locally (that is, user-only), and easily let you switch between them. If wanted, each of these different Python versions can then use as many different virtual environment as you'd like. So you can have a Python versions + v-env for each project if wanted.

The documentation is all there on its GitHub page, but since it includes documentation for many platforms, shells and what not, and some things still seem to be missing, below it's written in one go for Ubuntu & friends.

## Setting up and installing pyenv

pyenv builds Python form source, thus it requires some libraries and a C compiler to be installed. That includes some graphical libraries, for its Tk module, so in total, it may be quite a bit of packages. It's a one-off though: do it once, then forget you ever installed them. For Ubuntu, this should be
```
sudo apt-get install -y make build-essential libssl-dev zlib1g-dev \
libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm \
libncursesw5-dev xz-utils tk-dev libxml2-dev libxmlsec1-dev libffi-dev liblzma-dev \
git
```
(This is the only time `sudo` is used.)

`git` is for actually downloading/cloning pyenv. Remove the `-y` option if you want to manually confirm the list of packages that are about to be installed. The list, by the way, is from [the pyenv wiki](https://github.com/pyenv/pyenv/wiki).

Once that is installed, make sure you are in your home directory: `cd`. Now clone the repository into a `~/.pyenv` directory:
```
git clone https://github.com/pyenv/pyenv.git ~/.pyenv
```

Optionally, build a little bash extension for speedier use of pyenv:
```
cd ~/.pyenv && src/configure && make -C src
```

The following goes into your `~/.bashrc` (or `~/.zshrc`; I'm a Zsh user):
```
if [ -d "$HOME/.pyenv" ]
then
        export PYENV_ROOT="$HOME/.pyenv"
        command -v pyenv >/dev/null || export PATH="$PYENV_ROOT/bin:$PATH"
        eval "$(pyenv init -)"
fi
```

This sets up pyenv properly for use in your shell.

Source the `~/.bashrc` file (or log out/log in; or open a new terminal). To verify, see that `printenv PYENV_ROOT` is set to `/home/<username>/.pyenv`.

From the above, it is hopefully obvious that this only works for the current user (given the use of `$HOME`). Which is great: no interference with anything but yourself.


## What does pyenv do? How does it work?

The longer (more complicated?) description is in the README in its repository. Basically, it sets up your `PATH`, and possibly `LD_LIBRARY_PATH` (but probably not: the relevant `libpython*` will be statically linked), so that any Python version it has installed, will be found before the system Python version. Don't worry, the system Python is still there (probably as `/usr/bin/python`) and system scripts that rely on that will have `#! /usr/bin/python` at their top (also, system scripts run as root or some other users, and won't even see the `~/.pyenv` directory).

You can see installed Python versions with
```
pyenv versions
```

which will show nothing, since nothing was installed yet.

To show available Python versions, use
```
pyenv install --list | more
```
(there are 586 versions available, as of 2022-09-20).

To install, for example, the most recent version CPython 3.9 (CPython is the most standard Python), use
```
pyenv install 3.9.14
```

It will download that version from the source, then start building it (using the system packages installed above). That may take a few minutes, so sit back, relax, take a coffee, etc.

Once done, `pyenv versions` will show it. Before showing how to use it, let's install another versions, to show how to switch between versions, and how to set (user-)global and (directory-)local versions: `pyenv install 3.10.7` for the most recent (stable) Python version currently.

The actual places where these Python versions (and packages later on) are installed are in `~/.pyenv/versions/x.y.z`. You'll find `bin/` and a `lib/pythonx.y/site-packages/` etc directories in those directories.

## Using pyenv

Let's set our default Python version to 3.10.7:
```
pyenv global 3.10.7
```

That sets it for the current user, anywhere. `pyenv versions` will show an asterisk in front of it. Starting `python`, or just simply `python -c "import sys; print(sys.version)` should show that.

Any Python package now installed, will be installed for this Python version.

To use the other Python version for a specific project, *create and change to a specific directory* for that project. Then, use
```
pyenv local 3.9.14
```

Now, this directory, and all of its subdirectories, will use Python version 3.9.14. The way pyenv does that, is by noticing the file `.python_-version` in the base directory, which directs the Python version to use (the contents of that file is just `3.9.14`).

Note that this Python is separated from all other Python installations. For example, for me, `python -c "import numpy; print(numpy.__version__)"` fails on `ModuleNotFoundError`; but in my home directory, the global version has NumPy 1.23.2 installed, while doing this with `/usr/bin/python` shows `1.21.5` (which is the `python3-numpy` package).

You can also always see the current Python version with
```
pyenv version
```

Of course, you can switch around: use `3.9.14` as a global version, and `3.10.7` in subdirectories for specific projects. What you won't (ever) need to use anymore, is the system Python. Ignore it, let it update itself with `sudo apt update` in normal system maintenance (or whatever you use for that), and that's it.

## Installing packages

Installing packages with `pip` works as usual: pyenv takes care of providing the correct `pip`. Nevertheless, I always advise to install through Pip with
```
python -m pip install <package(s)>
```
That guarantees the Pip version used corresponds to the Python version used. There are too many cases where `pip` did not correspond with `python`, and people were not able to use the Python package they had just installed.

Aside: the `-m` flag is for a "runnable module": `pip` is really a simple wrapper scripts around a Python module/package. Runnable modules are a neat Python utility that allows a package to be run as a script (more or less), which also guarantees the correct Python version is used with that package.


## Virtual environments

As mentioned, you can use virtual environments (v-envs) with any of these Python versions. Just make sure they are all named differently: don't use the same name for a v-env while only the Python version differs.
```
python -m venv <name>
```
will simply create the virtual environment `<name>` for the current Python. Activate it as usual:
```
source myvenv/bin/activate
```

and `deactivate` to turn it off.

In general, I've rarely had the need for a v-env: packages I've installed rarely, if ever, conflict between each other. But for a large(ish) project, with lots of fixed dependency versions, a v-env might be useful.

In fact, I rarely had the need for switching between multiple Python versions. I mainly use this option for testing, to see if things can work with older (or newer) versions of Python.

Also: there is a plugin for pyenv that might may working with virtual environments easier/better/clearer: https://github.com/pyenv/pyenv-virtualenv . But I haven't used it. Its repository looks recent enough, though activity seems to have dwindled a bit (e.g., there are very few comments on recent pull requests).

## Updating pyenv

pyenv will not automatically find newly released Python versions. The repository will be updated with the information, but they are not fetched from your local machine. But it's an easy step to update this yourself: go to the `~/.pyenv` directory, then run
```
git pull
```
to pull in the latests updates from the pyenv repository. This should be a smooth update, and once done, you can run `pyenv install --list | more` again to see all available Python versions, which should have the latest-greatests versions as well (e.g., 3.11 is currently in the release-candidate stage, but is expected to be fully released in October 2022. Give it one or two months for packages to be updated as well, and you can use that as the global Python version; I certainly will.)


Note that packages like NumPy and SciPy will likely be up-to-date at any new Python release, since these use beta and release candidates to adjust to the new versions. It's less well-maintained packages that may be problematic, though generally, Python is backwards-compatible enough that this should not be a problem.
