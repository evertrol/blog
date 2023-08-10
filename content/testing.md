Title: Testing your code
Date: 2022-12-06
Category: Julia
Status: draft
Summary: How to test your code, to minimize (unnoticed) errors


# Testing your code

The first tests will be done while you work on the code: it's simply running the code for a short while, for a minimal simulation or on a small (but representative!) selection of your data. This is likely to be iterative, until you have something that works. Or at least, it seems to work. The final test is to run your code in "production", but there is no guarantee that this provides the proper results: there may be an algorithmic error (which would be independent of your code), but there may also be more subtle coding errors. The latter can be hard to find, or even to notice, in particular when the output is close to what you expect.

To find such errors, more rigorous testing is required. There are several things you may want to do:

- address compilers and linter warnings

- targeted unit testing


## Addressing compiler and linter warnings


### Compilers

Compilers have had several decennia to be developed (even recent compilers borrow from existing compilers), and are therefore quite good at noticing things that may cause problems, but that one person may easily have overlooked. 

First, make sure you use appropriate flags when compiling. For example, for C and C++, I prefer the `-Wall` and `-Wextra` flags (works with both `gcc/g++` and `clang/clang++`) for "all warnings" and "extra warnings" (yes, "all" doesn't really mean all. There is even an `-Weverything` flag, but that can produce pages of irrelevant warnings. I used it once, then decided to not use `-Weverything`). These warnings are often useful, at least to some point. Do heed them, and don't ignore or otherwise silence them, unless you really, really know what you're doing (as I said: compilers are really smart, and will try and protect the code, also from future errors).

Compilers can and will optimize parts of your code. If there are subtle bugs in your code, the compiler may find a shortcut that is valid for your intentation, but is valid for the buggy code. A classic example is when the compiler detects certain code has undefined behaviour, and it may just optimize the code away (that is, the code is removed in the final result); though you'll likely see some warnings as well. 
While such problems can be hard to find, try compiling both without (`-O0`) and with optimization (`-O3`), and see if you get the same result. Of course, without optimization, your program will take quite a bit longer to run, so find short but representative use cases.

Finally, use a fairly recent compiler standard. C11 (or even C17) is a good minimal standard to use with C, while`-std=C++11` should be the minimal standard to use with C++ code (not all compilers will have implemented the C++20 or C++23 standardsfully, but C++14 and C++17 should also be possible for most platforms). This prevent you from archaic usage, and while that is not a problem an sich, newer standards have better tools to make programming easier and safer. Some new utilities also help making code clearer and thus can prevent errors (such as designated initializers for structs in C99 and later, where you can use the field name in the struct initialization. That prevents you from accidentally mixing two integer fields, for example).


### Linters

Linters are programs that run through source code, issuing all kinds of warnings and suggestions to improve your code. They used to be quite standard a few decades ago, but compiler warnings are now so good, that they have essentially taken over linters jobs (though linters can still suggest how to clarify your code).

For non-compiled languages, or rather, once that are effectively compiled during runtime, linters may have more use: they act as a warning system for potential bugs that otherwise would only appear (if at all) when running the code. Since linters can also make suggestions on how to rewrite your code for clarity, some linters can be rather verbose, and you might be inclined to ignore them completely. Try and find a setting to limit their verboseness, or at least glance through all the messages, so you can pick out the important ones.

For Python, several linters exists, with various degrees of verboseness and strictness:

- flake8 is a popular one, that is relatively mild in its verboseness. Usually, it is easy to heed all warnings and notices outputted by flake8 and fix them.

- pylint is much more verbose. It will point out errors, warnings, but also suggestions. Examples are variable names that are too short (less than 3 letters, excluding the standard `i` and `j`); rewriting long functions (which is good thing by itself, but generally doesn't help with error preventation.

Of course, for Python, one thing even a linter can help you with, is an accidental indentation mistake. Compare
```
a = 1
if a < 2:
    a += 1
a -= 2
```
and
```
a = 1
if a < 2:
    a += 1
    a -= 2
```

Here the mistake is rather obvious, but with some code in between, it's easily overlooked (then again, a linter in that case might point out that there is a long if-branch, and it is better to put that in a separate function. In which case, this error should become more obvious, since now the `a -= 2` line has completely disappeared from this part of the code).

The example above also brings me back to compilers, or rather languages that uses braces `{}` to separate code blocks: *always* use braces. Avoid lines such as `if (a < 2) a += 1`, but use `if (a < 2) { a += 1}` (probably spread out over 2 or more lines); search for "Apple goto fail" for an example of what can happen. Which brings me to the last bit of this section, which is not so much about warnings, but still good practice.

### Code formatters

Good code is consistent. Not just in its usage, but also how it looks. Good code must be readable, and that makes it easier to spot easier. If you happen to write (Python) like this:
```
a=0
if a<2:a+=1
a-=2
```
then your code will quickly become unreadable. Whitespace (spaces, empty lines) are a good thing. Use indentation *also* when using braces; and don't skimp on it: 2 spaces of indentation is too little: larger indentations can easily show that you have too many nested blocks, and that you may want to refactor the inner block(s) into a separate function. 

Similarly, line length should not be overly long. These days, with large monitors available, it is easily possible to cram 120 characters (with or without indentation) on a single line, but at some point, you loose track of which line you are working on. And when you then later try to read the code on a small-sized laptop, the line may wrap, which makes it look even more confusing. If you have very long variable or function names, try to see if you can use aliases instead. Nobody writes `matplotlib.pyplot.scatter(...)`, but `import matplotlib.pyplot as plt` and then `plt.scatter(...)` (do use common aliases, don't invent nonobvous ones yourself. And be weary with `using namespace std` in C++, as that is generally not recommended). Of course, if you're writing Java, this may not be feasible; sorry.

The best option, however, is not to do this by hand (or not fix it by hand): use a code formatter that is (somehwat) standard for the language you're using. For C and C++, `clang-formatter` can be used, which has different styles (and you can adjust each style). For Python, `Black` has become more and more the norm: it has no configuration options, you just have to accept what it formats your code to; it may not be to your liking, but it is consistent, not just in your project, but across the whole (Python) world. Newer languages often provide a formatter alongside the compiler, or within their larger ecosystem. Rust has `cargo fmt` (needs to be installed separately from the ecosystem). For Julia, there is `JuliaFormatter`.

## Unit testing

The previous section is a bit more about error prevention before you have even compiled your code. Unit testing deals more with testing small pieces (units) of completed and compiled code.

Unit tests often have their own little section in a library or package. They usually testing the smaller functions of your code (that is, functions that don't take minutes or more to complete), which serve as the building blocks of your overall code. That also means that if you do have an essential but larger and long-running function that you'd like to test, you may want to split it up and refactor it into smaller functions.

Unit tests should be written for code that is technically compiled and installed (it doesn't have to actually be installed, but they should work as normal code would work). Since unit tests will need to call functions from your code, the majority of your code will likely need to be a library or package, where all the functionality is located.

Unit tests run these functions with specific input, and a specific, expected output (or other outcome, such as a file on disk). Comparing the expected output with the actual output will show if there is an error within the function. If so, you'll need to find and fix the actual problem, so it's convenient that unit tests work on small pieces of code: the error is easier to find.

Since unit tests have a given input and expected output, you can use them, among others, to verify the correctness of an algorithm implementation: find some important inputs and outputs for the algorithm, and use that to create a unit test. Specific values you could always consider for numerical algorithms are 0, 1, -1, infinity, -infinity and NaN. Even if some of these values are outside the problem domain, testing your function with them as input may make that function more robust. And while something like a NaN is almost guaranteed to show up in the output, an early warning, flag or complete stop from the program can often be better than finding a NaN in your output after running your code for several hours or more. Other specific values to test for, depending on the input, are empty arrays, empty strings, null values (null/nil/None), minimum and maximum integers (to test for e.g. integer overflow), or dates that are incorrect, very early, or of course the not-so-relevant-anymore Y2K problem and the Unix-time problem.

When writing tests with multiple different inputs (and outputs), you *parameterize* the unit tests. A good testing framework (use one if you can; see below) can help you with that, so be aware of it and look for how to avoid code duplication, also for unit tests.

Unit tests can also prevent future errors, if you are changing existing code. If there isn't already a unit test for the relevant piece of code, you can write a number of tests, then change the code, and rerun the tests and see if these all work. While it is rarely a 100% guarantee, this picks out refactoring errors pretty quickly.

The counter to that is that you write unit test for each and every function, with all possible inputs, and do that even before the actual code is completed. This results in test-drive-development, and while it can create very safe code (to a point, I guess), it is a very slow and inconvenient process. Unless you're launching a satellite, this is probably not the way you want to write your code.

One advantage, though, of writing a few tests beforehand, is to get a feel for what the function should actually do, and what it should return. Should it return one value, or multiple? In case of an error, should it abort early, stopping the program, or issue a warning, and return a flag and and an incorrect value?

Unit tests can also serve as tiny examples of how to call a certain function, and what to expect in return. This is most useful if you are developing a library with functions that other people also use, but you haven't gotten around to writing proper (API) documentation yet. This will depend a bit on your workflow: the code itself might be enough, there may already be documentation, or you have better, documented, examples than unit tests.

### Unit tests frameworks

Most languages will have a framework for creating unit tests. This can help to parametrise unit tests, as well as providing an initial setup and teardown; they often also provide convenient ways to test for errors that should occur (i.e., test if the proper exception gets raised for invalid input). For Python, there is the built-in `unittest` module, but I recommend using pytest, which makes it easier to set up tests, run the tests, parametrise them, test for exceptions, and more. `nose` is also a well-known Python unit test framework, but pytest seems to be the most common one these days.

Rust has unit testing built-in. For C and C++, the Googletest suite may be help. But there are numerous unit test frameworks for C and C++. For a listing, also for other languages, start by having a look at https://en.wikipedia.org/wiki/List_of_unit_testing_frameworks . If you pick one, do check that it is a framework that is still being used widely and still being maintained: this helps when you run into problems with using the framework, or installing it somewhere else.

## Continuous integration and installation testing

Once you have set up a (selective) set of tests, you'll want to run them from time to time. Mostly, when you've made notable changes to your code. Some unit tests may not be relevant to those changes, but if you set it up correctly, running the tests shouldn't take more than 10 minutes.

If you are using version control, and store your code somewhere on a server (you should: version control has a bunch of benefits, plus you have a backup somewhere), then you might be able to set up things on that server (from a user side) that will run your tests automatically, every time you update the server with your code changes. This is called continuous integration (CI): it integrates testing of your code with the development, all the time.

How to set it up depends on the versioning software (if any) and the server / service being used. GitHub has something called GitHub Actions. For it, you write a configuration file that you add to your repository (mostly just once, with an occasional update). The GitHub server will notice the file, and each time it receives new updates to your repository, it will run a set of commands on a virtual machine (more or less), according to that configuration file. The file is not a direct set of commands, but more indications of what needs to be set up, and then how to run the tests. This allows fairly straightforward testing of different versions of e.g. Python, along with different versions of libraries and packages. You can usually even get it to set up, for example, a specific Conda environment (or more) to run the tests in.

Other services may have other similar CI options, with similar style workings: it allows you to test your unit tests against a matrix of different compilers / interpreters and libraries / packages. You will have to read the documentation on how to set up the configuration file, but usually, plenty of examples exist that can help you getting started. Not all CI services are free; sometimes, your software needs to be in a public repository for CI to be allowed for free, or otherwise, you have to pay a small amount for its usage. Or you can see if there is something else around that you can use. Search around for "continuous integration <service>" to see what is around (service being things like GitHub, GitLab, Codeberg, or perhaps your local university's server).

A bonus advantage is that you can also test your installation procedure automatically. A small change in your setup configuration may not affect the unit tests (the code will be the same), but it may break your installation. Some services allow testing on different platforms (in a virtual machine), although macOS is often not included (because of costs). But if you rely on system packages, testing against various Linux flavours can be helpful.

Such testing also allows you to test the (automated) building of your documentation (if you have any). For example, if the documentation uses information from code files (from comments or the general interface), references could break. It will not put the documentation online for you, but it can definitely check if nothing is broken (note that building documentation may often issue warnings and not errors, so broken documentation stands out less).

If there are any errors, you'll likely get a notification, and there is generally a full build log to read through. Errors (and possibly warnings) will also be highlighted. For warnings, remember that these may not interrupt tests, installations or documentation building, so they may go unnoticed. This will depend on the CI service you used. It is probably good to send warnings (and errors) to standard error, and normal informative messages (to users) to standard output; that way the CI tool can pick up warnings as well (thus not, e.g., `print("WARNING: invalid configuration file")`, since that goes to standard output).



