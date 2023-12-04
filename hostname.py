from typing import TypeGuard, Any, Self
import re
import dns.name


class Hostname:
    @classmethod
    def is_hostname(cls, s: Any) -> TypeGuard[Self]:
        if not isinstance(s, (str, bytes)):
            return False

        # checks DNS requirements and converts to punycode if needed.
        try:
            dname: dns.name.Name = dns.name.from_text(s).canonicalize()
        except Exception:
            return False
        labels = dname.to_text().split(".")

        # remove root (most significant) label
        labels = labels[:-1]

        # Reject empty hostname
        if len(labels) == 0:
            return False

        # A faster implementation would be to inline this
        # and to avoid regular expressions by following
        # the example in
        #    https://github.com/rthalley/dnspython/issues/1019#issuecomment-1837247696

        if not all([cls._is_label(label) for label in labels]):
            return False

        # Last (most significant) label cannot be all digits
        if re.match(r"^\d+$", labels[-1]):
            return False

        return True

    @staticmethod
    def _is_label(s: str) -> bool:
        """For a valid dns label, s, is valid hostname label"""

        # Valid dns labels are already ASCII and mean length
        # requirements.
        #
        # Labels are composed of letters, digits and hyphens
        # A hyphen cannot be either the first or the last
        # character.
        # Note that because labels can be a single character
        # long, a single regular expression for this neither
        # simple nor human readable. So best to use separate
        # checks

        if not re.match(r"^[a-z\d-]*$", s):
            return False

        if s[0] == "-" or s[-1] == "-":
            return False

        return True
