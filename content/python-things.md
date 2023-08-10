Title: Practical Python things
Date: 2023-01-30
Category: python
Tags: python
Status: published
Summary: A set of practical Python tips and tricks


## The print function's keyword arguments

The `print()` function takes any number of arguments (separated by
comma), then will turn each argument into a readable string, and output
these with a space in between them. It will also automatically add a
newline at the end of its output.

But `print()` can also take specific keyword arguments:

`end`
:   The keyword argument `end` can be used to set how `print()` will end
    its output; . The default is `'\n'`, which is a newline, but setting
    it to an empty string `''` or a single space `' '` may be useful at
    times if you want to continue output on the same line.

    ```
    print("Hello, ", end="")
    print("world")
    ```

`sep`

:   The keyword argument `sep` is similar, but providese the separator
    between arguments; the default is a space, `' '`. If you have a
    list of strings (or things that can be turned into a string, which
    in Python is basically everything), you can use the following:

        strings = ["hello", "world", "you're", "number", 1]
        print(*strings, sep=", ")


    which prints the strings (and number) in order, separated by a comma
    and a space. Or use `sep='\n'` to have each item on a separate line.


`file`
:   The keyword argument `file` can be set to a file-like object (*not*
    a file name). So you could do:

    ```
    with open("hello-world.txt", "w") as fp:
        print("Hello, world", file=fp)
    ```

    Of course, `fp` should be writeable. You can also use
    `file=sys.stderr` to write to standard error. The default is `None`,
    which will result `print()` writing to `sys.stdout`, the normal
    standard output.

There is a fourth keyword, `flush` (default `False`) which flushes the
current output. Usually, you'll want to leave this to false: the
output will be buffered, which is more efficient. But it may mean that
you won't immediately see every line printed, in which case you could
use `flush=True`. It can be useful for debugging, but in general,
leave it as is (if you tend to use this keyword for printing status
messages, consider using logging instead).


## f-string debugging

A quick and simple way to debug your program is by printing out the
values of your variables at different points in your program. This,
however, requires you to annotate the `print()` function in a way that
it also prints the variable name and position, so you know where the
values printed come from. With f-strings, you can use a shortcut for
including the variable name:

```
print(f"{myvar=}")
```

Format the variable inside the f-string, and put a single `=` sign
after the variable. That's it. The output will be something like:

```
myvar=1.23
```

### Logging debugging

To also include things like the line number and possibly the file
name, think about using the logging module instead.  My preferred
message format does tend to be lengthy, but notice how there is a
function name and a line number in there:

```
import logging
logging.basicConfig(
    format="%(asctime)s [%(levelname)-5s] - %(funcName)s():%(lineno)d: %(message)s",
    datefmt="%y-%m-%d %H:%M:%S",
	level=logging.DEBUG   # Change to INFO or WARN for less logging
)
...
logging.debug("myvar = %s", myvar)
```

which results in something like:
```text
23-01-30 14:30:39 [DEBUG] - main():11: myvar = 1.23
```

Important note: do *not* preformat the logging message. Not with
f-strings, not with `.format()` or even with old-style `%`
formatting. Prepare a string with `%s` placeholders for variables
(`%f` or `%d` also works for floating point or integer numbers, but
`%s` always works), then supply the relevant variables as separate
arguments after the format string. This prevents the string formatting
from always being done, and will only be done when necessary (in this
case, when the logging level is set to DEBUG, and not when it is INFO
or WARN to silence all debugging messages). It saves a bit of time,
and is overall good practice.



## Chain comparisons

Instead of

```
if myvar >= 0 and myvar <= 10:
    ...
```

use

```
if 0 <= myvar <= 10:
    ...
```

instead. And yes, the following also works:

```
if -10 <= mynegvar <= 0 <= myvar <= 10:
    ...
```

but be careful about going overboard: readability
("understandability") of code is important. I might split the above in
to two chained comparisons, combined with `and`:

```
if -10 <= mynegvar <= 0 and 0 <= myvar <= 10:
    ...
```

But in the example below, it makes sense to have a single chained comparison with two variables:

```
if -10 <= lowvar <= highvar <= 10:
    ....
```

(Also, the `if` is not necessary: comparisons can stand on their own, or use it in a `while` clause, for example).


### Comparisons with `range`

In the particular example of `if 0 <= myvar <= 10:`, if `myvar` is an
integer and the two boundaries are integers, you can also use

```
if myvar in range(0, 11):
    ...
```

depending on which one you find more readable. But `5.5 in range(0,
11)` will be false, since `5.5` is a float.

Also, `in range(...)` is evaluated smartly: `1234 in range(0,
100_000_000)` doesn't create 100 million numbers: it will just look at
the start and stop values of the range (and the step if given: `1234
in range(0, 100_000_000, 10)` is false).


## Use `_` to as separator for large numbers

You can make reading large numbers clearer by putting (an) underscore(s)
in the number, to separate digits: compare `100000000` versus
`100_000_000`. It also works for floating point numbers:
`1_000.123_45` (but the accuracy may of course be less than than the
actual written number for floats). The `_` does not have to be per
three digits either: `1_0_0_0_0_0_0_0_0` works, but really shouldn't
be used.



## Flattening a nested list

```
nestedlist = [[1, 2, 3], [4, 5], [6, 7, 8, 9]]
```

```
unflattened = []
for sublist in nestedlist:
    for item in sublist:
	    unflattened.append(item)
```

```
unflattened = []
for sublist in nestedlist:
    unflattened.extend(sublist)
```

### Nested list comprehension

```
unflattened = [item for sublist in nestedlist for item in sublist]
```

```
unflattened = [item for sublist in nestedlist for item in sublist if item % 2 == 1]
```

```
unflattened = [item * item for sublist in nestedlist for item in sublist if item % 2 == 1]
```

You can even put a ternary if-expression in the item part, but that decreases readability rapidly. Judge for yourself:

```
unflattened = [item * item if item <= 5 else item  for sublist in nestedlist for item in sublist if item % 2 == 1]
```

which reads at least a bit better when spread across multiple lines:

```
unflattened = [item * item if item <= 5 else item
               for sublist in nestedlist
			   for item in sublist
			   if item % 2 == 1]
```

but you probably should avoid this level of list comprehension in general. (It might still be readable for a non-nested list comprehension: `[item * item if item <= 5 else item for item in mylist if item % 2 == 1]`. And it may help to put parentheses around the ternary if-expression).


Note the different between the ternary if-expression, which applies to every item, and the if condition at the end, which filters the resulting list.



### Itertools

```
from itertools import chain

unflattened = list(chain(*nestedlist))
```

```
from itertools import chain

unflattened = list(chain.from_iterable(nestedlist))
```


### Recursively flattening a nested list

```
multinestedlist = [[[1, 2], 3], [4, 5], [6, 7, [[8], 9]]]
```




# Tuples versus lists

Python has two built-in types for sequential storage of heterogenous data: tuples and lists. (There is also [an `array` module](https://docs.python.org/3/library/array.html#module-array) in the standard library, and of course NumPy, but both of these two deal with homogenous data: every element in these arrays has to be of the same type.)

## Mutability

The directly noticeable difference between the two is that tuples are immutable and lists are mutable: you can't alter a tuple once created. Quite often, they are used this way: data that shouldn't be altered is stored in a tuple, while lists are used when data may be appended, inserted, or removed. Indexing, slicing and splicing will work for tuples and lists equally well.

When I say altered, I mean of course "in-place": `data.append(5)` is not the same as `data = data + [5]`; the latter works equally well for tuples and lists, but you do create a new list or tuple (`data = data + (5,)` is the tuple variant); but the old list or tuple is not accessible anymore, since you've reassigned the variable name.

A practical thing to remember: operations that act in-place generally don't return a value (or rather, return `None`). This is used as an indication that the value itself has changed. While this is not always the case, it is convenient to keep in mind, and is also useful to use in your own functions. This also works, for example, for dicts: `my_dict.update({'item': 5.5})` will change `my_dict` directly. Keep in mind that this mainly applies to Python's standard library; Pandas, for example, always returns the changed `DataFrame` or `Series`, and only the specific `replace` argument (set to `True` or `False`) determines whether the original `DataFrame` or `Series` was changed as well, or not. As always: read the documentation (for the library you are using)!


## Usage

I prefer another distinction: I like to think of lists more of a homogenous sequence of items (even if it isn't; (NumPy) arrays tend to be homogenrous), and tuples as a bag of varied items. Varied items here means with different semantic meaning, even if the actual values could be of the same type. For example, storing the mean, median and standard deviation in a tuple makes more sense to me, even if they're all statistical entities, and all (likely) floating point numbers; a simple list of three values doesn't make it clear which one is the mean, median or standard deviation.

Worded differently, I like to think of tuples as a C struct, which has a separate field for each item. This is most clear by using named tuples (`collections.namedtuple`), which for the above example would look something like `stats(mean=5, median=4.5, stddev=1.2)`. (Be aware that [the `struct` module](https://docs.python.org/3/library/struct.html#module-struct) in Python's stdlib is not very relevant in this context, so don't compare to that.)

I don't care too much that this isn't changeable in-place: these values should be calculated once, and then likely don't, or rarely change. It's unlikely (for this example certainly) that you'd be appending more and more values to the tuple.

With the above example and mention of C-structs, dataclasses would perhaps be even more appropriate. And these can be altered in-place. Plus you can inherit from them. If tuples are like C-structs, then dataclasses are perhaps more like C++ classes.

So I like to use (named) tuples when returning multiple items from a function, or storing multiple items together to pass around. If more is required than just passing several combined values around, then a dataclass or something else may be appropriate. I don't use tuples for immutable lists; for that, I simply use a list, and avoid altering it (with the flexibility of Python, good coding behaviour is more the norm than defensive typing).

And why not use a dict? Because of a similar semantic difference: to me, a dict contains a set of similar values, but accessible by a key instead of an index. This doesn't work in practice when using keyword arguments to a function: these may contain wildly different types of values, but you can only use the `**kwargs` expansion trick with a dict, not with a named tuple (possibly because the named tuple came later). So with `s = stats(mean=5, median=4.5, stddev=1.2)` being a named tuple, I can't do `f(**s)`, but I could with a dict. Well, unless I use `f(**s._asdict())`, since there is a namedtuple-to-dict conversion (it has an underscore to prevent colliding with field (attribute) names); it's doubtful though if that is very readable. Using a dict for the `**kwargs` expansion does have the additional advantage that one can use `mean = kwargs.pop('mean')` in the function itself (which modifies `kwargs` in-place), then return or pass on the remaining `kwargs` to another function (for example, Matplotlib does this, as its functions often take a multitude of keyword arguments to set e.g., the styling).

## Advice

My suggestion is to use a (named) tuple where this makes sense (i.e., if you have several distinct values that you want to combine, try and see if turning them into a named tuple makes sense), and otherwise probably a list or a dict. If you need a bit more functionality, have a look at [dataclasses](https://docs.python.org/3/library/dataclasses.html). I don't recommend using a tuple as an immutable list: it may prevent a few errors, but in Python, it can be easy to circumvent such "protections".

Note: for ease of creationg, using [`typing.NamedTuple`](https://docs.python.org/3/library/typing.html#typing.NamedTuple) may be convenient.

Keep in mind that tuples (and dataclasses) are for single combined variables. If you have a list of tuples or dataclasses, and these become large, you're probably dealing with some sort of table, and it may be worth your while to look into NumPy recarrays or Pandas.


## Relevant links

- https://stackoverflow.com/questions/51671699/data-classes-vs-typing-namedtuple-primary-use-cases
