Exceptions
===========

All exceptions listed here are subclasses of :class:`exception.HostnameException`

Overview and examples
----------------------

.. testcode::

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


Because we want to distinguish the case when something isn't a hostname
from when arguments are provided incorrectly,
we use
:class:`hostname.exception.NotAStringError`
instead of :py:class:`TypeError` when the
candidate hostname is not a string.

.. testcode::

    e = "No exception so far"
    try:
        hostname.Hostname(1)
    except  hostname.exception.NotAStringError:
        e = "Caught Hostname NotAStringError"
    except TypeError:
        e = "Caught TypeError"
    except Exception:
        e = "Some other expection"

    print(e)

.. testoutput::

    Caught Hostname NotAStringError

This allows us to use TypeError to check other arguments

.. testcode::

    e = "No exception so far"
    try:
        hostname.Hostname("foo", unknown_flag = "bar")
    except  hostname.exception.NotAStringError:
        e = "Caught Hostname NotAStringError"
    except TypeError:
        e = "Caught TypeError"
    except Exception:
        e = "Some other expection"

    print(e)

.. testoutput::

    Caught TypeError

If a candidate hostname triggers an error from
`the IDNA package <https://pypi.org/project/idna/>`_,
we wrap that in
:class:`hostname.exception.IDNAException`

.. warning::

    Only one exception will be raised even if the candidate is
    invalid for multiple reasons.
    Which of the errors gets reported in such cases is undefined behavior.


All :class:`HostnameException` classes
---------------------------------------

.. automodule:: hostname.exception
    :members:
