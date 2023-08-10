Title: Configuration files
Date: 2023-02-26
Category: 
Status: draft
Summary: Suggestions for and caveats about configuration files

# Configuration files

Configuration files are a practical, and probably essential, thing to have your code run flexibly. A good configuration can prevent lots of tiny (or large!) errors, and make it easier for other people to use your code (or you yourself if you haven't used the code for a while).


Generally, there will be configuration files, to change things like 
- starting configuration (of a simulation)
- output file names, directories or formats
- what to calculate or process (steps to take, steps to skip)
- what to output (some calculated parameters may not be interesting for most calculations)
- logging setup: log file(s), logging level

For very simple things, you can create a simple text file, change settings there, read the file and process it. Alternatively, you can have it at the start of your program in code, change it, recompile as necessary, then run it. Both work for very simple things, but can quickly get out of hand, become cumbersome and errorprone as things grow. You may to use a good configuration file format from the start instead.

Nearly always, the configuration file should be a text file. Probably with key-value pairs, where the keys (parameter names) are preferably just ASCII characters, or otherwise straightforward letters. An underscore and numbers will also work, but not just by themselves: that will be just to unclear. I tend to follow standard variable naming rules for keys. ASCII characters prevent confusing and avoid searching on how to input accented or other characters. Of course, plenty of people use non-ASCII characaters, or non-Latin characaters, on a daily basis. But ASCII is so prevalent in code, that it makes sense to stick to that initially. Personally, I often find `phi = 55.5` to be more readable than `ɸ = 55.5`. 

Note that binary values don't really belong in a configuration file. If any are needed, these should probably be stored in a file, and the file should be pointed to from the configuration file. Be sure to have the file format documented somewhere (although it will be indirectly documented in the code that reads it). As for floating point numbers and their inherent inaccuracy in computer programs: if this becomes an issue, then consider rewriting the input of the configuration file, possibly by scaling parameters appropriately, or put them in a binary file (but that hides the actual values from easy inspection). Generally though, this shouldn't be an issue, as the code should have ways to properly deal with floating point numbers, and a single value in a configuration file shouldn't matter (e.g, the configuration value may be multiplied by another number in the code, and then both inputs, and the result, are all likely to suffer from floating point inaccuracies. Having the configuration value in a binary format will not matter here).

You also want to avoid actual code in an input file. It can be tempting and convenient to have users define e.g. a short function in the input file, and then, if you're using Python, use (`ast.literal_`)`eval` on that code to run it. But code should be inside your code base, and any such changes can either be made through configuration parameters, or by adding it to the code base. In the latter case, there are more possibilities for control of the new code, such as code review and tests, which would otherwise not be possible.

I strongly recommend to *not* reinvent the wheel: don't come up with your own configuration file format. There'll be specific settings, like several list of numbers, that you feel may not be suitable for standard configuration formats; or you may already have a code base with its own specific configuration format. Still, it will be worth your while to do some searching for a proper configuration file format that can handle such things, and use that instead. Sometimes, a little rewriting of the configuration settings can make things much cleaner in the file format.

Good use of sections is also important, or even the use of subsections. Don't overdo it, and don't use several layers of sections: that will make it again harder to read. But clear sections make searching for parameters a lot easier, especially if parameter names happen to be re-used in different sections.

A configuration format that allows for comments is also convenient. Comments may remove the problem of having to look up what a parameter is for, and can have some examples of valid (or invalid) values of that parameter.

In code, the configuration will be an object, and will likely all be a nested amalgation of lists and dicts (in Python parlance), consisting of integer and floats, and possibly some booleans and date-time values. A good configuration file format, with appropriate library routines, will be able to allow for such values, and convert them into the right in-code format. Some configuration file formats allow for things like references, so that repeated sections are less necessary, or other re-use of values in the configuration file (e.g., string interpolation in configparser ini files). These can be a convenience, but may also complicate things, having to look up the actual value, or making it harder to tweak a single value in a referenced section.

I regard configuration files as read-only, that is, the program shouldn't really (re)create the configuration file from the in-code configuration object. The reason is that this may change sections or keys around, confusing users (even if it's not a problem for the actual configuration). Some formats even allow for multiple ways of writing the same (sub)sections, which can be confusing, and makes documentation and examples look differently, even if the actual configuration is the same. What I tend to do, is write the default configuration as a single large string in the code (Python's triple-quoted strings are useful for that), and parse that in the usual way to get a default configuration. The string itself is simply printed to provide a user with a starting point for their own configuration file.

One thing to consider is whether to always require a fully-fledged configuration file, or a configuration file with just relevant (changed) parameters. In the latter case, you'll need to update the default configuration object with the changed configuration file. This may be straightforward, but in case of a nested dict and more complicated, this could become tricky, as you would have to recurse through several levels to adjust the right key-value. If you're lucky, the accompanying configuration file library provides such a routine; otherwise, it requires some (careful) programming. The alternative, to always require a full configuration file, makes this a lot easier. It also has the advantage that it is always visible what every parameter is: there is no need to know the default configuration, or look it up in the documentation.

One convenience option you may want to consider is whether some command-line options to your program can override parameters in the configuration file. This is really a convenience for the user, but it has the disadvantage that the configuration file for a specific run of the program is not the actual configuration: the final configuration will need to be saved with the results if reproducibility is required (which may seem to go against the read-only style mentioned earlier). See the section on provenance and reproducilibity about this potential problem.

## Suggested configuration file formats

There are dozens of configuration file formats. Below, the most common ones are listed, with some advantages and disadvantages.

### TOML

My preferred configuration file format is TOML (which is an acronym for Tom's Obvious Minimal Language; Tom being the person who came up with it). It is fairly freeform, but does allow (or require) strict types of values, such as integers, floating point numbers (including infinity and not-a-number values), strings, date-time objects and booleans. This makes for safe handling of configuration files, with less chances of accidental mistakes. 

Sectioning can be done using so-called tables, which transform into dicts in Python. You'll end up with a nested dict. Lists (called arrays in TOML) are calso possible, as well as multi-line strings and comments.

It is possible to do weird things, such as having empty keys, heavily nested tables, dotted keys (which result in nested dicts) with lots of spacing around the dots. The usual advice applies: avoid it, and stick to a simple configuration file.

Python 3.11 and later have a `tomllib` module built into the standard library. This is a read-only module: the flexibility regarding tables in TOML makes it nearly impossible to output the same configuration file as an input file, when going through a configuration object. There are separate Python packages for TOML files that preserve the format, such as [`tomlkit`](https://pypi.org/project/tomlkit/). 

See the [`tomllib`](https://docs.python.org/3/library/tomllib.html#module-tomllib) documentation for more information (note the conversion table at the bottom of the page), or the documentation for [the TOML format itself](https://toml.io/en/).


### INI / Configparser


### YAML

YAML allows for a flexible, deeply-nested, configuration format in the form of associative arrays (dicts) and lists, with single values such as strings, integers, floating point numbers and booleans. Unfortunately, its flexibility in interpreting values also means it can cause unexpected errors: the classic example is the ["Norway problem"](https://hitchdev.com/strictyaml/why/implicit-typing-removed/), where the string "NO" should be the abbreviation for Norway (in a list of country abbreviations), but is interpreted as a boolean false value.

I dont' use YAML because of these potential errors; its flexibility also means you can reference whole blocks: convenient, but they can be confusion when you can't find the anchor belonging to the reference. And ultimately, it is possible to execute code through a YAML input file. That is not what you want: don't have code in an input file.

If you do use YAML, I strongly suggest to use only the StrictYAML set of features, and the corresponding parser.

There are no YAML modules in the Python standard library, but [`PyYAML`](https://pyyaml.org/) is near ubiquitously used (note that it's imported as `yaml`). For StrictYAML, you can use, well, the (`strictyaml`)[https://hitchdev.com/strictyaml/)] package.


### JSON


### Text

Text configuration files likely consist of simple lines in a `key = value` or `key value` format. This works for the simplest configuration files, and, for example, plenty of Linux system programs make use of this format. But as stated near the start of the section, I don't recommend using simple text files. 

It generally requires parsing the lines yourself (which is not difficult, but still; add comments, blank lines and a few other options to the list, and the parsing code quickly grows), but there are no checks on the type of `value` (it is always a string). If you also code the conversions yourself, you'll want to keep track of the line number when throwing an error. And list values complicate things further.

INI/Configparser files are close to plain text files, and should probably be preferred over simple text files, as the configuration file grows. From there, it may be a relatively small step to use TOML files.

### Code module

One very flexible option, is to use actual code for the full configuration (in contrast to a single bit of code in a configuration file, as mentioned earlier). This works best for programming languages that essentially compile on-the-fly (or nearly so), and can easily import/include a file as a module. Python is the prime example, but this would also work for Julia, while far less so for compiled languages such as C, C++ or Rust. In the latter cases, you would have to compile the file to an object file, then link it to your program (it's still possible, but less convenient).

The clear advantage of this is that you have a lot of flexibility, to allow for all types of configuration values. Conversion from the configuration file to values like booleans, numbers, date-time objects, lists, dicts or more exotic objects is also not necessary, as this is already how the configuration is entered.

The obvious disadvantage is that there are fewer checks on the correctness of the input (unless you code such checks yourself), and that it may be overly flexible.

The example were I know this is used, is for Django (a web framework) projects. There, I have used it myself with extra conveniences, such as splitting the Python configuration module up into multiple modules (basically making it a configuration package), which can be flexibly imported as necessary. It can also set set paths flexibly, deduced from e.g. the location of the configuration file itself.

While listed at the bottom of the formats, this would be my second preferred option, in particular if the flexibility is required. Be careful to document carefully what is possible for the options, since initial checks on the correctness of values are not present.

An example for a Python project is as follows:

```
project base directory/
|
+-- myscript.py , that calls the package/code to run it
|
+-- config/
          + __init__.py
		  + base.py
		  + local.py
```

The script doesn't need to import the config package. It would just need to import the actual package. That would then try and import a config module:
```
try:
    import config
except ModuleNotFoundError:
    # Set default configuration
```

Because the `config/` directory is in the same base directory as the `myscript.py`, Python is able to import it as a package (if these are not on the same path, you may have to tweak your `PYTHONPATH` environment variable). The `config/__init__.py` could then look as follows:
```
from .base import *
try:
	from .local import *
except ModuleNotFoundError:
	pass
# More optional modules
# try:
#     from .optional import *
# except ModuleNotFoundError:
#     pass
```
This would have all the settings stored in `base.py`, but have them overridden as necessary by settings in `local.py`. This way, depending on how you store the current project, you can have `base.py` in version control, while `local.py` is really local to the machine, and not in version control (`.gitignore` could contain a line `config/local.py`).

The actual package could require that `import config` always succeeds: if it fails with a `ModuleNotFoundError`, the program should simply stop and exit. The `config/base.py` can then contain the default configuration, with the `local.py` file and/or other modules overriding select configuration items.
