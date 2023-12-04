import unittest
from typing import TypeAlias

import hostname


class TestHostname(unittest.TestCase):
    TestString: TypeAlias = tuple[str, bool, str]

    test_strings: list[TestString] = [
        ("a.good.example", True, "simple"),
        ("-initial.hyphen.example", False, "leading hyphen"),
    ]

    def test_is_hostname(self) -> None:
        for data, expected, desc in self.test_strings:
            with self.subTest(msg=desc):
                result = hostname.Hostname.is_hostname(data)
                self.assertEqual(result, expected)


if __name__ == "__main__":
    unittest.main()
