Pluggen
=======

A simple plugin system for python modules, allowing you to register plugins
using class decorators. This project used to be called pyplug, but someone else
obviously beat me to the name.

This project came about as a part of my
[toy mDNS library](https://git.shangtai.net/staffan/zc) that needed a handy
way of registering DNS record types.

Usage
-----

Create a plugin collection by extending pluggen.Plugin:

```
from pluggen import Plugin

class TestCollection(Plugin):
	paths = [ 'path.to.my.plugins' ]
```

Then in path.to.my.plugins, create modules for your plugins and decorate them
with `@TestCollection.register` or the more verbose
`@TestCollection.register(name="alt_name", ...)`.

Additional parameters can be set in the register method to store metadata about
this particular plugin. The special parameter `name` can be used to give the
plugin a particular name, if none is provided the class name will be used.

The `name` should be unique, duplicate names will be ignored.

By default the `instance(name, config)` method can then be used to instantiate
a plugin based on its name, but you are of course free to override it and/or
add any custom lookup method you wish to use.

See pydoc pluggen.Plugin for more information (or read the source, it's small)
