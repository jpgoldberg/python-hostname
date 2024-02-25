.. Hostname documentation master file, created by
   sphinx-quickstart on Sun Jan 28 13:59:46 2024.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

A Python validator for Internet hostnames
===========================================

Not all valid DNS names are valid hostnames, although all valid hostnames are valid DNS names.

Along with a :class:`hostname.Hostname` class,
this |project| package provides
:func:`hostname.is_hostname`
boolean function, which performs syntactic validation of candidate hostname.


This validation only on the form of the candidate hostname.
It does *not* check whether the name exists in the DNS system.

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   overview
   usage
   exceptions
   standards
   underscore



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
