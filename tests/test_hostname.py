import unittest
from typing import ClassVar, TypeAlias

import hostname.hostname as hn


class TestHostname(unittest.TestCase):
    TestString: TypeAlias = tuple[str, bool, str]

    test_strings: ClassVar[list[TestString]] = [
        ("a.good.example", True, "simple"),
        ("-initial.hyphen.example", False, "leading hyphen"),
        ("szárba.szökik.hu", True, "idna"),
        ("no..empty.labels", False, "empty label"),
        ("123.456.78a", True, "digit labels ok"),
        ("last.digits.123", False, "last label digits"),
        ("under_score.in.host", False, "Controversial: no underscore at all"),
        ("underscore.in.net_work", False, "not allowed in network names"),
        ("3com.net", True, "Initial digit"),
    ]

    def test_is_hostname(self) -> None:
        for data, expected, desc in self.test_strings:
            with self.subTest(msg=desc):
                result = hn.Hostname.is_hostname(data)
                self.assertEqual(result, expected)


class TestHostnameUnderscore(unittest.TestCase):
    TestString: TypeAlias = tuple[str, bool, str]

    test_strings: ClassVar[list[TestString]] = [
        ("a.good.example", True, "simple"),
        ("-initial.hyphen.example", False, "leading hyphen"),
        ("szárba.szökik.hu", True, "idna"),
        ("no..empty.labels", False, "empty label"),
        ("123.456.78a", True, "digit labels ok"),
        ("last.digits.123", False, "last label digits"),
        ("3com.net", True, "Initial digit"),
        ("under_score.in.host", True, "allowed with option"),
        ("underscore.in.net_work", False, "not allowed in network names"),
    ]

    def test_is_hostname(self) -> None:
        for data, expected, desc in self.test_strings:
            with self.subTest(msg=desc):
                result = hn.Hostname.is_hostname(data, hn.HostnameFlag.ALLOW_UNDERSCORE)
                self.assertEqual(result, expected)


if __name__ == "__main__":
    unittest.main()
