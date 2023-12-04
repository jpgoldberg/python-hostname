from typing import TypeGuard, Any, Self
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

    @classmethod
    def is_hostname(cls, s: Any) -> TypeGuard[Self]:
        if not isinstance(s, (str, bytes)):
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

        # A faster implementation would be to inline this
        if not all([cls._is_label(label) for label in labels]):
            return False

        # Last (most significant) label cannot be all digits
        if all(c >= cls._DIGIT_0 and c <= cls._DIGIT_9 for c in labels[-1]):
            return False

        return True

    @classmethod
    def _is_label(cls, label: bytes) -> bool:
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

        for c in label:
            if not (
                (c >= cls._LOWER_A and c <= cls._LOWER_Z)
                or (c >= cls._UPPER_A and c <= cls._UPPER_Z)
                or (c >= cls._DIGIT_0 and c <= cls._DIGIT_9)
                or c == cls._HYPHEN
            ):
                return False
            # Starting or ending with "-" is also forbidden.
        if label[0] == cls._HYPHEN or label[-1] == cls._HYPHEN:
            return False
        return True
