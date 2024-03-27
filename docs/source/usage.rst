Using |project|
===============

Common signature
----------------

The class, :class:`Hostname`, and the function, :func:`is_hostname`, described here have a common signature:

  :samp:`{funcOrClass}(candidate: Any, **kwargs: bool) -> {rtype}`

In normal usage, ``candidate`` must be a :py:class:`str`,
and non-string inputs will result in failure,
though not a :py:exc:`TypeError`. [#TypeError]_

Details on the keyword arguments are described in :ref:`sec-flags` below.



The function
-------------

.. autofunction:: hostname.is_hostname

The function, :func:`hostname.is_hostname` returns |True| if and only
if its argument is a syntactically valid hostname.
It's behavior can be adjusted slightly with some flags which can be set as keyword arguements.

>>> is_hostname("a.go-od.example")
True

>>> is_hostname("a.-bad.example")
False

Additionally it acts as a :pep:`647` :py:class:`typing.TypeGuard`,
allowing type checkers to know that any object which
passes the test is a :class:`hostname.Hostname`.


.. code-block:: python

    import hostname

    def do_something_with_hostname(hostname: hostname.Hostname) -> None:
        ...

    name1: str = "www.example"

    do_something_with_hostname(name1)  # Fails type checking

    if not hostname.is_hostname(name1):
        raise TypeError('Expected valid Hostname')
    do_something_with_hostname(name1)  # Passes type checking

    name1 = name1.upper() # creates new str object.
    do_something_with_hostname(name1)  # Fails type checking

Note that the :py:class:`typing.TypeGuard` mechanism only
affects static type checking.
To create an instance of the :class:`hostname.Hostname` class initilize a Hostname:

>>> s = 'example.com'
>>> is_hostname(s)
True
>>> isinstance(s, hostname.Hostname)
False
>>> t = hostname.Hostname('example.com')
>>> isinstance(t, hostname.Hostname)
True

.. note::

    Although underlyingly hostnames are case insensitive
    that does not hold for internationalized hostnames.
    Althouh both valid, ``straße.example`` is not equivalent to
    ``STRASSE.EXAMPLE``.

    >>> 'straße.example'.upper()
    'STRASSE.EXAMPLE'


Hostname class
--------------

The :class:`hostname.Hostname` is a subtype of :py:class:`str`.

If ``candidate`` is not a valid hostname,
initializing the class will raise one of the
:exc:`hostname.exception.HostnameException` :doc:`exceptions`.
``**kwargs`` are described in :ref:`sec-flags`.


.. autoclass:: hostname.Hostname
    :members:

Because :class:`~hostname.Hostname` is a subclass of :py:class:`str`,
all ``str`` methods are available.
But it is important to note that what is returned by those inherited methods is not a :class:`hostname.Hostname`.

>>> h = hostname.Hostname('foo.example')
>>> isinstance(h, hostname.Hostname)
True
>>> isinstance(h.upper(), hostname.Hostname)
False


.. _sec-flags:

Flags
-----

The possible keyword arguments are the booleans, ``allow_idna``, ``allow_underscore``, and ``allow_empty``.

.. _flag-allow_idna:

``allow_idna`` (Allow non-ASCII hostnames)
    When |True|, a hostname candidate hostname like
    ``"szárba.szökik.hu"`` will be accepted.
    When |False| such a candidate will raise an
    :exc:`hostname.exception.NotASCIIError` error.

    Default |True|

    >>> is_hostname("szárba.szökik.hu")
    True

    >>> is_hostname("szárba.szökik.hu", allow_idna=False)
    False

    >>> is_hostname("szarba.szokik.hu", allow_idna=False)
    True

.. _flag-allow_empty:

``allow_empty`` (Allow the empty string as a valid hostname)
    When |True|, a hostname candidate hostname like
    ``""`` will be accepted.
    When |False| such a candidate will raise an
    :exc:`hostname.exception.NoLabelError` error.

    Default |False|

    >>> is_hostname("")
    False

    >>> is_hostname("", allow_empty=True)
    True

.. _flag-allow_underscore:

``allow_underscore`` (Allow underscore in leftmost label)
    When |True|, a hostname candidate hostname like
    ``"under_score.in.host"`` will be accepted.
    When |False| such a candidate will raise an
    :exc:`hostname.exception.UnderscoreError` error.

    Default |False|

    >>> is_hostname("under_score.in.host")
    False

    >>> is_hostname("under_score.in.host", allow_underscore=True)
    True


    In all cases, a candidate with an underscore anywhere other than
    in the first (leftmost) label,
    such as ``"underscore.in.net_work"`` will raise an  :exc:`hostname.exception.UnderscoreError`.

    >>> is_hostname("leftmost.not_leftmost.example")
    False

    >>> is_hostname("leftmost.not_leftmost.example", allow_underscore=True)
    False

    See :doc:`underscore` for details and rationale.



.. rubric:: Footnotes

.. [#TypeError] In the case of :func:`hostname.is_hostname`,
    we want the function to accept any input,
    but return |False| for all instances of the
    candidate not being a valid hostname.
    Not being a string is just one reason for not being valid.

    In case of the class initiations, we want to reserve :py:exc:`TypeError`
    for bad types of other arguments.
    When the candidate hostname is not a string, we raise :class:`hostname.exception.NotAStringError`.
