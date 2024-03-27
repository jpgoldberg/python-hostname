# Validating hostnames

A python package for syntactically validating and parsing hostnames.

[![Checked with mypy](http://www.mypy-lang.org/static/mypy_badge.svg)](http://mypy-lang.org/)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/charliermarsh/ruff/main/assets/badge/v0.json)](https://github.com/charliermarsh/ruff)
[![Hatch project](https://img.shields.io/badge/%F0%9F%A5%9A-Hatch-4051b5.svg)](https://github.com/pypa/hatch)

The package provides a function, `is_hostname()`,
which returns True if and only if its first argument is a valid hostname.

```python
from hostname import is_hostname

assert is_hostname('a.good.example')
assert not is_hostname('a.-bad.example')
```

`is_hostname()` can also be used as a [TypeGuard].

This package also provides a class, `Hostname`.

```python
from hostname import Hostname, exception

h = Hostname('a.good.example')
assert isinstance(h, Hostname)

try:
    b = Hostname('a.-bad.example')
except exception.BadHyphenError:
    assert True
else:
    assert False
```

See the package [documentation](https://jpgoldberg.github.io/python-hostname/)
for complete documentation,
including

- details of various flags to change acceptance criteria
- Lots of examples
- Notes on various subtleties
- class properties
- And best of all, rants about non-standard parsing!

-----------------

Much to my surprise, or perhaps simply failure to search properly,
there there no RFC compliant python tool that syntactically validates hostnames.
Note that not all valid domain names are valid hostnames.
So I wrote this.

To validated domain names, I recommend [dnspython],
and to validate Urls
I recommend [Pydantic](https://docs.pydantic.dev/latest/).
But neither offers direct validation of hostnames.

The Hostname package uses the excellent [dnspython] to validate that its input is a valid domain name
along with [idna] to handle internationalized hostnames.

[dnspython]: https://www.dnspython.org "DNS toolkit for Python"
[idna]: https://pypi.org/project/idna/ "PyPi: International Domain Names in Applications"
[TypeGuard]: https://docs.python.org/3/library/typing.html#typing.TypeGuard "typing.TypeGuard"
