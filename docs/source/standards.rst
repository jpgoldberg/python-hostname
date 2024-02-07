RFCs
======

Nomenclature
-------------

The definitions below will refer to this example::

    bar.foo.example



label
    Roughly speaking, a label is a portion of a hostname between the dots.
    In the example,
    we see three [#noroot]_ labels, ``bar``, ``foo``, and ``exmaple``.
    Note that a valid hostname need not contain any dots if it is a relative hostname.

rightmost label
    In our example ``example`` is the rightmost label. It may also be referred to as the **last** label. There are conditions that apply to only the rightmost label which is why this term is useful.

leftmost label
    In our example ``bar`` is the lefttmost label. It may also be referred to as the **first** label. We may optionally relax some conditions on the leftmost label, which is why this term is useful



The primary basis for what is and is not a valid hostname comes from [RFC-952] (with updates from [RFC-1123] and [RFC-5890]).

### Labelling labels


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

This allowed hostnames such as `3Com.net`.[#3]_

.. rubric:: Footnotes

.. [#noroot] I am not counting the invisible root label, "", in this discussion.

.. [#3] 3Com was a a leading network technology company at the time that these standards were developed.
