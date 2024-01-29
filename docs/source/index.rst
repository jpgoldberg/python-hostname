.. Hostname documentation master file, created by
   sphinx-quickstart on Sun Jan 28 13:59:46 2024.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

A Python validator for Internet hostnames
===========================================

Not all valid DNS names are valid hostnames, although all valid hostnames are valid DNS names.

The |project| package package provides
:func:`hostname.name.is_hostname`
boolean function, which performs syntactic validation of candidate hostname.
This validation only on the form of the candidate hostname.
It does *not* check whether the name exists in the DNS system.

.. testcode:: python

   import hostname.name

   candidates = [
      "an.ok.example",  # Good
      "a.single.letter",  # Good
      "-initial.hyphen.example", # Bad hyphen placement
      "123.456.78a", # This is Good
      "last.digits.123", # But last label cannot be all digits
   ]

   [ hostname.name.is_hostname(c) for c in candidates ]

.. testoutput::

   [True, True, False, True, False]

The :class:`hostname.name.Name(candidate: str)` will return a new and initialized
:class:`hostname.name.Name` if and only if its argument is a valid hostname.
Otherwise it will raise an exception, which will contain some information about why validation failed.

For example

.. code-block:: python

   import hostname.name
   import hostname.exception as exc

   bad_name = hostname.name.Name("last.digits.123")

should raise :class:`hostname.exception.DigitsOnlyError`.

The full list of expections is documented in :doc:`exceptions`.





.. toctree::
   :maxdepth: 2
   :caption: Contents:

   usage
   exceptions
   standards
   underscore



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
