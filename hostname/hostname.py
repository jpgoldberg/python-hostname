from typing import Any, TypeGuard

import hostname.exception as exc

import dns.name
import dns.exception


class Name:

    """A hostname

    A hostname must been all of the requirements of a domain name along with
    addtional contraints that are specific to hostnames.
    """

    _dnsname: dns.name.Name
    _flags: dict[str, bool]
    _labels: list[bytes]

    DEFAULT_FLAGS: dict[str, bool] = {
        "allow_underscore": False,
        "allow_empty": False,
        "allow_idna": True,
    }

    def __init__(self, hostname: str, **kwargs: bool):
        if not isinstance(hostname, str):
            raise exc.NotAStringError

        self._flags = self.DEFAULT_FLAGS.copy()
        for k, v in kwargs.items():
            if k not in self.DEFAULT_FLAGS:
                raise ValueError(f'Unknown option "{k}"')
            self._flags[k] = v

        if not (hostname.isascii() or self._flags["allow_idna"]):
            raise exc.NotASCIIError

        try:
            self._dnsname = dns.name.from_text(hostname)
        except Exception as e:
            raise exc.DomainNameException(dns_exception=e) from e

        # We need a mutatable list of the labels to deal with root
        self._labels: list[bytes] = [e for e in self._dnsname.labels]
        # Exclude the root "" label for our checks
        if self._labels[-1] == b"":
            self._labels.pop()

        # Reject empty hostname unless allowed
        if len(self._labels) == 0:
            if not self._flags["allow_empty"]:
                raise exc.NoLabelError
            else:
                return

        for idx, label in enumerate(self._labels):
            self._validate_label(idx, label)

    @property
    def dnsname(self) -> dns.name.Name:
        """Returns a dns.name.Name"""
        return self._dnsname

    @property
    def flags(self) -> dict[str, bool]:
        """Returns the flags used when valicating this hostname"""
        return self._flags

    @property
    def labels(self) -> list[bytes]:
        """Returns a list of labels, ordered from leftmost to rightmost.

        Returned list never includes the DNS root label "", if you want
        the full DNS labels use dnsname().labels
        """
        return self._labels

    def _validate_label(self, index: int, label: bytes) -> bool:
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

        # We will be legitimately be making some ASCII assumptions
        LOWER_A = ord("a")
        LOWER_Z = ord("z")
        UPPER_A = ord("A")
        UPPER_Z = ord("Z")
        DIGIT_0 = ord("0")
        DIGIT_9 = ord("9")
        HYPHEN = ord("-")
        UNDERSCORE = ord("_")
        NO_SUCH_BYTE = -1

        first: bool = True if index == 0 else False
        last: bool = True if index == len(self._labels) - 1 else False

        # Even allow_underscore only allows it in the first label
        # underHack will be the ord value for the underscore when that is
        # allowed or an int that will never be a byte.
        if self._flags["allow_underscore"] and first:
            underHack = UNDERSCORE
        else:
            underHack = NO_SUCH_BYTE

        # Last (most significant) label cannot be all digits
        if last:
            if all(b >= DIGIT_0 and b <= DIGIT_9 for b in label):
                raise exc.DigitOnlyError

        # Hyphens cannot be at start or end of label
        if label.startswith(b"-") or label.endswith(b"-"):
            raise exc.BadHyphenError

        for c in label:
            if not (
                (c >= LOWER_A and c <= LOWER_Z)
                or (c >= UPPER_A and c <= UPPER_Z)
                or (c >= DIGIT_0 and c <= DIGIT_9)
                or c == HYPHEN
                or c == underHack
            ):
                if c == UNDERSCORE:
                    raise exc.UnderscoreError
                else:
                    raise exc.InvalidCharacter

        return True


def from_text(hostname: str, **kwargs: bool) -> Name:
    """retruns a Name if input is synatically valid.

    If validation fails, this raises a HostnameException with some details of
    why it failed

    *flags*
        *HostnameFlags.ALLOW_UNDERSCORE* allows an underscore in the the first
        label. This is non-standard behavior. Use the default (False) unless
        you have a compelling reason to perpetuate non-standard behavior and
        run the risk of security problems many years from now.
    """

    return Name(hostname, **kwargs)


def is_hostname(candidate: Any, **kwargs: bool) -> TypeGuard[Name]:
    """retruns True iff candidate is a standards complient Internet hostname.

    True when candidate is a valid hostname following RFCs defining hostnames, domain names, and IDNA.

    *flags*
        *HostnameFlags.ALLOW_UNDERSCORE* allows an underscore in the the first label. This is non-standard behavior. Use the default (False) unless you have a compelling reason to perpetuate non-standard behavior and run the risk of security problems many years from now.
    """

    try:
        Name(candidate, **kwargs)
    except exc.HostnameException:
        return False
    return True
