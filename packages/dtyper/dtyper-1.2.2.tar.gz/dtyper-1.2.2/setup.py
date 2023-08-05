# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['dtyper']
install_requires = \
['typer']

setup_kwargs = {
    'name': 'dtyper',
    'version': '1.2.2',
    'description': '⌨️dtyper: Call typer commands or make dataclasses from them ⌨',
    'long_description': '# ⌨️dtyper: Call `typer` commands, or make a `dataclass` from them  ⌨️\n\n`typer` is a famously easy and useful system for writing Python CLIs but it has\ntwo issues.\n\nYou cannot quite call the `typer.command` functions it creates directly.\n\nAnd as you add more and more functionality into your CLI, there is no obvious\nway to break up the code sitting in one file.\n\n`dtyper` solves these two defects, calling `typer.command` functions\nwith the right defaults, and constructing a `dataclass` from a `typer.command`.\n\n-----------------------------------------------\n\n`dtyper` is a drop-in replacement for `typer`, so you can even write\n\n    import dtyper as typer\n\nif you like!\n\n It overrides one member from `typer`, and adds two new ones:\n\n* `dtyper.Typer`is a class identical to `typer.Typer`, except it fixes\n  `Typer.command` functions so you can call them directly (with the right\n  defaults).\n\n* `@dtyper.dataclass` is a decorator that takes an existing `typer` command\n  and makes a `dataclass` from it.\n\n* `@dtyper.function` is a decorator that takes a new `typer` command and returns\n  a callable function with the correct defaults.  It is unncessary if you use\n  `dtyper.Typer`.\n\n## Installation\n\n    pip install dtyper\n\n## Examples\n\n### Example: a simple `dtyper.dataclass`\n\nHere\'s a simple CLI in one Python file with two arguments `bucket`, `keys` and\none option `pid`:\n\n    @command(help=\'test\')\n    def get_keys(\n        bucket: str = Argument(\n            ..., help=\'The bucket to use\'\n        ),\n\n        keys: str = Argument(\n            \'keys\', help=\'The keys to download\'\n        ),\n\n        pid: Optional[int] = Option(\n            None, \'--pid\', \'-p\', help=\'process id, or None for this process\'\n        ),\n    ):\n        get_keys = GetKeys(**locals())\n        print(get_keys())\n\n    @dtyper.dataclass(get_keys)\n    class GetKeys:\n        site = \'https://www.some-websijt.nl\'\n\n        def __call__(self):\n            return self.url, self.keys, self.pid\n\n        def __post_init(self):\n            self.pid = self.pid or os.getpid()\n\n        def url(self):\n           return f\'{self.site}/{self.url}/{self.pid}\'\n\n\n### Example: putting the `dtyper.dataclass` into a separate file\n\nIn real world CLIs, there are frequently dozen of commands, each with dozens\nof options or arguments.\n\nTo avoid the "big bowl of mud" anti-pattern, you often want to split off the\nuser-dash facing definition of the API from its implementation, and in large\nprograms, you might well want to split the implementation itself into multiple\nfiles.\n\nThis example has three Python files.\n\n`interface.py` contains the CLI API for this command.\n\nThe `big_calc` module is lazy loaded in interface.py - only loaded when this\ncommand is actually called.\n\nLazy loading is extremely useful in large projects, because it means you don\'t\nload the entire universe that any command _might_ want just to execute one tiny\ncommand that has no dependencies, and it is necessary in this case to avoid\ncircular dependencies.\n\n    # In interface.py\n\n    @command(help=\'test\')\n    def big_calc(\n        bucket: str = Argument(\n            ..., help=\'The bucket to use\'\n        ),\n        # dozens of parameters here\n    ):\n        d = dict(locals())\n\n        from .big_calc import BigCalc\n\n        return BigCalc(**d)()\n\n\nHere\'s the actual dataclass, which knows about everything.\n\n\n    # In big_calc.py\n\n    from .interface import big_calc\n    from . import helper\n    from dtyper import dataclass\n\n    @dataclass(big_calc)\n    class BigCalc:\n        def __call__(self):\n           if helper.huge_thing(self) and self.etc():\n              self.stuff()\n              helper.more_stuff(self)\n\n           # Dozens of methods here\n\n\n\n    # In helper.py\n\n    def huge_thing(big_calc):\n        # Lots of code\n\n    def more_stuff(big_calc):\n',
    'author': 'Tom Ritchford',
    'author_email': 'tom@swirly.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/rec/dtyper',
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.7',
}


setup(**setup_kwargs)
