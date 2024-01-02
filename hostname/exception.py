# This is intended to wrap dns.exception

import dns.exception
import dns.name


class HostnameException(dns.exception.DNSException):
    """A generic expection abstractions"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class UnderscoreError(HostnameException):
    """An underscore appeared in a label it shouldn't have."""


class InvalidCharacter(HostnameException):
    """A forbidden character was found in a lable"""


class DigitOnlyError(HostnameException):
    """The rightmost label is contains only digits"""


# Looking at how dnspython handles INDA exceptions and doing
# that here wrt to DNS errors
class DomainNameException(HostnameException):
    """DNS Parsing raised an exception"""

    supp_kwargs = {"dns_exception"}
    fmt = "DNS syntax error: {dns_exception}"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
