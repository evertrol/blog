Title: Runnable Python modules
Date: 2022-11-24
Category: python
Tags: python
Status: published
Summary: How to use and create runnable Python modules and packages

Python has a neat feature, that allows one to run an installed module or package as if it were a command line program (or script, if you prefer that term). The module or package needs some small code setup for that to work, but if that's available, you can simply do
```
python -m some_package
```
on the shell command line; while, of course, you can still import and use all of the functionality of `some_package` in Python itself.

## Why use runnable modules

The major convenience, to me, is that it is guaranteed that the module or package is run with that specific Python executable. This is in particular useful when you install things with Pip, the Python package manager, and then later want to run the installed package for the corresponding Python setup. The Pip example is somewhat notorious, because numerous examples can be found on the internet of people having installed a package through Pip, and then not being able to import or execute it with Python: it turns out they often have multiple Python installations, and the `pip` command didn't match their `python` command. Using `python -m pip` (followed by e.g. `install jupyter`) very often solves that problem. This was in particular an issue during the Python 2-to-3 transition (and still is, in its aftermath), where `pip` *might* refer to the Python 2 version, while `python` might refer to the Python 3 version. (The operating system would normally have a clear distiction by using explicit version numbers in the commands, but if people installed their own Python version from somewhere, things could get tricky.)

I now basically run any external Python program as a runnable module/package, as a habit. It is a few more keystrokes, but it saves me any potential problems occurring later. Some particular commands are:
```
python -m pip [install | list | ...] ...

python -m venv myenvironment

python -m jupyter [notebook | console | ...]

python -m black  # A Python formatter

python -m pylint  # A Python linter

python -m pyflakes  # Another Python linter

python -m poetry  # For package development
```

Note: when using an (active) virtual environment, this problem goes away; or at least it should. I still always check in a virtual environment if the commands I use directly are found in the virtual environment: `which python`, `which pip` or `which jupyter` would do that (for example, if I haven't yet installed Jupyter in the virtual environment, but it is installed globally, running `jupyter` will still work, but it will not pick up the virtual environment. While `python -m jupyter` in that virtual environment will promptly complain about the package not being found.


## How to create a runnable module

This is where the if-clause often found in Python comes into play:
```
if __name__ == "__main__":
    main()
```
(the choice of `main()` is up to the programmer; below I'll show the fuller structure I use in my programs.)

This should be at the base level in any module (that is, not inside a function). When a module is imported, the special variable `__name__` takes the name of that module (possible prepended with the (sub)package name). In that case, the if-statement doesn't pass, and the `main()` is not run. Note that the *definition* or `main` and other functions will still be parsed, but not executed.

If the module is executed directly, or, more conveniently, as a runnable module, the `__name__` variable has the value `"__main__"`, and the function `main()` is executed. Depending on what the `main()` function does, it then executes more functions and such, and the module is being run.

My overall structure of a module often looks as follows:
```
# import statements
# global variables
# (other) function definitions

def run(arg1, arg2, arg3):
    ...

def main():
    # do command line parsing
    args = parse_args()

    # set up logging
    setup_logging(args.loglevel)

    run(args.value1, args.value2, args.value3)

if __name__ == "__main__":
    main()
```

The `run` function is actually the main entry point of the module. If you import the module, you would then call the `run` function to execute things, e.g.: `import mymodule; mymodule.run(1, 2, 3)`. Other appropriate function names are fine, but `run` is nicely generic while I'm still writing the code and sorting out the detailed module structure.

When executed as a runnable module, `main()` is called first. This handles the command line arguments (I still stick to the `argparse` module, but use your favourite package). It then sets up the logging (note: this should not be set in e.g. `run()`, but at the outer level, so in this case `main()`. There are some more details to it, but if you set up logging in `run()`, then you might override any logging level that has been defined by the calling program that has the `import mymodule` and `mymodule.run` lines, which is not what you want. Inside `main()`, there is no calling program: `main()` is essentially the calling program.


### Creating a runnable package

You can also create a runnable package. Of course, a package is often just a directory, so you can't really code an `if __name__ == "__main__"` statement there. You might think that you should do this in `__init__.py`, but the actually file that you need to create is `__main__.py`. If you have a directory/package `mypackage/` with `__main__.py` (next to a, perhaps empty, `__init__.py` file) in that directory, you can run `python -m mypackage` and the code in `mypackage/__main__.py` will be executed. I still use the above structure, with `run`, `main` and `if __name__ ...` in that file, but that isn't really necessary: `__main__.py` is only used directory to run as a program, not as import. So a `run()` function doesn't make much sense. In fact, it is more like
```
from . import core

def main():
    # as before

    core.run(args...)

if __name__ == "__main__":
    main()
```

I tend to keep `__init__.py` empty, except for some imports and perhaps the occasional global variable, and put the main functionality in a `core.py` file, which then of course has a `run()` function. (I copied the `core.py` idea from AstroPy, which may have copied this from elsewhere.)

To note again: this functionality is only used to make a package runnable. `__main__.py` is never imported (nor should it be), so any functional code shouldn't really be there.


### Wrapping the runnable module in a script

Sometimes, a developer might still prefer a command line program, next to runnable module or package. The program would simply import the relevant module and execute `main()` directory, to handle command line arguments and logging setup. One disadvantage is that the program name may not be the actual program: `sys.argv[0]` may contain the module name, not the program name. Some smart handling of this can resolve this, which provides nicer (warning) messages to a user when they run the program with a `--help` option or forgot a command line argument.

Several tools for creating Python packages, such as Setuptools and Poetry, already do this. In Poetry, you set up your scripts by setting its name to the function in the package to be executed, in the `pyproject.toml` file (I'm unfamiliar with Setuptools exact way of handling this; but you use something called entry-points). So that would like something like
```
[tool.poetry.scripts]
myprogram = "mypackage.mymodule:main"
```

The `:` is to indicate a function inside a module. So if this package is installed, you can run it with
```
python -m mypackage.mymodule
```

or simply as
```
myprogram
```

(And yes, Poetry uses "scripts". I guess I'm the odd one out for naming Python programs "programs".)


## More runnable modules

There are lots of runnable modules in packages. The standard library that comes with Python already has several dozen. Some are useful, often for quick tests (running a simple http server or a smtp server), others not so much (anymore).

I'll list a few below; but do search and check yourself when using packages. There may be some hidden functionality that is easy to access in this way.

```
python -m pelican
python -m pelican.tools.pelican_quickstart

python -m sphinx #  `sphinx-build`
python -m sphinx.cmd.quickstart
```

Pelican is the blogging tool I am using for these pages, while Sphinx is a documentation tool. For both, the default runnable package (re)buils the text (from Markdown or Restructured Text to HTML), while the setup commands ("quickstart") are more hidden; which makes sense, because the latter are only used once.

```
python -m unidecode -c "ĥéłlø wöřlð"
```

The Unidecode package provides functionality to replace accented and other non-ASCII letters with their ASCII equivalent. The above is the command line functionality.


```
python -m django
```

This is the equivalent of the `django-admin` executable. If you look at the code for `django-admin` itself: this is just eight lines of Python script, that calls the Django package, which ends up essentially doing the same thing as above.

```
python -m jupyter [console | notebook | lab]
```

Runs the Jupyter notebook, or console, or Jupyter Lab, just which variant you pick. Leaving of the `python -m` gives you basically the equivalent of the Jupyter command (and `ipython` is nearly equivalent to `jupyter console`, while `jupyter-lab` can be its own command).


Black, Pylint, Pyflakes and Poetry, all mentioned in the introduction, are packages useful for development of Python packages yourself. Black is a formatter ("opioniated", as the developers phrase it; there are no configuration options to change its output), Pylint and Pyflakes are linters (do read and heed their warnings and suggestions), and Poetry was mentioned a bit above, for overall management of package development.


### Standard library modules

Below are a few examples of runnable library modules I have used occasionally in the past, for testing purposes.

#### Create a virtual environment

```
python -m venv ENV_NAME
```

Creates a virtual environment called `ENV_NAME` in a local directory `ENV_NAME`. Use `source ENV_NAME/bin/activate` to start it, then `deactivate` to stop it.


#### Run a webserver, with the contents of the current directory

```
python -m http.server
```

Runs a simple HTTP server (very insecure). By default, it provides an index listing of the files in the current directory when opening the corresponding IP address (localhost on port 8000) in a browser. This can be useful if you are developing a website that needds some functionality that can't be provided by simply opening a HTML page directly in a browser; for example, when testing an AJAX or similar query (though you wouldn't get a responsefrom this server).

#### A quick timing test

```
python -m timeit "<some python code>"
```
Timeit can be used on the command line to easily test some one-liner Python code. You can tweak various parameters, and even give a setup statement. So you can, for example, do
```
python -m time -n 2000000 -s "import math" "math.log(5)/5"
```

#### Test sending emails locally

```
python -m smtpd -c DebuggingServer -n localhost:1025
```
lets you test sending emails locally: it will output the details and text of the received email in the terminal. I've occasionally used while developing a Django application, so that I could simulate people signing up and receiving a confirmation email: the email would be send through this smtpd server, and its output would appear in the terminal.

Note that the `smtpd` module will in the future (from Python 3.12) be replaced by the `aiosmtpd` package, which is an external package.


#### More stdlib runnable modules

There is a whole list of modules in the standard library to try out yourself (some will have a `--help` option as well):

```
python -m pprint

python -m profile

python -m pstats

python -m pyclbr

python -m py_compile

python -m pydoc

python -m quopri

python -m random

python -m rlcompleter

python -m runpy sysconfig

python -m site

python -m smtplib

python -m sndhdr

python -m sysconfig

python -m tabnanny

python -m telnetlib

python -m tokenize

python -m tarfile

# non-functional: python -m textwrap

python -m trace --count -C . somefile.py

python -m webbrowser

python -m zipall

python -m zipfile -l/-e/-c/-t somefile.zip
```
