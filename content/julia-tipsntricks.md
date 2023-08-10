Title: Julia tips and tricks
Date: 2022-12-06
Category: Julia
Status: draft
Summary: Practical things to know when starting out with Julia


## Packages

### Install a package, view installed packages (and their status), updating packages, or removing a package

```
using Pkg
Pkg.add("PackageName")
Pkg.update()
Pkg.status()
Pkg.rm("PackageName")
```

### Interactively adding packages

Type `]`. The prompt will change to `(@vx.y) pkg> `. You can now run commands such as
```
add PackageName
update
status
rm PackageName
```

To return to the normal prompt, press backspace or delete (Mac) at the prompt.

More information in [the Julia Pkg documentation](https://docs.julialang.org/en/v1/stdlib/Pkg/).

## Updating Julia

You can download the latest version from https://julialang.org/downloads/ and install that over your current version.

Alternatively, start Julia with admin access:
```
sudo julia
```

then run
```
using Pkg
Pkg.add("UpdateJulia")
using UpdateJulia
update_julia()
```

You may have to update or check your existing packages.


## Source code

### Formatting

```
using Pkg
Pkg.install("JuliaFormatter")
using JuliaFormatter
# Format all files in the current directory
format(".", always_for_in=true, remove_extra_newlines=true)
# Format a selected file
format_file("example.jl", always_for_in=true, remove_extra_newlines=true)
# Format a string
format_text(a_string)
# Format files in a package
format(PackageName)
```

`format()` and `format_text()` return `false` if the output is different than its input, otherwise it returns `true`; `format_text` returns the formatted string.

Without `always_form_in=true`, some loops may be styled as `for i = 1:10`, instead of `for i in 1:10`.

Details in [the JuliaFormatter documentation](https://domluna.github.io/JuliaFormatter.jl/dev/).
