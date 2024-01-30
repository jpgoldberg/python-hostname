Using |project|
===============

Common signature
----------------

The two classes and one function described here have a common signature:

  :samp:`{funcOrClass}(candidate: Any, **kwargs: bool) -> {rtype}`

In normal usage, ``candidate`` must be a :py:class:`str`,
but we want :func:`hostname.name.is_hostname` to be defined for all inputs,
and we want the others to :exc:`TypeError` only when there is a type problem with the other arguments, while raising some subclass of :class:`hostname.exceptions.HostnameException` on a malformed candidate.

Details on the keyword arguments are described in :ref:`sec-flags` below.



The function
-------------

.. autofunction:: hostname.name.is_hostname

The function, :func:`hostname.name.is_hostname` returns |True| if and only
if its argument is a syntactically valid hostname.
It's behavior can be adjusted slightly with some flags which can be set as keyword arguements.

Additionally it acts as a :py:class:`typing.TypeGuard`,
allowing type checkers to know that any object which
passes the test is a :class:`hostname.name.Hostname`.


Classes
-------

Name
^^^^^

The :class:`hostname.name.Name` is the substantive class.

.. autoclass:: hostname.name.Name
    :members:

If ``candidate`` is not a valid hostname, initializing the class will one
of the :exc:`hostname.exceptions.HostnameException` :doc:`exceptions`.

Hostname
^^^^^^^^

The :class:`hostname.name.Hostname` should be thought of as a subtype of :py:class:`str`.

.. autoclass:: hostname.name.Hostname

If ``candidate`` is not a valid hostname, initializing the class will one
of the :exc:`hostname.exceptions.HostnameException` :doc:`exceptions`.
``**kwargs`` are described in :ref:`sec-flags`.


.. _sec-flags:

Flags
-----

The possible keyword arguments are the booleans, ``allow_idna``, ``allow_underscore``, and ``allow_empty``.

``allow_idna`` Allow non-ASCII hostnames.
    When |True|, a hostname candidate hostname like
    ``"szárba.szökik.hu"`` will be accepted.
    When |False| such a candidate will raise an
    :exc:`hostname.exceptions.NotASCIIError` error.

    Default |True|

``allow_empty`` Allow the empty string as a valid hostname.
    When |True|, a hostname candidate hostname like
    ``""`` will be accepted.
    When |False| such a candidate will raise an
    :exc:`hostname.exceptions.NoLabelError` error.

    Default |False|

``allow_underscore`` Allow underscore in leftmost label.
    When |True|, a hostname candidate hostname like
    ``"under_score.in.host"`` will be accepted.
    When |False| such a candidate will raise an
    :exc:`hostname.exceptions.UnderscoreError` error.

    In all cases, a candidate with an underscore anywhere other than
    in the first (leftmost) label,
    such as ``"underscore.in.net_work"`` will raise an  :exc:`hostname.exceptions.UnderscoreError`.
    See :doc:`underscore` for details.

    Default |False|
