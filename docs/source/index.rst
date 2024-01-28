.. Hostname documentation master file, created by
   sphinx-quickstart on Sun Jan 28 13:59:46 2024.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

A Python validator for Internet hostnames
====================================

Not all valid DNS names are valid hostnames, although all valid hostnames are valid DNS names.

The |project| package package provides :func:`hostname.name.is_hostnbame`
boolean function, which performs syntactic validation of candidate hostname.
This validation is syntactic only.
It does not check whether the hostname exists in the DNS system or is reachable.


.. toctree::
   :maxdepth: 2
   :caption: Contents:



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
