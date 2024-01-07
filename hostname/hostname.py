from typing import Any, TypeGuard, Iterable, Union, Optional
from enum import Flag, auto

import hostname.exception as exc

import dns.name
import dns.exception

import idna

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
    DENY_IDNA = auto()


class Name(dns.name.Name):

    """A host name.

    A hostname.hostname.Name class is a kind of dns.name.Name,
    with additional syntactic constraints specific to hostnames.
    """

    flag_default = HostnameFlag(0)

    def __init__(
        self,
        labels: Iterable[Union[bytes, str]],
        flags: Optional[HostnameFlag] = None,
    ):
        try:
            super().__init__(labels)
        except Exception as e:
            raise exc.DomainNameException(dns_exception=e) from e

        # dns.name.Name is immutable, so we call the mother of all __setattr__
        # to set self.flags
        if flags is None:
            object.__setattr__(self, "flags", self.flag_default)
        else:
            object.__setattr__(self, "flags", flags)

        mutable_flags = self.__getattribute__("flags")

        # We need a mutatable list of the labels, and
        # it will be convenient to have them be strings.
        host_labels: list[str] = self.to_unicode().split(".")
        # Exclude the root "" label for our checks
        if host_labels[-1] == "":
            host_labels = host_labels[:-1]

        # Reject empty hostname
        if len(host_labels) == 0:
            raise exc.NoLabelError

        for label in host_labels:
            _validate_host_label(
                label, mutable_flags
            )  # will raise exceptions on failure

            # only allowed in first label
            mutable_flags = mutable_flags & ~HostnameFlag.ALLOW_UNDERSCORE

        # Last (most significant) label cannot be all digits
        if all(c.isdigit() for c in host_labels[-1]):
            raise exc.DigitOnlyError


def from_text(s: Any, flags: Optional[HostnameFlag] = None) -> Name:
    """retruns a Name if input is synatically valid.

    If validation fails, this raises a HostnameException with some details of
    why it failed

    *flags*
        *HostnameFlags.ALLOW_UNDERSCORE* allows an underscore in the the first
        label. This is non-standard behavior. Use the default (False) unless
        you have a compelling reason to perpetuate non-standard behavior and
        run the risk of security problems many years from now.
    """

    if not isinstance(s, str):
        raise TypeError("Expected str input")

    try:
        dname = dns.name.from_text(s)
    except Exception as e:
        raise exc.DomainNameException(dns_exception=e) from e

    if flags is None:
        flags = HostnameFlag(0)

    return Name(dname.labels, flags=flags)


def is_hostname(s: Any, flags: HostnameFlag | None = None) -> TypeGuard[Name]:
    """retruns True iff s is a standards complient Internet hostname.

    Returns True when s is a valid hostname following RFCs defining hostnames, domain names, and IDNA.

    *flags*
        *HostnameFlags.ALLOW_UNDERSCORE* allows an underscore in the the first label. This is non-standard behavior. Use the default (False) unless you have a compelling reason to perpetuate non-standard behavior and run the risk of security problems many years from now.
    """

    try:
        from_text(s, flags)
    except Exception:
        return False
    return True


def _validate_host_label(label: str, restrictions: HostnameFlag) -> bool:
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

    blabel: bytes = label.encode()

    ## breaking up statements for debugging
    is_label_ascii: bool = label.isascii()
    if not is_label_ascii:
        try:
            blabel = idna.alabel(label)
        except Exception as e:
            raise exc.INDAException(idna_exception=e) from e

    if HostnameFlag.ALLOW_UNDERSCORE in restrictions:
        underHack = _UNDERSCORE
    else:
        underHack = _NO_SUCH_BYTE

    # check for bad hyphens *before* punycode encoding
    if blabel.startswith(_HYPHEN.to_bytes()) or blabel.endswith(
        _HYPHEN.to_bytes()
    ):
        raise exc.BadHyphenError

    for c in blabel:
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
