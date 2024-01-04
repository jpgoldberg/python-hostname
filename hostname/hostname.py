from typing import Any, Self, TypeGuard
from enum import Flag, auto

import hostname.exception as exc

import dns.name
import dns.exception


class HostnameFlag(Flag):
    """Flags for deviating from default hostname validation.

    *ALL_UNDERSCORE* allows an underscore in the leftmost label.

    *DENY_IDNA* Candidate hostname must be 7 bit ASCII.
    """

    ALLOW_UNDERSCORE = auto()
    DENY_IDNA = auto()


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
    def validate(cls, s: Any, flags: HostnameFlag | None = None) -> str:
        """retruns a canonical form of the hostname if s is valid.

        If validation fails, this raises a HostnameException with some details of why it failed

        *flags*
          *HostnameFlags.ALLOW_UNDERSCORE* allows an underscore in the the first label. This is non-standard behavior. Use the default (False) unless you have a compelling reason to perpetuate non-standard behavior and run the risk of security problems many years from now.
        """

        if flags is None:
            flags = HostnameFlag(0)

        if not isinstance(s, str | bytes):
            raise TypeError("Expected str input")

        # checks DNS requirements and converts to punycode if needed.
        try:
            dname: dns.name.Name = dns.name.from_text(s).canonicalize()
        except Exception as e:
            raise exc.DomainNameException(dns_exception=e) from e

        labels: tuple[bytes, ...] = dname.labels

        # remove root (most significant) label
        labels = labels[:-1]

        # Reject empty hostname
        if len(labels) == 0:
            raise exc.NoLabelError

        for label in labels:
            cls._validate_label(
                label, flags
            )  # will raise exceptions on failure

            # only allowed in first label
            flags = flags & ~HostnameFlag.ALLOW_UNDERSCORE

        # Last (most significant) label cannot be all digits
        if all(c >= cls._DIGIT_0 and c <= cls._DIGIT_9 for c in labels[-1]):
            raise exc.DigitOnlyError

        return dname.to_text()

    @classmethod
    def is_hostname(
        cls, s: Any, flags: HostnameFlag | None = None
    ) -> TypeGuard[Self]:
        """retruns True iff s is a standards complient Internet hostname.

        Returns True when s is a valid hostname following RFCs defining hostnames, domain names, and IDNA.

        *flags*
          *HostnameFlags.ALLOW_UNDERSCORE* allows an underscore in the the first label. This is non-standard behavior. Use the default (False) unless you have a compelling reason to perpetuate non-standard behavior and run the risk of security problems many years from now.
        """

        try:
            cls.validate(s, flags)
        except Exception:
            return False
        return True

    @classmethod
    def _validate_label(cls, label: bytes, restrictions: HostnameFlag) -> bool:
        """For a valid dns label, s, is valid hostname label.

        Raises exeptions of various failures
        """

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

        # underHack will be the ord value for the underscore when that is
        # allowed or an int that will never be a byte.
        if HostnameFlag.ALLOW_UNDERSCORE in restrictions:
            underHack = cls._UNDERSCORE
        else:
            underHack = cls._NO_SUCH_BYTE

        for c in label:
            if not (
                (c >= cls._LOWER_A and c <= cls._LOWER_Z)
                or (c >= cls._UPPER_A and c <= cls._UPPER_Z)
                or (c >= cls._DIGIT_0 and c <= cls._DIGIT_9)
                or c == cls._HYPHEN
                or c == underHack
            ):
                if c == cls._UNDERSCORE:
                    raise exc.UnderscoreError
                else:
                    raise exc.InvalidCharacter
            # Starting or ending with "-" is also forbidden.

        if cls._HYPHEN in (label[0], label[-1]):
            raise exc.BadHyphenError
        return True
