# Validating hostnames

The Hostname package provides an `is_hostnbame(str: candidate)` function, which performs syntactic validation of candidate hostname

Much to my surprise, or perhaps simply failure to search properly,
there is no RFC compliant python tool that syntactically validates hostnames.
Note that not all valid domain names are valid hostnames.

To validated domain names, I recommend [dnspython],
and to validate Urls
I recommend [Pydantic](https://docs.pydantic.dev/latest/).
But neither offers direct validation of hostnames.

## "Host" v "hostname"

A host for many internet protocols can be given in the form of a domain name, an IPv4 address, or an IPv6 address. I will use the term "hostname" to require to the domain name form.
A hostname must be a valid domain name, but not all valid domain names are hostnames.

## Standard interpretation

The primary basis for what is and is not a valid hostname comes from [RFC-952] (with updates from [RFC-1123] and [RFC-5890]).

### Labelling labels

In the discussion here, I will use the term “label” to refer to a part of a hostname that appears between the dots.
For example the hostname "`bar.foo.example`" has three labels.[^4]:
"`bar`", "`foo`", and "`exmaple`".
There are requirements that are specific to the last (rightmost) label,
and there may be things that are allowed only in the first (leftmost) label.
In the example, "`bar`" is the first (leftmost) label, and "`example`" is the last (rightmost) label.

[^4]: I am not counting the invisible root label, "", in this discussion.

### RFC952: Hosts, etc

[RFC-952] codifies hostname conventions which emerged prior to the Domain Name System.
It tells us that a valid hostname ("hname" in the grammar given) conforms to

```txt
<hname> ::= <name>*["."<name>]
<name>  ::= <let>[*[<let-or-digit-or-hyphen>]<let-or-digit>]
```

Roughly that is a string of labels dot separated labels ("name" in that grammar.
The first character of a label
(and there must be a first character)
must be a letter.
The requirement that it be a letter was later dropped.
The last character of a label must be a letter or a digit.
Internal characters must be a letter, or a digit, or a hyphen.

### Length restrictions

RFCs [1034][RFC-1034] and [1123][RFC-1123] introduce additional requirements on hostnames.

[RFC-1123] makes it clear that a hostname must also be a valid domain name.
So all requirements on domain names must apply to hostnames.
Of course not all valid domain names are valid hostnames.
After all, `*&.!!+1.()` is a valid domain name, but is certainly not a valid hostname.

Section 3.1 of [RFC-1034] specifies a length limits of 63 bytes on labels,
and 255 bytes for the entire domain name. That 255 includes a root "." and root domain.
And so domain names without the trailing dot can have a maximum length of 253 bytes.

The Hostname package uses the excellent [dnspython] to validate that its input is a valid domain name.

### Digits first

Section 2.1 of [RFC-1123] amends the restriction on the first character, allowing it to be a digit as well as a letter.

> The syntax of a legal Internet host name was specified in [RFC-952].
> One aspect of host name syntax is hereby changed: the
> restriction on the first character is relaxed to allow either a
> letter or a digit.  Host software MUST support this more liberal syntax.

This allowed hostnames such as `3Com.net`.[^3]

[^3]: 3Com was a a leading network technology company at the time that these standards were developed.

### IDNA

To do

[RFC-5890] and friends radically change what counts as an allowable letter.

### Underscore

To Do


----

[![Checked with mypy](https://www.mypy-lang.org/static/mypy_badge.svg)](https://mypy-lang.org/)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

[RFC-952]: https://datatracker.ietf.org/doc/html/rfc952 "Host Table Specification"
[RFC-1123]:  https://datatracker.ietf.org/doc/html/rfc1123 "Requirements for Internet Hosts"
[RFC-5890]: https://datatracker.ietf.org/doc/html/rfc5890 "IDNA Definitions"
[dnspython]: https://www.dnspython.org "DNS toolkit for Python"
[RFC-1034]: https://datatracker.ietf.org/doc/html/rfc1034 "Domain Name Concepts"
