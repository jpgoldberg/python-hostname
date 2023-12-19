# `is_hostname()` for python

Much to my surprise, or perhaps simply failure to search properly,
there is no RFC compliant python tool for that syntactically validates hostnames.
Note that not all valid domain names are valid hostnames.

To validated domain names, I recommend [dnspython],
and to validate Urls
I recommend [Pydantic](https://docs.pydantic.dev/latest/).
But neither offers direct validation of hostnames.

## "Host" v "hostname"

A host for many internet protocols can be given in the form of a domain name, an IPv4 address, or an IPv6 address. I will use the term "hostname" to require to the domain name form.
A hostname must be a valid domain name, but not all valid domain names are hostnames.

## Standard interpretation

The primary basis for what is and is not a valid hostname comes from [RFC952] (with updates from [RFC1123] and [RFC5890]).

### Labelling labels

In the discussion here, I will use the term “label” to refer to a part of a hostname that appears between the dots.
For example the hostname "`bar.foo.example`" has three labels.[^4]:
"`bar`", "`foo`", and "`exmaple`".
There are requirements that are specific to the last (rightmost) label,
and there may be things that are allowed only in the first (leftmost) label.
In the example, "`bar`" is the first (leftmost) label, and "`example`" is the last (rightmost) label.

[^4]: I am not counting the invisible root label, "", in this discussion.

### RFC952: Hosts, etc

[RFC952] codifies hostname conventions which emerged prior to the Domain Name System.
It tells us that a valid hostname ("hname" in the grammar given) conforms to

```txt
<hname> ::= <name>*["."<name>]
<name>  ::= <let>[*[<let-or-digit-or-hyphen>]<let-or-digit>]
```

Roughly that is a string of labels dot separated labels ("name" in that grammar.
The first character of a label
(and there must be a first character)
must be a letter[^3].
The last character of a label must be a letter or a digit.
Internal characters must be a letter, or a digit, or a hyphen.

### [RFC1123] Domain name requirements

[RFC1123] says that a valid hostname must also be a valid domain name.
But it is also clear that not every valid domain name is a valid hostname.
Hostnames must meet both the requirements of [RFC952] and of valid hostnames.
It does, however, amend [RFC952] to allow the first character of a label to be a digit.
If I recall correctly, this was informally called "the 3Com amendment" at the time.

The additional requirements on hostnames that come from [RFC1123] impose length restrictions on labels (63 bytes) and on the entire name (254 bytes).

The Hostname package uses the excellent [dnspython] to validate that its input is a valid domain name.

[^3]: [RFC1123] amends the restriction on the first character, allowing it to be a digit as well as a letter. [RFC5890] and friends radically change what counts as an allowable letter.

[![Checked with mypy](https://www.mypy-lang.org/static/mypy_badge.svg)](https://mypy-lang.org/)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

[RFC952]: https://datatracker.ietf.org/doc/html/rfc952 "Host Table Specification"
[RFC1123]:  https://datatracker.ietf.org/doc/html/rfc1123 "Requirements for Internet Hosts"
[RFC5890]: https://datatracker.ietf.org/doc/html/rfc5890 "IDNA Definitions"
[dnspython]: https://www.dnspython.org "DNS toolkit for Python"
