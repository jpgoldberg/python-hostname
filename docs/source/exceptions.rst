Exceptions
===========

All exceptions listed here are subclasses of :class:`exception.HostnameException`

If a candidate hostname does not meet the requirements of a domain name,
we raise an
:class:`hostname.exception.DomainNameException`
which wraps :doc:`dns:exceptions` from the dns package.

If a candidate hostname triggers an error from `the IDNA package <https://pypi.org/project/idna/>`, we wrap that in
:class:`hostname.exception.IDNAException`

.. automodule:: hostname.exception
    :members:
