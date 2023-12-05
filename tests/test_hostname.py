import unittest
from typing import ClassVar, TypeAlias

from src.hostname import hostname


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
    ]

    def test_is_hostname(self) -> None:
        for data, expected, desc in self.test_strings:
            with self.subTest(msg=desc):
                result = hostname.Hostname.is_hostname(data)
                self.assertEqual(result, expected)


if __name__ == "__main__":
    unittest.main()
