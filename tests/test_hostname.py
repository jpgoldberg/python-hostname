import unittest
from typing import ClassVar, Union, Type, Tuple, Set, NamedTuple

import hostname.hostname as hn
import hostname.exception as exc

ExceptionType = Union[None, Type[Exception], Tuple[Type[Exception], ...]]


class TestVector(NamedTuple):
    candidate: str
    is_hostname: bool
    description: str
    exception: ExceptionType


class VariableVector(NamedTuple):
    candidate: str
    good_flags: Set[str]
    description: str
    exception_when_false: ExceptionType

    def to_vector(self, flags: Set[str]) -> TestVector:
        is_hostname: bool
        exception: ExceptionType
        if self.good_flags.issubset(flags):
            is_hostname = True
            exception = None
        else:
            is_hostname = False
            exception = self.exception_when_false

        return TestVector(
            self.candidate, is_hostname, self.description, exception
        )


class TestName(unittest.TestCase):
    # Results for these vectors do not vary as flags vary
    common_vectors: ClassVar[list[TestVector]] = [
        TestVector("an.ok.example", True, "simple", None),
        TestVector("a.single.letter", True, "single letter label", None),
        TestVector(
            "-initial.hyphen.example",
            False,
            "leading hyphen",
            exc.BadHyphenError,
        ),
        TestVector(
            "no..empty.labels", False, "empty label", exc.DomainNameException
        ),
        TestVector("123.456.78a", True, "digit labels ok", None),
        TestVector(
            "underscore.in.net_work",
            False,
            "not allowed in network names",
            exc.UnderscoreError,
        ),
        TestVector(
            "last.digits.123", False, "last label digits", exc.DigitOnlyError
        ),
        TestVector("3com.net", True, "Initial digit", None),
        TestVector(
            "a.b@d.example", False, "invalid character", exc.InvalidCharacter
        ),
    ]

    variable_vectors: ClassVar[list[VariableVector]] = [
        VariableVector(
            "szárba.szökik.hu", {"allow_idna"}, "idna", exc.NotASCIIError
        ),
        VariableVector(
            "under_score.in.host",
            {"allow_underscore"},
            "Controversial: no underscore at all",
            exc.UnderscoreError,
        ),
        VariableVector("", {"allow_empty"}, "empty", exc.NoLabelError),
    ]

    def test_is_hostname(self) -> None:
        # default flags are {"allow_idna"}
        other_vectors = [
            v.to_vector({"allow_idna"}) for v in self.variable_vectors
        ]
        for data, expected, desc, _ in self.common_vectors + other_vectors:
            with self.subTest(msg=desc):
                result = hn.is_hostname(data)
                self.assertEqual(result, expected)

    def test_allow_underscore(self) -> None:
        other_vectors = [
            v.to_vector({"allow_idna", "allow_underscore"})
            for v in self.variable_vectors
        ]
        for data, expected, desc, _ in self.common_vectors + other_vectors:
            with self.subTest(msg=desc):
                result = hn.is_hostname(data, allow_underscore=True)
                self.assertEqual(result, expected)

    def test_allow_empty(self) -> None:
        other_vectors = [
            v.to_vector({"allow_idna", "allow_empty"})
            for v in self.variable_vectors
        ]
        for data, expected, desc, _ in self.common_vectors + other_vectors:
            with self.subTest(msg=desc):
                result = hn.is_hostname(data, allow_empty=True)
                self.assertEqual(result, expected)

    def test_deny_idna(self) -> None:
        other_vectors = [v.to_vector(set()) for v in self.variable_vectors]
        for data, expected, desc, _ in self.common_vectors + other_vectors:
            with self.subTest(msg=desc):
                result = hn.is_hostname(data, allow_idna=False)
                self.assertEqual(result, expected)

    def test_validate(self) -> None:
        other_vectors = [
            v.to_vector({"allow_idna"}) for v in self.variable_vectors
        ]
        for data, _, desc, exception in self.common_vectors + other_vectors:
            if exception is not None:
                with self.subTest(msg=desc):
                    self.assertRaises(exception, hn.from_text, data)

    def test_type(self) -> None:
        self.assertRaises(exc.NotAStringError, hn.from_text, 1)


if __name__ == "__main__":
    unittest.main()
