Overview
===========================================

Full usage details of :func:`hostname.is_hostname`
and :class:`hostname.Hostname` are provided in :doc:`usage`.
Here is just an overvew to present an idea of what this package provides.

Motivation
-----------

Incorrect and inconsistant validation of inputs can lead to security vulnerabilities. Thus there is a need for a way to ensure that a string is a valid hostname before using it as such.

The plethora of StackExchange and other answers to
"how to parse hostnames in python" were rarely complete or correct.
I was suprised that there was no standards-based solution already,
and took this as an opportunity to learn how to write a Python package.

Valid hostnames
----------------

The details of what defines a valid hostname and the Internet
standards that define them are in :doc:`standards`.
For now, it is important to know that valid hostnames are a proper subset of valid DNS names, but they have some additional requirements.

.. note::

    This package is very opinionated about underscores in hostnames.
    See the :ref:`flag-allow_underscore` flag to enable
    limited non-standard behavior
    and :doc:`underscore` for the rationale.

The |project| package provides
:func:`hostname.is_hostname`
boolean function, which performs syntactic validation of candidate hostname.
This validation only on the form of the candidate hostname.
It does *not* check whether the name exists in the DNS system.

Examples
---------

.. testcode::

   import hostname

   examples = [
    ("an.ok.example", True, "A simple example"),
    ("a.single.letter", True, "Some regexs get this wrong"),
    ("-initial.hyphen.example", False, "Bad hyphen placement"),
    ("123.456.78a", True, "all digit labels sometimes ok"),
    ("last.digits.123", False, "last label cannot be all digits"),
    ("an.absolute.example.", True, "Note the final '.'"),
   ]

   if all([ hostname.is_hostname(c)== v for c, v, _ in examples ]):
        print("All are as expected")
   else:
        print("Oops")


.. testoutput::

   All are as expected

The :class:`hostname.Hostname(candidate: str)` will return a new and initialized
:class:`hostname.Name` if and only if its argument is a valid hostname.

>>> hn = hostname.Hostname("foo.bar.example")
>>> type(hn)
<class 'hostname.Hostname'>
>>> isinstance(hn, str)
True
>>> hn.labels
[b'foo', b'bar', b'example']

If, however, the candidate hostname is not valid,
initialization will raise an exception.
The specific exception will contain
information about why validation failed.
The full list of expections is documented in :doc:`exceptions`.

There are also a number of :ref:`sec-flags` for changing the default behavior.
For example, the :ref:`flag-allow_empty` flag allows an empty hostname.

>>> hostname.is_hostname("")
False
>>> hostname.is_hostname("", allow_empty = True)
True
