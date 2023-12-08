# `is_hostname()` for python

Much to my surprise, or perhaps simply failure to search properly,
there is no RFC compliant python tool for that syntactically validates hostnames.
Note that not all valid domain names are valid hostnames.

To validated domain names, I recommend [dnspython](https://www.dnspython.org), and to validate Urls
I recommend [Pydantic](https://docs.pydantic.dev/latest/).
But neither offers direct validation of hostnames.

## "Host" v "hostname"

A host for many internet protocols can be given in the form of a domain name, an IPv4 address, or an IPv6 address. I will use the term "hostname" to require to the domain name form.
A hostname must be a valid domain name, but not all valid domain names are hostnames.

[![Checked with mypy](https://www.mypy-lang.org/static/mypy_badge.svg)](https://mypy-lang.org/)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
