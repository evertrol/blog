Title: Python class functionality
Date: 2022-10-17
Category: Python
Status: draft

```
def force(r, m1, m2, G=6.674e-11):
	F = G * m1 * m2 / r**2
	return F
```


```
class System:
	def __init__(self, mass1, mass2, radius, G=6.674e-11):
		self.mass1 = mass1
		self.mass2 = mass2
		self.radius = radius
		self.G = G

	def force(self):
		F = self.G * self.mass1 * self.mass2 / self.radius**2
		return F
```

```
	def set_force(self):
		self.F = self.G * self.mass * mass / r**2
```

Of course, now the same calculation is done twice: once in the `force` method, once in `set_force` method. It's more convenient (or natural, or standard), to calculate `self.F` in `set_force`, and simply return `self.F` in `force`. Thus, rewrite `force` to
```
	def force(self):
		self.set_force(self)
		return self.F
```

Inconveniently, there are now two ways to set the force `self.F`: once directly through `set_force`, once more indirectly through `force`. Since the force acting on the body is here a property of the body itself (which is clear from the `self` use in `self.F`), `force()` should really just return `self.F`:

```
    def force(self):
		return self.F
```

The slight disadvantage is that you can't see what happens under the hood: here, there is no calculation, while in the previous code sample, there was a calculation.


There is also the option that you calculate the force directly in `__init__()`:
```
	def __init__(self, mass1, mass2, radius, G=6.674e-11):
		self.mass1 = mass1
		self.mass2 = mass2
		self.radius = radius
		self.G = G
        self.F = self.set_force()
```

This is a choice, and a bit of a trade-off. I prefer setting the basic parameters of the class, with minimal calculates, and not use methods to calculate extra things. I like to make such calculations explicit. This helps keeping the class instantiation quick and simple: it does nothing extra.


An annoyance is the fact that `force()` has to be called to obtain the value. You could call `self.F` directly, but if you use the previous approach, you may first need to calculate something before returning the force. In that case, you can use Python's `@property` attribute. You use it as follows:
```
    @property
	def force(self):
		return self.F
```

The `@` indicates a decorator, which tells the function after it (the `property` function) to "decorate" the function below it, `force()`. In this case, the `property` function uses some Python magic, so that you can access the method directly as a instance variable: it turns the method into a so-called getter:
```
body = Body(mass1, mass2, radius)
body.set_force()
print(body.force)
```

Properties are not always necessary, and should be used with caution. You'll mostly want them when you need to do a little extra to return a value. Or, for so-called setters, a little extra when you set an instance variable. Some more information is available in the [Python documentation](https://docs.python.org/3/library/functions.html#property).

But what if you want to change the mass of the main body; or perhaps even change physics and use a different value for `G`? And do that for a range of masses?

Most logical, and clearest, is to use a loop:
```
mass2 = 100
radius = 10
masses = range(10, 100, 10)
for mass1 in masses:
    body = Body(mass1, mass2, radius)
	body.set_force()
	print(body.force)
```

There may be a tiny bit of extra overhead, since you have to instantiate the `Body` class every time. But this is very minimal.

But, in some cases, you may prefer setting the body's mass directly (`body.mass2 = new_mass`), and also having the force update automatically in that case. This is where properties come in again, this time as a setter for `mass1`:

```
class Body:
    ...
	@property
	def mass1(self):
	    return self.mass1

	@mass1.setter
	def mass1(self, mass):
	    self.mass1 = mass
		# Update self.F
		self.set_force()
```

Note that, despite the various uses of `mass1` and `mass`, there is no confusion: `mass1` refers to the property, `self.mass1` to the instance variable, and `mass` to the new value. When using `body.mass1` outside of the class definition, the property overrides (or replaces) the instance variable, and will go through the respective methods for getting or setting the variable. So, the above code would now be:


```
mass2 = 100
radius = 10
masses = range(20, 100, 10)
body = Body(10, mass2, radius)
for mass1 in masses:
	body.mass1 = mass1  # using the setter property; automagically updates self.F
	print(body.force)   # fetches self.F with the force() getter property. print(body.F) would also work
```

