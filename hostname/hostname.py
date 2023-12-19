from typing import Any, Self, TypeGuard

import dns.name


class Hostname:
    # We will be legitimately be making some ASCII assumptions
    _LOWER_A = ord("a")
    _LOWER_Z = ord("z")
    _UPPER_A = ord("A")
    _UPPER_Z = ord("Z")
    _DIGIT_0 = ord("0")
    _DIGIT_9 = ord("9")
    _HYPHEN = ord("-")
    _UNDERSCORE = ord("_")
    _NO_SUCH_BYTE = -1

    @classmethod
    def is_hostname(cls, s: Any, allow_underscore: bool = False) -> TypeGuard[Self]:
        """retruns True iff s is a standards complient Internet hostname.

        Returns True when s is a valid hostname following RFCs defining
        hostnames, domain names, and IDNA.

        *allow_underscore* is a ``bool``. If true underscores are
        allowed in in the first label.
        This is non-standard behavior.
        The default is False.
        Use the default (False) unless you have a compelling reason to
        perpetuate non-standard behavior and run the risk of
        security problems many years from now.
        """
        if not isinstance(s, str | bytes):
            return False

        # checks DNS requirements and converts to punycode if needed.
        try:
            dname: dns.name.Name = dns.name.from_text(s).canonicalize()
        except Exception:
            return False
        labels: tuple[bytes, ...] = dname.labels

        # remove root (most significant) label
        labels = labels[:-1]

        # Reject empty hostname
        if len(labels) == 0:
            return False

        for i, label in enumerate(labels, 1):
            if i != 1:
                # if allowed, only in first label
                allow_underscore = False
            if cls._is_label(label, allow_underscore) is False:
                return False

        # Last (most significant) label cannot be all digits
        if all(c >= cls._DIGIT_0 and c <= cls._DIGIT_9 for c in labels[-1]):
            return False

        return True

    @classmethod
    def _is_label(cls, label: bytes, allow_underscore: bool = False) -> bool:
        """For a valid dns label, s, is valid hostname label"""

        # Valid dns labels are already ASCII and meet length
        # requirements.
        #
        # Labels are composed of letters, digits and hyphens
        # A hyphen cannot be either the first or the last
        # character.
        #
        # Note that it is very easy to the the regular expression
        # for RFC 952 wrong. And if we can avoid importing the
        # regular expression package all together, that is even
        # better.
        #
        # I am taking this from Bob Halley's suggestion on GitHub
        #
        #   https://github.com/rthalley/dnspython/issues/1019#issuecomment-1837247696
        #
        # Remember kids, don't play with character ranges this
        # way unless you have already checked that you are using
        # 7-bit ASCII.

        if len(label) == 0:
            return False

        # underHack will be the ord value for the underscore when that is
        # allowed or an int that will never be a byte.
        underHack = cls._UNDERSCORE if allow_underscore else cls._NO_SUCH_BYTE

        for c in label:
            if not (
                (c >= cls._LOWER_A and c <= cls._LOWER_Z)
                or (c >= cls._UPPER_A and c <= cls._UPPER_Z)
                or (c >= cls._DIGIT_0 and c <= cls._DIGIT_9)
                or c == cls._HYPHEN
                or c == underHack
            ):
                return False
            # Starting or ending with "-" is also forbidden.
        if cls._HYPHEN in (label[0], label[-1]):
            return False
        return True
