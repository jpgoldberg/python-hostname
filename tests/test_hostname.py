import unittest
from typing import ClassVar, TypeAlias, Union, Type, Tuple

import hostname.hostname as hn
import hostname.exception as exc

ExcptionType = Union[None, Type[Exception], Tuple[Type[Exception], ...]]


class TestHostname(unittest.TestCase):
    TestString: TypeAlias = tuple[str, bool, str, ExcptionType]

    test_strings: ClassVar[list[TestString]] = [
        ("a.good.example", True, "simple", None),
        (
            "-initial.hyphen.example",
            False,
            "leading hyphen",
            exc.BadHyphenError,
        ),
        ("szárba.szökik.hu", True, "idna", None),
        ("no..empty.labels", False, "empty label", exc.DomainNameException),
        ("123.456.78a", True, "digit labels ok", None),
        ("last.digits.123", False, "last label digits", exc.DigitOnlyError),
        (
            "under_score.in.host",
            False,
            "Controversial: no underscore at all",
            exc.UnderscoreError,
        ),
        (
            "underscore.in.net_work",
            False,
            "not allowed in network names",
            exc.UnderscoreError,
        ),
        ("3com.net", True, "Initial digit", None),
        ("", False, "empty", exc.NoLabelError),
        ("a.b@d.example", False, "invalid character", exc.InvalidCharacter),
    ]

    def test_is_hostname(self) -> None:
        for data, expected, desc, _ in self.test_strings:
            with self.subTest(msg=desc):
                result = hn.is_hostname(data)
                self.assertEqual(result, expected)


class TestHostnameFlags(unittest.TestCase):
    TestString: TypeAlias = tuple[str, bool, str]

    test_strings: ClassVar[list[TestString]] = [
        ("a.good.example", True, "simple"),
        ("-initial.hyphen.example", False, "leading hyphen"),
        ("szárba.szökik.hu", True, "idna"),
        ("no..empty.labels", False, "empty label"),
        ("123.456.78a", True, "digit labels ok"),
        ("last.digits.123", False, "last label digits"),
        ("3com.net", True, "Initial digit"),
        ("underscore.in.net_work", False, "not allowed in network names"),
        ("a.b@d.example", False, "invalid character"),
    ]

    def test_allow_underscore(self) -> None:
        for data, expected, desc in self.test_strings + [
            ("under_score.in.host", True, "allowed with option"),
            ("", False, "empty"),
        ]:
            with self.subTest(msg=desc):
                result = hn.is_hostname(data, hn.HostnameFlag.ALLOW_UNDERSCORE)
                self.assertEqual(result, expected)

    def test_allow_empty(self) -> None:
        for data, expected, desc in self.test_strings + [
            ("under_score.in.host", False, "allowed with option"),
            ("", True, "empty"),
        ]:
            with self.subTest(msg=desc):
                result = hn.is_hostname(data, hn.HostnameFlag.ALLOW_EMPTY)
                self.assertEqual(result, expected)


class TestNameExceptions(unittest.TestCase):
    TestString: TypeAlias = tuple[str, bool, str, ExcptionType]

    test_strings: ClassVar[list[TestString]] = [
        ("a.good.example", True, "simple", None),
        (
            "-initial.hyphen.example",
            False,
            "leading hyphen",
            exc.BadHyphenError,
        ),
        ("szárba.szökik.hu", True, "idna", None),
        ("no..empty.labels", False, "empty label", exc.DomainNameException),
        ("123.456.78a", True, "digit labels ok", None),
        ("last.digits.123", False, "last label digits", exc.DigitOnlyError),
        (
            "under_score.in.host",
            False,
            "Controversial: no underscore at all",
            exc.UnderscoreError,
        ),
        (
            "underscore.in.net_work",
            False,
            "not allowed in network names",
            exc.UnderscoreError,
        ),
        ("3com.net", True, "Initial digit", None),
        ("", False, "empty", exc.NoLabelError),
        ("a.b@d.example", False, "invalid character", exc.InvalidCharacter),
    ]

    def test_validate(self) -> None:
        for data, _, desc, exception in self.test_strings:
            if exception is not None:
                with self.subTest(msg=desc):
                    self.assertRaises(exception, hn.from_text, data)

    def test_type(self) -> None:
        self.assertRaises(exc.NotAStringError, hn.from_text, 1)


if __name__ == "__main__":
    unittest.main()
