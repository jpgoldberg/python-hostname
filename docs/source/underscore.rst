Underscores
============

The underscore character "``_``" is not allowed in Internet standard hostnames.
Canditate hostnames with underscores in them are not valid hostnames.
Allowing underscores in hostnames is an error.

Do not use the :ref:`allow_underscore<flag-allow_underscore>` flag.

Parser mismatch is bad
-----------------------
Parser mismatch or parser inconsistancy is bad.
Having multiple parsers treat data differently can
and has led to security problems.

For a rundown of a few examples, I refer you to
Tim McCormack's
`What is a parser mismatch vulnerability? <https://www.brainonfire.net/blog/2022/04/11/what-is-parser-mismatch/>`_

The most notorious examples involve URL parsing,
but there are many more cases, some of them quite subtle
involving vaguenss in standards.

Many vulnerabilities originate from attemps to remain compatable with
non-standard complient systems.
Often times, the vulnerabity only shows up years later.
HTTP Request Smuggling through inconsistent header parsing is an example.
At the time that the lax parsing was introduced, it was harmless.
It was only after other features where added to HTTP headers did seemingly harmless acceptence of invalid header syntax create a security vulnerability.

We cannot know what vulnerabities may arise in the future do to some systems accepting invalid hostnames, but we know that we can reduce
those future dangers by more strongly enforcing standards complience today.

History
-------

The standards do not allow the underscore character, "``_``",
to appear in a hostname.
However some Internet software doesn't enforce that,
and there was a time when some systems created such names in the most local (leftmost) part of a hostname.

The account I offer here of why some systems do erroneously accept underscores in hostnames is based on unreliable memory and
some speculation.

Microsoft's Windows 95 operating system produced hostnames with underscores.
Locally machines names could have names like "``Alices Computer``".
When Windows 95 needed to present that to the Internet as a hostname label,
it would convert it to "`alices_computer`".
This was certainly the case when constructed the SMTP ``HELO`` message,
which required the client's hostname.

Sendmail, the overwhelmingly dominant mail transport agent at the time,
allowed hostnames with underscores.
Sendmail's acceptance of invalid hostnames  had probably been programming oversight at the time instead of a deliberate decision.
The combination of
a large number hosts sending invalid hostnames to major parts of Internet infrastructure
which in turn accepted those invalid hostname
led to such malformed hostnames being widely accepted.

Many regular expression libraries have the pattern ``\w``
which can be thought of as matching characters that can be part of words. These also match the underscore.
Python's  :py:mod:`re` documentation for ``\w`` says,

    For Unicode (str) patterns:
      Matches Unicode word characters; this includes all Unicode alphanumeric characters (as defined by :py:meth:`str.isalnum`), as well as the underscore (``_``).

    Matches ``[a-zA-Z0-9_]`` if the ASCII flag is used.

I do not know the extent to which this contributes the persistence of the problem,
but I have seen attempts at hostname matching that use regular expressions with ``\w``.
