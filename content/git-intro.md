Title: An introduction to Git
Date: 2022-10-18
Category: Git
Status: draft
Summary: An introduction to Git


# Preliminaries

Nearly all of the below assumes that you are using a command line, and that you have a recent version of Git installed. Test with `git --version`. My versions are 2.32.1 (an Apple-amended Git version) and 2.34.1 on Ubuntu 22.04. Since I also have access to Git 1.8.3.1 on a Linux system, I'll point out where things don't work for older Gits.

You should be able to use the command line in a unix-style environment, with most common commands such as `ls`, `cd` or `echo`. You should also be able to start a text editor from the command line. The reason for all this command line work is that you can hopefully more clearly see what is happening, instead of doing it through some other application, which may hide certain options or commands behind a (graphical) user interface.

Code, textual output and commands are shown in a fixed-width font with a different background.

# The use of Git

Git can be used for a number of things.

For me, it is mostly a nice way of keeping track of small changes in software I write. If I make a mistake, and I notice it quite a bit later, it can be easier to go back to that mistake and fix it. If the mistake is less clear, git can make it easier to find out what the actual mistake was.

Moreover, it can be a (very) useful to work on developing a piece of software with multiple people, where work may overlap. That is, not everyone has to do completely separate parts of the software.

Then, there is the convenience of various services online that can store your code and, if used with Git, also keep track of the changes; additional services such as bug (issue) tracking can directly point to certain commits with html links. Such services also make it easier when using git to collaborate with other people on the software (also publicly or privately) .

Further, it is nice to see a continuous series of (small) changes in your software when you check the log of changes. It gives a small feel of accomplishment when you see all the edits you've made over the past months to your project.

> **What does Git mean**

> Git doesn't mean anything in particular. It is not an abbreviation, and at best a proper name, thus capitalized. The name was chosen (according to legend) by Linus Torvalds, because he likes to names things (software) after himself (such as Linux).

# Starting with Git

Note: it will be a while before actual files are stored. There will be a bit of setup first, but that will quicker every next time in practice.


To start, change to the directory with your software, and type
```console
git init
```

This will set up a Git repository. A repository is basically a collection of files, in this case with versioning added. Git does this by storing all information in a `.git` directory in that repository. Therefore, don't change things in that directory!

Recent versions of `git` will show a few paragraphs about the name of the branch (what a branch is, is explained a bit later on). In recent years, there has been a change in the naming scheme, away from the use of `master`. Git still uses the old ones, but lots of organisations and people have started using another default name. Most of the time this is `main`; `develop` or `trunk` are also used (GitHub uses `main` as default). If you want to change the name, do as the message says: `git branch -m main` or similar. Don't pick anything fancy, because that will confuse people if someone else looks at your repository.

# Adding files

First, check that Git knows about the directory and its files and subdirectories:
```console
git status
```

It will show your files (never the directories by itself), under a heading "Untracked files", and possibly in red (to indicate files that Git is indeed no tracking). Note that the `.git` directory is not shown: it is automatically ignored by Git itself (and automatically stored in the repository).

You can add files that Git should keep track of, with
```console
git add <file1> [file1, ...]
```

Now doing `git status` will show these files under the heading "Changes to be committed"; for me, they also show up in cyan. These are not yet fully stored (committed) to Git: there is an intermediate stage where you add changes (in this case, whole files), without yet storing them in Git's versioning.

You can keep adding files, one by one, in bunches, or all in one go. But there are more convenient ways, as detailed below.

# What files should Git track

Note that Git doesn't really store files: it keeps track of changes in files. Of course, with the very first commit, it stores the changes going from an empty directory (the basic starting point) to an initial set of files, so effectively, the files are still stored.

You don't want to store all files in a directory. Don't store:

- build products, such as object files, executables, byte-compiled files

- backup files (note: Git is your backup!). For me, this would be emacs `*~` files.

- editor configuration files, such as `.vscode` or `.editorconfig` files. (See below for a bit more on this.)

Instead, store

- source files (that can recreate other files). This can include helper files such as `Makefile` or `setup.py`.

- documentation (again, only the sources files, for example, Markdown files, but not the rendered HTML files)

- Installation and Readme files

- A software license(!)

### A note on the editor configuration and similar files.

An editor configuration file is not a project file, even if some teams may require a certain editor or IDE, for whatever reason. That seems unnecessary to me, as well as an editor configuration file.

There is also the [`.editorconfig`](https://editorconfig.org/) file, which is supposed to be a generic editor configuration. I suggest not to this in a repository either.

Most of these configuration files deal with indentation settings. But this can (and should, in my opinion) be handled differently:
- At least make sure there is a style guide for the project if you care about that, and let (other) users handle things themselves.
- Use either a defined formatter (to be run every time before a commit) or use pre-commit hooks (see later in this document) to handle formatting and verification of the style guide before a commit.

## How to prevent storing such files

Git uses a special file, `.gitignore`, that contains "rules" per line what files to ignore when checking for changes. The file works per directory, and recursively. You can thus have a `.gitignore` in a subdirectory, and files ignored in that subdirectory will be those set by the main `.gitignore` and the one in the subdirectory itself.

The rules are fairly simple, and follow a default globbing pattern. So for example, a simple `.gitignore` for a C or C++ project can look like:
```shell
*.so
*.a
*.o
build/
```
The last line ignores a whole directory. In fact, if the project is set up such that all `*.so`, `*.a` and `*.o` files are created in the `build/` directory, you only need one line.

For files that should be ignored, but are more personal to your machine or coding environment (in my specific case, emacs backup files, `*~`), I recommend to use the global git-ignore file; the local `.gitignore` file should only lists files that apply to the project.

The global (user) git-ignore file tends to be `$HOME/.git-core.excludesfile` (the name is configurable; see below on your local Git configuration). Here you can add a line like `*~`. For convenience, you could add things like `*.pyc`, but these are more project related, so probably shouldn't be in the global user git-ignore file.

### Empty directories

Git doesn't store empty directories.

If, for some reason, you want to store an empty directory , one trick is to add a single file `.gitkeep` in that directory, and then commit that file to Git. That is fairly clear and unique, and will work 99% of the time.

There is a nice convenience to that: I gave `*.pyc` files as an example to ignore per project. These are byte-compiled Python files, created from the `*.py` source files. In Python 2, these `*.pyc` files are stored in the same directory as the source files. Python 3 introduced special `__pycache__` subdirectory to store `*.pyc` files, which is easier on the eyes when listing the directory contents. By ignoring `*.pyc` files instead of `__pycache__` directories, the byte-compiled files for both Python versions are ignored. And that results in an empty `__pycache__` directory, to Git's eyes, so the directory is also not stored.


# Git configuration

Git stores its general user configuration in `$HOME/.gitconfig` file. Don't edit this file manually: use the `git config` command to make changes (though it is a text file, so manual editing will mostly be alright, when taking care of indentation and such).

Let's create an (empty) `$HOME/.git-core.excludesfile` and add it to the Git config file:
```console
touch $HOME/.git-core.excludesfile
```
then
```console
git config --global core.excludesfile $HOME/.git-core.excludesfile
```
The `--global` option indicates a (user-wide) general option, so not for the local directory (there is also a `--system` option, for sys-admins. Stick to `--global` in general). The `core` part indicates the section in the configuration, while the `excludesfile` is the actual configuration option in that section. The last part is of course the actual file.

You can see all configuration options with
```console
git config --global --list
```
or
```console
git config --global -l
```

If you happen to be inside a Git repository directory, and leave off the `--global` part, you'll see all options that apply to that repository: both the global and the local ones.

You can also simply view the `$HOME/.gitconfig` file, which may now look like:
```
[core]
	excludesfile = /home/evert/.git-core.excludesfile
```

Other things to add are a name (and possibly an e-mail adres):
```console
git config --global name "Evert Rol"
git config --global email "@"
```

Perhaps you don't get colors on the command line when running Git commands. Try with
```console
git config --global color.ui true
```

I like some shortcuts for git commands, aliases. Since I find `status` already too long to type (you use that command quite a bit), I have aliased it to `stat`:
```console
git config --global alias.stat status
```

Other configuration options and aliases will come along the way in this guide.

# Committing changes

With all the above set up, it is now a lot easier to add files.

First, check the status
```console
git status
```

There may be a lot of files that are now hidden: they will be ignored by the local `.gitignore` file, or globally ignored.

You can still selectively add files, or add the whole directory (recursively!) if you're fine with the selection. These can be added to existing files in the "staging" area:
```console
git add .
```

often again followed by `git status`.

Note that `.gitignore` is also added, which is good practice: while perhaps not part of the code or documentation, it is definitely part of the repository.

Now, we finally can *commit* these files to be stored in the Git repository. This requires a so-called commit message, which can be given using the `-m` option:
```console
git commit -m"Initial commit"
```

"Initial commit" is quite a common first-commit message, even though it's not always the best. More about good commit messages later on.

However, sometimes you want to add a bit more information. If you have already commited the currently staged files, create an empty dummy file and add that:
```
touch dummy
git add dummy
```

Don't run `:::python git commit` yet! When you use `git` without the `-m <message>` option, it will open up an editor. Which editor, depends on the `GIT_EDITOR`, `VISUAL` or `EDITOR` environment variable (in order), or what is set in the git configuration file. When nothing is set, it will often fall back to using Vi (which is often aliased to Vim). This then leads to numerous searches on "how to exit Vi", as people unfamiliar with Vi get stuck in the editor (the answer is `<escape>:q!`. That is, four keys/letters in that sequence. This is the most failsafe way to exit Vi, as it avoids saving any accidental edits).

Provided your editor can be started from the command line (which is where we are running Git), you probably want to tell Git to use your editor of choice. Mine is Emacs, so I use:
```console
git config --global core.editor "emacs -nw"
```

(the `-nw` option to Emacs means it won't open in a new window, but opens instead in the terminal.)

`pico` or `nano` are other simple editors. Most of the time, you want a simple text editor, since you'll be typing plain text, no code.

Now, you can do a simple
```console
git commit
```
and the text editor will open. It will show an empty line, then a bunch of commented-out lines with some guidance. Near the bottom, it will show which files will be commited, and above that, on what branch you are. This way, this interactive commit style can prevent some incorrect commits.

Enter a one-line, brief, so-called commit message that says what this commit is about. A good commit message tends to be 50-60 characters at most; use that as a guideline. This top-most one-line message is called the commit subject.

If there is more information you'd like to give (e.g., for a bug fix, what the problem was, how it was discovered, what has been done to prevent the bug returning, such as adding a unit test), add two newlines after the top line to create an empty line to offset it from the top line, then type your message. Wrap the text around 70 characters width, but make it as long as necessary (keep it clear and to the point). Multiple paragraphs (separated by an empty line) are fine.

Once you're happy with the commit message, save and close the editor. You have now created your first commit.

If you realised there was something wrong with the files being added, or you're in the wrong branch, remove all the text (you can leave the comments), save and exit. Git will not create a commit when the commit message is empty, and there will be a line in the terminal like "Aborting commit due to empty commit message." `#!console git status` should show the status as after the commit.

If you're not happy with the commit message itself, or you realise after the fact there was one file you've forgotten, you can amend the commit. Add the file if necessary with `git add <forgotten-file>`, then run
```console
git commit --amend
```

The editor will open up again, with the commit message from earlier. Alter the commit message as necessary, save and close, and your commit has been updated. For cases where you only forgot a file, you can even do `git commit --amend --no-edit`, which will not open the editor: the file or changes will be added, but the commit message remains the same.

You can also add small, forgotten, updates with amend: edit a file as necessary, then run `#!console git add <edited-file>`, then `#!console git commit --amend`. But only do that if the edits (or forgotten file) really are part of this commit, and not something new. Finaly, you can simply run `#!console git commit --amend` without adding anything, if you want to change the commit message.

(I've added forgotten files or small updates to files quite often. I now have an alias called `#!console git amend` for `#!console git commit --amend --no-edit`: `#!console git config --global alias.amend "commit --amend --no-edit"` if you like that idea.)

But don't use `--amend` to add more and more files or all changes to files: that is what multiple commits are for. A single commit should be a logical, small, unit of work.

To verify everything is as it should be, run:
```console
git status
```
and see that there are (presumably) no untracked files, nor any staged files. If you didn't change any of the tracked files either, git sees a clean repository.

A fun aspect of this amending is visible, when you add (but not yet commit) a file (or add a changed file), then edit the file. If you then run `#!console git status`, you'll see the file appear twice: once under "Changed to be committed:", and once under "Changes not staged for commit:". The message headers tell you what is happening: part of what you already added is ready to be committed. The part that you just edited, but didn't yet add, it not staged for commit, and will thus be left out if you now run `#!console git commit`.

So commits are not per file: they are per *changes*, and can (usually do) span across several files (for example, if you decide to apply some stylistic change, the change will be happening across lots of files in your project, but it is still one commit). That leads into the following topic, about commits and branches.

## What is a commit and branch

Git works by keeping track of the differences between changes. Together, these can be thought of a series of pipe pieces stuck together. Each set of changes you make are "committed" to Git, and then form a pipe piece. Each commit comes with a unique identifier, that identifies such a pipe piece.

A commit is thus a change in your code or documentation that is stored by Git. Usually with a message, a unique identifier (a hash), a date, and the name of the person who made the commit. That change can be a simple correction for a typo, or numerous changes in various files. But try to keep your commits small: you can always combine multiple commits into a larger commit ("squashing" commits) later on.

A series of commits that form a single "pipe" can be called a branch. So initially, you start out on the main branch, and keep adding commits to it.

Sometimes, you want  try out something new. You "branch off", and create a new branch. It may have a name such as "feature/multithreading" when you change your code to run multi-threaded, while maintaining the single-threaded code on the main branch; or "bugfix/infinite-probability" when you're fixing a bug that leads to infinite probabilities in your code (lenghty names are not common, but not bad either: tab-completion helps a lot here when e.g. switching between branchs, and prefer clarity over obscurity).

So the picture would then be a series of pipe pieces, at some points diverging (and possibly diverging again, and again), branching off from a trunk (hence the possible name "trunk" for a "main" branch).

But the comparison to a tree of pipe pieces fails at some point, because some of these branches may be "merged" back into the main branch. Or a sub-sub-branch may be merged back into a sub-branch (before that is all merged back into a main branch). A bug fix would be merged back once it has been completed and verified to be correct. A feature branch would also be merged back once deemed stable and mature enough. That would lead to the picture of a tree of pipe pieces, with branches that at some point grow back into the tree trunk.

To top it off, it is possibly to take pipe pieces (or rather, the changes stored therein) and apply these to completely different sections of the tree. So suddenly, a pipe piece is copied and stuck in the middle or on top of a completely unrelated branch. That would possibly be more like genetic engineering than a tree of pipe pieces. But Git doesn't care about tree, pipes or DNA, and it simply allows for all these possibilities. Which option(s) you use, depends on the situation, but if you run a single project on your own, branches will be far and few.


## Viewing the commits

To see that the commit exists, use
```console
git log
```
which gives an overview of the commits.

The output contains quite a bit information. Let's look at the example below:
```
commit 809d5453c00d6e26130ec1d0bce9838e1a14f193 (HEAD -> main)
Author: Evert Rol <@>
Date:   Wed Jun 15 15:08:16 2022 +0200

    Initial commit
```

The hexadecimal hash is a unique identifier for this commit (in very large repositories, the same identifier may appear twice, a so-called hash collision (or hash clash, as I like to call it); this happened in the Linux kernel repository, but is extremely rare). The hash is calculated from the changes made within this commit.

Then there is some branch information: more about `HEAD` later, but it means we're at the top (front) of this branch, and that branch is `main`.

Then, there is the author name, with an e-mail address (yes, my e-mail is set to a single `@` in my git configuration). This makes it easy to find out who is responsible for which changes. There is even a `#!console git blame` command to help with that, although the naming is perhaps a bit negative: bug fixes and new features (most of the time) are also attributed to people, and this makes it easier to see who all contributed to a repository.

There is the date, which is obvious. It's timezone aware, so my local time at the time of the commit was eight minutes past five in the afternoon.

And finally, there's the commit message.

If I had written more below the subject message, perhaps even several paragraphs, those would all have been listed as well. If there are dozens, hundreds or even more commits with such messages, all of these will be shown (usually paged), making `#!console git log` somewhat unreadable. It is, for me, mostly useful to view the most recent commit message.

In repositories with a large amount of commits, it it more useful to shorten all information to one line. Again, I have an alias for that:
```console
git config --global alias.lol "log --pretty=format:%h%x09%ad%x09%s --date=short --color"
```

Now do `#!console git lol`:
```
809d545       2022-07-28      Initial commit
```
Of course, there is only one commit. The date is much shorter (no time information), there will only be the top-line message (which is why you want it to be about 50 -- 60 characters short), and a shortened version of the hash. Even the shortened hash is often enough to unique identify the commit in a single repository.

If you want to deciper the "pretty" format:

- `%h`: the abbreviated commit hash
- `%x09`: print the hex code character: 09 is the tab
- `%ad`: the author date
- `%x09`: another tab
- `%s`: the commit message subject

and `--date=short` of course sets the YYYY-MM-DD format of the date.

# Adding selective changes

At times, you may make multiple changes that you want to be distinct from each other, stored in different commits. For example, you're adding a new function to your code, and along the way, extend another function or do some refactoring in another file. And at the same time, you added a license file to your project as well.

There are a few ways to add select what files or parts of files are added to a commit.

First, you can just name all the individual files that you want to add. That will add all changes in those files, but it will leave other files outside the commit.

Second, you can use the `-u` or `--update` with `git add` to add all changes in all *tracked* files. Tracked files are files that Git already keeps, well, track of. If you run `git status`, you may also see a list of untracked files. So `git add .` will add *all* files, tracked and untracked, but `git add -u .` will add only already tracked files (the `.` indicates all files in the current directory, and recursively through all subdirectories as well).

Third, you can add a section of a file. This may be for cases where you performed multiple, independent, changes in a file. This is a tad more complicated. Use the `-p` or `--patch` option with `git add`; I almost exclusively use this together with the `-u` option, since adding completely new files are often their own commit. Thus, `git add -up <filepath(s)>`.

This will step through sections of the files, and Git asks the user for each section whether it should be staged (that is, added to the next commit). You have a number of answer possibilities (type `?` for a brief explanation). The most common ones to use are
- `y`: Yes, add this part
- `n`: No, skip this part (that is, this change should go into another commit later)
- `q`: Quit, stop further processing of patches. Previously added patches remain staged

Use control-C to cancel the complete process: this will undo staged patches.

When adding patches ("hunks") of changes to Git, you likely will end up with files being partly in the staging area ("Changed to be commit") and partly just modified ("Changes not staged for commit"). You can see this when you run `git status`.

As a fourth option, you can even edit subdivide the hunks that Git suggests. Use the split option, with `s` when running `git add -p`, to let Git attempt to find smaller blocks.

And when even that is not enough, you can tell Git which lines to include and exclude for a specific hunk (lines are about the minimum change you can add; this is in large part because it is easier to tell a change between and old and new line, than a change inside a line itself. It is certainly easier to view; see below for viewing differences). For this, use the `e`, edit, option. This will open the text editor you've configured, and show the patch, with some annotations. Notably, there will be '+' or '-' signs in front of changed lines, depending on whether a line was added or removed. The commented out notes near the bottom tell you want to do:

- if you don't want to remove a line (for this specific commit), replace the '-' at the start of the line with a space. The line will not yet be removed when you commit the staged patches, but it will still be removed in the modified file after the commit.
- if you don't want to add a line, delete the whole line (it should start with a '+'). Again, the line won't be added when you perform the actual commit, but will remain as a new line in the modified file afterwards.

Be aware that all relevant lines (whether context lines, added or removed lines) will all start indented by one column. That indent may then be a space, '+' or '-'. Don't remove that indent! In particular, code comment lines (or e.g. Markdown headings) may start with a '#', but will be indented, to distinguish them from actual comment lines by Git.

One you've done the modifications, save and close the files, and Git will stage the changes.

# Viewing what you have changed.

Before adding files for a commit, you can already view what you changed. Use
```
git diff <filepath(s)>
```
or (as usual) possibly
```
git diff .
```

This will show lines of old and new code. They are shown in blocks, starting with `@@` and then the relevant line numbers. Then, as before with manually editing what you want to stage for a commit, removed (or replaced) lines start with a '-' sign, while new or changed lines start with a '+'. Lines that have changed often show two versions directly above each other: the previous version that Git has stored, and the newly modified version. Of course, if a line (or more) has only been added, no old line is shown, just the new line(s) with a '+' prepended; and similar for lines that have been completely removed. Conveniently, the changes may also be shown in color: for me, red means old (removed), while yellow indicates changed or added, and grey lines are surrounding context lines (so no changes).

## Viewing what will be commited

Once you have added changed to be committed ("staged"), you can view what is actually about to be commit when you run `git commit`. Use
```
git diff --staged <filepath(s)>
```

So this is very similar as above, just with the `--staged` option added. And the output shown also uses the same format. If you notice something amiss, you can adjust as by adding more as above. Alternatively, you can of course amend the commit later on.


# Undoing a `git add`

If you add a file or change you didn't intend to, you can revert that change. `git status` will already tell you how:

> use "git restore --staged <file>..." to unstage

Using `git restore --staged` with the path(s) (or `.`, to revert all files), has the advantage that all previously untracked files become untracked again, and any modified files become modified again. Thus, changes you made to files are kept, but you can start with a clean slate for the next commit.

You can even use the `-p` or `--patch` option with `git restore` to selectively restore staged patches, as before when adding patches.

# Undoing changes to a modified file

If you make changes that you don't want, you can ask git to undo this completely. This is dangerous, because there'll be no way to go back to the modified file!

Use
```
git restore <filepath>
```
to undo any modifications.

If you ever do this by accident, check if the file is still open in your text editor. If it still has the changes, save the file. Otherwise, if the file updated to the restored file on disk, try undoing the last edit(s) to get your changes back, then save the file.


`git restore` is very useful if you accidentally delete or overwrite a file (removing a file is, to Git, also a change; and Git keeps track of changes). `git status` will show the file as deleted (if overwritten, it will just show it as changed), but `git restore` will bring the original file back. At least to the point that Git knows about, so any changes you had made before you deleted it are, unfortunately, lost. Which is a good reason to often perform small commits. You can then later combine ("squash") these small commits together in a larger, more comprehensive commit. Of course, amending a commit also works, if you don't care about the intermediate changes.

# Getting command line help

Git commands provide help, with a slight twist. `git <command> -h` will briefly show the most common options and sub-commands. For me, that is always a good reminder how to use a command. 

`git <command> --help`, however, will actually show you a manual page for that command, which is a lot more to read through. Use the former as a quick reminder of options and what does what; use the latter if you want a much more in-depth explanation of the command.
