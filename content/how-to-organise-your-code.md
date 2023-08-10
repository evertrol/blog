Title: How to organise your code
Date: 2022-10-18
Category: Code, coding
Status: draft
Summary: How to organise your code


# Intent


# Directory structure



# Repository




# Testing

## Unit testing

- Use a suitable testing framework for your language. As with any dependency, check how up-to-date the framework is, if it's easy to install for other users, and if it has good documentation.

  - Python: (pytest)[https://pytest.org/] is well known and used, and provide many options. The standard library `unittest` package tends to be more cumbersome. For more automated testing. (tox)[https://tox.wiki/en/latest/] may be of use.

  - C++:

  - Julia: Julia has (unit) [tests built-in](https://docs.julialang.org/en/v1/stdlib/Test/). See also [the documentation on adding tests to a package](https://pkgdocs.julialang.org/dev/creating-packages/#Adding-tests-to-the-package).

  - Rust: Rust has unit tests built-in. See [the documentation](https://doc.rust-lang.org/book/ch11-00-testing.html), or the (examples)[https://doc.rust-lang.org/rust-by-example/testing/unit_testing.html].

  A more complete list can be found at, for example, [Wikipedia](https://en.wikipedia.org/wiki/List_of_unit_testing_frameworks).

## Installation / deployment testing


## Integration testing

Testing the full code, with short sample input and comparison output data. May run for at most a few hours, probably a lot less. The output comparison can be limited to certain specific selection of the output data that are representive. The format of the output data (e.g., dimensions or data type) should of course also be tested.


# Documentation

Start with a simple README file, which is especially useful on sites such as GitHub, where the README is nicely rendered (provided the extension corresponds to a file format: `README.md` for Markdown and `README.rst` for REStructured Text are the common ones). An extra (short) section can be added to show some examples or results of the code in us.e

The README should contain a one-line sentence what license is used (the full text is in a LICENSE file). For example: "This software is released under the Apache License, Version 2.0 (https://opensource.org/licenses/Apache-2.0 )".

The README file should have a brief overview (one, two paragraph(s)) what the software is about, and a few paragraphs about the installation process. The latter paragraphs would include dependencies to be installed (or that will be installed by any installation script, but so that the user is aware of it), the actual installation steps, and a note on how to test the installation.

A usage section is also necessary: it shows the necessary steps to run the software, including several examples. Details may refer to actual documentation, such as all the details of an extensive input parameter file.

A longer README should have headings to easily navigate to relevant sections. If the README becomes very long (say, 2-3 screen pages, when rendered on a repository site), move the relevant sections into their own files (`INSTALL.md`, `USAGE.md` etc). Keep brief installation and usage notes etc. in the README file, with pointers to the other documents (releative links can work, depending on the repository site).

Of course, at some point, all the documentation will have to be put in its own directory. `docs/` or `documentation/` is a good choice. It may be practical to keep an `INSTALL.md` or `USAGE.md` file in the main repository (the README file should always be there), but with the same or more detailed instructions in the `docs/` directory.

## Documentation software

- MkDocs

- Sphinx


### API documentation

- Sphinx

- Doxygen


# License

If you are publishing your software to the world: provide a license!

Stick to a well-known license. Don't invent your own, since you're guaranteed to overlook some issues, and then people may puzzle about what is meant (mostly if it is to be distributed through other means, such as in an OS package).

Among the well-known ones are

- GNU public license (GPL) v3. The software is free to use, but any changes should be noted and made public. There is also a special license for libraries, as to whether these can or can't be used together with non-free software (LGPL).

- MIT license / BSD 2-clause license. These licenses are nearly the same. The software is free to use, with attribution, but any changes by others do not have to be made by public. This allows for easier use in commercial applications (for example macOS is derived from BSD, not Linux, in part because of the different licenses).

- Apache v2. Similar to the MIT and BSD licenses, but also handles possible patent issues (someone may have contributed code that is patented by that contributor, but the contribution can be used free of patent issues. Specific algorithms may fall into this case).

  The Apache license tends to be a populair choice for scientific software.

- Public domain. No attribution is necessary, and the software is free to use by anyone, for anything. SQLite is an example of software with this license, and is used both commercially and open source everywhere. Generally though, having an actual license is clearer.

More restrictive licenses are possible, but with open source, you probably want to stick to one of the above licenses. Check with your institution what software licenses are permitted or preferred.

If you don't provide a license (and don't note the software as being in the public domain), technically, the code has an exclusive copyright, and no-one can use it.

For more details, please see https://opensource.org/licenses , which also has a FAQ.

Note that it is possible to change the license, if you're the copyright holder. But do this with care, if you have to.


## Copyright

Copyright should be mentioned in the license. The copyright pertains to the owner of the software, which can be a single person, but also often is an organisation or institution. If you are being paid for writing software by an institution (often the case for scientific software), the copyright holder is probably that institute.

The copyright often comes with a year when it was first released; you don't need to increment the year each time, since the copyright holds for a reasonable amount of time.

## Authorship

Authorship is different from copyright: it pertains to the person(s) who wrote the software. Any contributor can be an author this way, so it may be up to the project whom they accept as an author.

## Changes to the license, copyright or authorship

All of the license, copyright or authorship can change. The license can become more or less restrictive, the copyright may go the different institute, and more authors can be added (or an author may withdraw their authorship).

Often, the older license(s) or copyright(s) are still left, with years indicating their validity period. For example, Python has multiple licenses for different years, plus some additional licenses for several of its library packages. Overall though, it's best (easiest) if you can stick to one license (one that contributors can agree with).


# Repository II
