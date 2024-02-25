Exceptions
===========

All exceptions listed here are subclasses of :class:`exception.HostnameException`

.. testcode::

    import hostname

    e = "No exception so far"
    try:
        hostname.Hostname("a.bad-.example")
    except hostname.exception.HostnameException:
        e = "Caught some hostname expection"
    except Exception:
        e = "Some other exception"

    print(e)

.. testoutput::

    Caught some hostname expection



If a candidate hostname does not meet the requirements of a domain name,
we raise an
:class:`hostname.exception.DomainNameException`
which wraps :doc:`dns:exceptions` from the dns package.

.. testcode::

    import hostname

    e = "No exception so far"
    try:
        hostname.Hostname("a..example")
    except hostname.exception.DomainNameException:
        e = "Caught some DNS expection"
    except Exception:
        e = "Some other exception"

    print(e)

.. testoutput::

    Caught some DNS expection





If a candidate hostname triggers an error from
`the IDNA package <https://pypi.org/project/idna/>`_,
we wrap that in
:class:`hostname.exception.IDNAException`

.. automodule:: hostname.exception
    :members:
