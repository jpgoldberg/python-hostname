Using |project|
===============

.. autoclass:: hostname.name.Name
    :members:

.. autofunction:: hostname.name.is_hostname

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
    ``""under_score.in.host","`` will be accepted.
    When |False| such a candidate will raise an
    :exc:`hostname.exceptions.UnderscoreError` error.

    In all cases, a candidate with an underscore anywhere other than
    in the first (leftmost) label,
    such as ``"underscore.in.net_work"`` will raise an  :exc:`hostname.exceptions.UnderscoreError`.
    See :doc:`underscore` for details.
