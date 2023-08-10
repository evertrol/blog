Title: Software versions
Date: 2023-04-30
Category: Versions
Status: draft
Summary: Use proper version naming for your code and your dependencies


# Software versions

Every software should have some version information; in particular if it's public. That makes it clear when changes are introduced, and (as long as the old versions are available) people can use the software safely as a dependency.

## Semantic versioning

My preferred version scheme is simply semantic version, "semver". http://semver.org/ has details, but overall, this amounts to a 3-number scheme separated by dots, like 3.2.1:

- the first number represents a major release version. It indicates the software is typically incompatible with other major versions of the same software. So once you've decided on a version number, you should stick to that as long as your changes are small and don't change how the software works.

- the second number represents a minor release version. It indicates some additions, but should not contain behavioural changes overall in the software. Normally, later minor versions are compatible with earlier ones, since they will have added only extras.

- the last number represents small patches, usually bug fixes. These should have no influence on how the software works in general, unless a bug is so ingrained that has it become part of the expected behaviour (which should be really rare). Using the latest bug fix release for a combination of major and minor version is generally recommended.

The numbers start at 0, and just increase by one for every released major, minor or bugfix release. When 0 is used for the major version, it usually indicates the software is still very much in flux, and its behaviour is definitely not settled upon yet; for 0 major version, it is generally accepted that each minor version may behave differently and break backwards compatibility, in contrast to major versions larger than 0. Patch/bug fix releases should still only fix bugs etc, not change the behaviour.

Note: while this *should* be the behaviour (backwards compatible changes with minor releases once past version 1.0.0, no essential changes with patch releases), not all software follows this scheme properly. I have seen examples where there was a backward incompatible change between versions 1.0.3 and 1.0.4: the authors had rethought their design (obviously, they had released version 1.0.0 too early, and felt that a version 2.0.0 was too drastic. But the patch release change, instead of at least minor release change, caught me off-gaurd).

Also of note, for languages specifically: new keywords introduced in minor versions may break older code. Python 3.5 introduced the `async` keyword, which broke code that uses that as a variable or function argument name, for example. But the `match` keyword introduced in 3.10 is safe from this, since the parser looks at the context to determine the meaning. But this concerns languages specifically, which are different than a library or package; and most of the time, such changes are easily remedied in the older code, since it mostly requires a basic search-and-replace.


### Postfixes to the semver scheme

Then there are the occasional letter combinations appended to the version (sometimes with a dash): "dev" for a development build, which is generally not stable. "alpha" is very similar, also an unstable version, but good for initial testing. "beta" is more stable, and can be used to test with with other software. "rc", release candidate, is to iron out the last fixes and test it on lots of installations. Usually, when a new major release for some software is coming up, you can find versions of that major release appended with these abbrevations in that order, until the actual version is released. For example, Python may have version 3.13-alpha, then 3.13-beta, then 3.13-rc, and finally 3.13.0 (and later 3.13.1, 3.13.2 etc); note that in this example, it is the minor versions for which dev, beta and rc exist, not (just) the major versions.

## Other schemes

Other version schemes exist. For example, a scheme that uses the current date when a version is released. So you'd have 20230615, 20230820, 20231111 etc. I advice against that: it is now not clear when breaking changes are introduced, while with semver it is (or at least, should be). It might look convenient to have the date in the package (so you know how old or new it is), but that really shouldn't matter, and distracts: some old software still works absolutely find today, while the latest software may be a complete mess. The date scheme has (near useless) meta information, but tells a user nothing about compatibility, while semver does.

Various (compiler) languages have versions ("standards") indicated by the year, for example, C99, C++11, Fortran2003. These versions tend to be several years apart, and introduction of new keywords may break some older code. In general, though, the standards are backwards compatible, and the timespan between the standards indicates these are major changes. Also, compilers tend to have flags to specify for what standard you want to compile the code. And again, this concerns languages, not libraries or packages, so it is somewhat different.

My recommendation is to not reinvent the wheel, and use a convention that is already well established.

## Dependencies

