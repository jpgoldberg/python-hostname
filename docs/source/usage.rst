Using |project|
===============

The function
-------------

.. autofunction:: hostname.name.is_hostname

The function, :func:`hostname.name.is_hostname` returns |True| if and only
if its argument is a syntactically valid hostname.
It's behavior can be adjusted slightly with some flags which can be set as keyword arguements.

Additionally it acts as a :py:class:`typing.TypeGuard`,
allowing type checkers to know that any object which
.. note::

    Uh, oh.  It isn't guarding the right type.

The class
---------

The :class:`hostname.name.Name` is a thing to be documented.

.. autoclass:: hostname.name.Name
    :members:

Flags
-----

The possible keyword arguments are the booleans, ``allow_idna``, ``allow_underscore``, and ``allow_empty``.

``allow_idna`` Allow non-ASCII hostnames. Default |True|
    When |True|, a hostname candidate hostname like
    ``"szárba.szökik.hu"`` will be accepted.
    When |False| such a candidate will raise an
    :exc:`hostname.exceptions.NotASCIIError` error.

``allow_empty`` Allow the empty string as a valid hostname. Default |False|
    When |True|, a hostname candidate hostname like
    ``""`` will be accepted.
    When |False| such a candidate will raise an
    :exc:`hostname.exceptions.NoLabelError` error.

``allow_underscore`` Allow underscore in leftmost label. Default |False|
    When |True|, a hostname candidate hostname like
    ``"under_score.in.host"`` will be accepted.
    When |False| such a candidate will raise an
    :exc:`hostname.exceptions.UnderscoreError` error.

    In all cases, a candidate with an underscore anywhere other than
    in the first (leftmost) label,
    such as ``"underscore.in.net_work"`` will raise an  :exc:`hostname.exceptions.UnderscoreError`.
    See :doc:`underscore` for details.
