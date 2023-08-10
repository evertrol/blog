Title: Good and bad uses of notebooks
Date: 2023-04-20
Category: Python, Jupyter
Status: draft
Summary: When to use notebooks, and when not to use them

# Good and bad uses of notebooks

Notebooks, the digital computational ones, have become very popular in science and research. They have a number of good uses, but there are also cases where you shouldn't use a notebook. Below, I list some opinionated points where notebooks are useful and where they probably should not be used. Some points may be controversial, but read my explanations below the lists.

Good use cases

- Data exploration

- Trying out things, such as short code snippets

- Examples and showcases

- Teaching

- 

Cases where you probably should not use notebooks

- Reproducibility

- Long running processes

- Data exploration on compute nodes


## Good use cases of notebooks

### Data exploration

This is one of the cases of the original intent of notebooks: explore your data in an interactive way, going back and forth while creating figures of the data, changing some parameters for reading and subsetting your data. It's a great way to get a good idea of the data, and how to handle it. Once you have a good idea of what the data contains and how to handle it, you can turn parts of your notebook into a proper program to automatically process the current and more data.


One thing that is also possible, is to work with more people in the same notebook for this purpose. This requires some discipline, as to not edit a notebook while someone else is editing it at exactly the same time, but it can make in particular data exploration, an interactive back and forth between colleagues, in particular when the people are not in the same space. It avoids the hassle of screen sharing while editing a notebook, and then having someone else trying to suggest an edit over an online connection: the second party can just directly edit their suggestion into the notebook. (On the technical side, this requires a notebook server on a machine that both people can access. But this is generally straightforward.)

### Trying out things

The interactive nature makes it easy to try out a short piece of code, rewriting it and running it again, until you have the (perfect) piece of code, which you can then use in your larger program. One case in particular could be making a graph, fiddling with the various settings and other tweaks until you get the right result. I occasionally also use it to time different variations of some code, to see if a change (that may make the code slightly less understandable, for example by using fancy slicing and broadcasting in NumPy) actually speeds up things significantly enough to see that the change is warranted.

### Examples and showcases

With the possibility to easily insert (formatted) text and figures in between the code, notebooks can easily be used to create examples for, say, a package or library you have written. Or, with the data exploration in mind, create an example of how to explore certain data. Which can then straightforwardly passed onwards to colleagues or other interested people. Notably, various sites (for example, GitHub) automatically render notebooks with all the text, code and figures (but don't run it!), such examples and showcases become very easy to show on the web (or an internal network).

### Teaching

With the above mentioned examples, teaching things is also possible. But with a caveat: I would not use it for beginners to learn how to code, since the interactive nature and different style of running a piece of code, hides some of the nature of running an actual program. Once people know the basics of this, notebooks can be useful for teaching, since you can go back and forth, altering things to show how that affects the result. Learning about specific libraries and packages for, for example, data science, or learning about specific data, can be very practically taught in a notebook.


## Cases to avoid using notebooks

Some of the below cases may be controversial, but I've listed my reason(s) why to avoid a notebook in each case

### Reproducibility

Being able to reproduce a simulation, a data reduction or data analysis, is an important thing, in particular in science. But the interactive nature of notebooks hampers this somewhat: you may have fiddled too much with certain variables, running code after every alteration, that the final result is not the result from a single run through the code anymore. To avoid this, you should restart the notebook and run it from start to end (for Jupyter notebooks, restart the kernel and run all cells; this is a menu option), but this is both easy to forget, and it may result in your end result is not what you had before (which is a good thing: it showed you have overlooked something).

Furthermore, reproducibility requires having the proper libraries and compiler / interpreter, including the correct version. You should therefore list the versions of all libraries that you use, as well as the main compiler or interpreter. For example, for Python in a Jupyter notebook, this would be something like 
```
from sys import version
import numpy as np

sys.version, np.__version__
```

Then, you may also have created multiple iterations of your notebook: you publish one, but later realise that you want to do things differently (perhaps there is a library that you didn't use in the first version). Now you have two version, and while you could delete the first one, it may stick around on the internet, causing confusion if people use different versions. Thus, you would need to annotate the version of your notebook. You could even use version control, such as Git, to have this done for you, but this can become quite annoying, as every time you run the notebook, even without altering it, Git will find it has changed, because the notebook stores some extra metadata such as the date it has been run. There are tools to clean notebook files, but then you probably want to take care the output is still preserved. 

I never use the last two points by default, which makes my notebooks already bad for reproducibility. Of course, that doesn't mean everyone doesn't do this, but there are very few notebooks that I have seen that do this. Some notebooks have a separate listing of the packages or libraries used (such as a `requirements.txt` or `environment.yml` file), but then you need to bring an extra file along. You might then want to start thinking about turning the notebook into a reproducible package, where this is much more the default.

If you do want to use notebooks for reproducible science, there are some guides. The main article I found is [Ten Simple Rules for Reproducible Research in Jupyter Notebooks](https://arxiv.org/ftp/arxiv/papers/1810/1810.08055), with an accompanying website at https://github.com/jupyter-guide/jupyter-guide .

Personally, I would avoid notebooks for really creating reproducible code. Turn the code into a proper package or library (that is hopefully straightforward to install), then use notebooks for examples, showcases and explanation of the package, as a separate part of the package (probably as part of the documentation).


### Long running processes

With data exploration and once you have figured out a good way to process the data, it becomes easy to let your code run over a large set of data files (or similar, let it run a long simulation). But a practical problem is that now: do you close the notebook window (or browser tab)? If you have set things up correctly, the notebook process will still be running, including the data processing or simulation; in that sense, nothing is lost if you close the window or accidentally lose the connection (when not running the notebook locally). And the notebook file is likely also there. But if you have set up things to produce a figure *only* in the notebook, or print the results to the notebook (but neither to file), your output may lost, even if you reopen the notebook.

More generally, long running processes should probably coded such that they produce intermediate files from which they can be started again if the process itself happens to fail. This is beyond the scope of a notebook, and is a general recommendation, but a notebook will certainly not help with this.

### Data exploration on compute nodes

This one is quite specific, and doesn't have to be a bad thing per se. But I think it is indicative of going the wrong way about data exploration. Compute nodes are really for computations, including data reduction, but not for interactive work. In this case, exploring the data locally makes more sense. That, however, may not be feasible, for example when the data itself is large and can't be easily moved onto a local machine. It may be worthwhile to discuss this the relevant system administrator(s), to see if it's a good thing to do, or perhaps they have a separate server (or can set up one) from where you can access and explore the data as well. The latter server doesn't have to be like a compute note, since data exploration shouldn't really involve a lot of computational power.
