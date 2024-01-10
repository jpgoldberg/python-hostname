from typing import Any, TypeGuard, Optional
from enum import Flag, auto

import hostname.exception as exc

import dns.name
import dns.exception

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


class HostnameFlag(Flag):
    """Flags for deviating from default hostname validation.

    *ALL_UNDERSCORE* allows an underscore in the leftmost label.

    *DENY_IDNA* Candidate hostname must be 7 bit ASCII.
    """

    ALLOW_UNDERSCORE = auto()
    ALLOW_IDNA = auto()
    ALLOW_EMPTY = auto()

    DEFAULT = ~ALLOW_UNDERSCORE & ALLOW_IDNA & ~ALLOW_EMPTY


class Name:

    """A host name.

    A hostname.hostname.Name class is a kind of dns.name.Name,
    with additional syntactic constraints specific to hostnames.
    """

    def __init__(self, hostname: str, flags: Optional[HostnameFlag] = None):
        # dns.name.Name is immutable, so we call the mother of all __setattr__
        # to set self.flags

        if not isinstance(hostname, str):
            raise exc.NotAStringError

        try:
            self.dnsname = dns.name.from_text(hostname)
        except Exception as e:
            raise exc.DomainNameException(dns_exception=e) from e

        self.flags = HostnameFlag.DEFAULT
        if flags is not None:
            self.flags = flags

        # We need a mutatable list of the labels, and
        # it will be convenient to have them be strings.
        host_labels: list[bytes] = [e for e in self.dnsname.labels]
        # Exclude the root "" label for our checks
        if host_labels[-1] == b"":
            host_labels.pop()

        # Reject empty hostname
        if len(host_labels) == 0:
            raise exc.NoLabelError

        mutable_flags = self.flags
        for label in host_labels:
            _validate_host_label(
                label, mutable_flags
            )  # will raise exceptions on failure

            # only allowed in first label
            mutable_flags = mutable_flags & ~HostnameFlag.ALLOW_UNDERSCORE

        # Last (most significant) label cannot be all digits
        if all(b >= _DIGIT_0 and b <= _DIGIT_9 for b in host_labels[-1]):
            raise exc.DigitOnlyError


def from_text(hostname: str, flags: Optional[HostnameFlag] = None) -> Name:
    """retruns a Name if input is synatically valid.

    If validation fails, this raises a HostnameException with some details of
    why it failed

    *flags*
        *HostnameFlags.ALLOW_UNDERSCORE* allows an underscore in the the first
        label. This is non-standard behavior. Use the default (False) unless
        you have a compelling reason to perpetuate non-standard behavior and
        run the risk of security problems many years from now.
    """

    return Name(hostname, flags=flags)


def is_hostname(
    candidate: Any, flags: HostnameFlag | None = None
) -> TypeGuard[Name]:
    """retruns True iff candidate is a standards complient Internet hostname.

    True when candidate is a valid hostname following RFCs defining hostnames, domain names, and IDNA.

    *flags*
        *HostnameFlags.ALLOW_UNDERSCORE* allows an underscore in the the first label. This is non-standard behavior. Use the default (False) unless you have a compelling reason to perpetuate non-standard behavior and run the risk of security problems many years from now.
    """

    try:
        Name(candidate, flags)
    except exc.HostnameException:
        return False
    return True


def _validate_host_label(label: bytes, flags: HostnameFlag) -> bool:
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

    # inda.alabel() performs a number of hostname well-formedness checks,
    # but details of which and the exceptions raised does not appear to be
    # documented in sufficient detail, we won't defer to it. Thus, we will only
    # call idna.alabel() on non-ascii candidate labels.

    if HostnameFlag.ALLOW_UNDERSCORE in flags:
        underHack = _UNDERSCORE
    else:
        underHack = _NO_SUCH_BYTE

    # check for bad hyphens *before* punycode encoding
    if label.startswith(_HYPHEN.to_bytes()) or label.endswith(
        _HYPHEN.to_bytes()
    ):
        raise exc.BadHyphenError

    for c in label:
        if not (
            (c >= _LOWER_A and c <= _LOWER_Z)
            or (c >= _UPPER_A and c <= _UPPER_Z)
            or (c >= _DIGIT_0 and c <= _DIGIT_9)
            or c == _HYPHEN
            or c == underHack
        ):
            if c == _UNDERSCORE:
                raise exc.UnderscoreError
            else:
                raise exc.InvalidCharacter
        # Starting or ending with "-" is also forbidden.

    return True
