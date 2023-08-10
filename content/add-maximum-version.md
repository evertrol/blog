Title: An introduction to Git
Date: 2022-10-18
Category: Git
Status: draft
Summary: An introduction to Git


# Add a maximum version specifier to your project

Lots of projects have dependencies and specify minimum requirements for those dependencies. These are often used automatically by the installation process.

For Python projects, this may be in the `setup.py` file, like
```
setup(
    ...
	install_requires=[
        'Cython >= 0.22',
        'numpy >= 1.22.2',
        'scipy >= 1.6.2'
	],
...
)
```
or in a pyproject.toml file, like
```
dependencies = [
    'Cython >= 0.22',
    'numpy >= 1.22.2',
    'scipy >= 1.6.2'
]
```

That looks fine. After all, future versions of those software will perhaps add functionality, but they won't take away functionality.

Except that it isn't fine. There is no maximum version, and once a dependency changes it major version number (the first number, before the period), all bets are off (as the Python 2 to Python 3 transition has shown).

Notice how I put Cython there as a dependency, with a minimum requirement of version 0.22. Well, Cython has just released version 3.0.0, and not everything of that version is backwards compatible with the 0.22 version, or the 0.23, 0.24 etc versions. (Note that Cython went from a very long time being version 0.x to version 3.x.y. I don't know why they skipped 1.x.y and 2.x.y; possibly to show Cython is compatible with Python 3.

As a result, software that relies on certain specifics of its dependencies (as is normal), may fail to work, build or install when such a dependency releases a newer version.

**Thus, always set a maximum version dependency as well.** It may be very simple, just the same major version.

For the Python eco-system, there are two ways to do this. You can use multiple specifiers for the same dependency, separated by commas. That would look like
```
    'Cython >= 0.22, = 0.*',
```
The other option is to use the "compatible release" specifier (it's in the name), `~=`. That looks like

```
    'Cython ~= 0.22',
```
which is, for all practical purposes, the same as above. It keeps the version before the last period the same. Another example, for explicitly requiring SciPy 1.6.2 or later, but *not* 1.7 or later, you can use
```
	'scipy ~= 1.6.2'
```

A note on the 0.x(.y) versions: versions before a 1.0 release are often more flexible, and backwards compatibility between, for example, version 0.7 and 0.6 is not guaranteed. After a 1.0 release, compatibility for the same major version should be guaranteed, although not all software is that good in adhering to this.


Some people go as far as to specify a fixed version for each dependency. This is good for reproducible results, but it will miss out on bug fixes and other (minor) improvements in the dependencies. It also skips the possibility that a compatible version of the dependency is already installed (for example, NumPy), and will install an (older) version of the same dependency. Of course, this is the whole point about virtual environments: each environment has its own specific dependencies. (And disk space, bandwidth (downloading) and a bit of extra time are supposedly not to restrictive to create a new virtual environment for each software you install.)

There is a potential problem with strict requirements, if some dependencies require other dependencies (SciPy requires NumPy), and these dependencies have also fixed their dependency. Now you've ended up in dependency hell: the main software you want to install requires NumPy 1.22.2, but, for example, SciPy version 1.6.2 requires (for example) NumPy version 1.21.1. With exact version specifiers, you get a conflict that can't be resolved, unless you manually tune the SciPy or NumPy requirements. Which means altering the (setup) code of the software you are trying to install. (Not to worry, SciPy 1.6.2 has more releaxed NumPy version requirements than this example: NumPy has to be between versions 1.16.5 and 1.23.0.).
