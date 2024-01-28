import unittest
from typing import (
    ClassVar,
    Union,
    Type,
    Tuple,
    Set,
    NamedTuple,
)

from powerset_generator import subsets

import hostname.name as hn
import hostname.exception as exc

ExceptionType = Union[None, Type[Exception], Tuple[Type[Exception], ...]]


class TVector(NamedTuple):
    candidate: str
    is_hostname: bool
    description: str
    exception: ExceptionType


class VariableVector(NamedTuple):
    candidate: str
    good_flags: Set[str]
    description: str
    exception_when_false: ExceptionType

    def to_vector(self, flags: Set[str]) -> TVector:
        is_hostname: bool
        exception: ExceptionType
        if self.good_flags.issubset(flags):
            is_hostname = True
            exception = None
        else:
            is_hostname = False
            exception = self.exception_when_false

        return TVector(
            self.candidate, is_hostname, self.description, exception
        )


class TestName(unittest.TestCase):
    # First I over-engineer the way we handle combinations of different
    # flags for testing.
    known_flags: set[str] = {"allow_idna", "allow_underscore", "allow_empty"}

    @classmethod
    def flagset_to_dict(cls, flags: set[str]) -> dict[str, bool]:
        return {f: f in flags for f in cls.known_flags}

    # Results for these vectors do not vary as flags vary
    common_vectors: ClassVar[list[TVector]] = [
        TVector("an.ok.example", True, "simple", None),
        TVector("a.single.letter", True, "single letter label", None),
        TVector(
            "-initial.hyphen.example",
            False,
            "leading hyphen",
            exc.BadHyphenError,
        ),
        TVector(
            "no..empty.labels", False, "empty label", exc.DomainNameException
        ),
        TVector("123.456.78a", True, "digit labels ok", None),
        TVector(
            "underscore.in.net_work",
            False,
            "not allowed in network names",
            exc.UnderscoreError,
        ),
        TVector(
            "last.digits.123", False, "last label digits", exc.DigitOnlyError
        ),
        TVector("3com.net", True, "Initial digit", None),
        TVector(
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

    def test_default(self) -> None:
        # default flags are {"allow_idna"}

        flagset = {"allow_idna"}
        other_vectors = [v.to_vector(flagset) for v in self.variable_vectors]
        for data, expected, desc, _ in self.common_vectors + other_vectors:
            with self.subTest(msg=desc):
                result = hn.is_hostname(data)
                self.assertEqual(result, expected)

    def test_flag_combinations(self) -> None:
        for flagset in subsets(TestName.known_flags):
            other_vectors = [
                v.to_vector(flagset) for v in self.variable_vectors
            ]
            vectors: list[TVector] = self.common_vectors + other_vectors
            for data, expected, desc, _ in vectors:
                with self.subTest(msg=f"{desc} {flagset}"):
                    result = hn.is_hostname(
                        data, **TestName.flagset_to_dict(flagset)
                    )
                    self.assertEqual(result, expected)

    def test_exceptions(self) -> None:
        # Should promgrammatically construct this
        for flagset in subsets(TestName.known_flags):
            other_vectors = [
                v.to_vector(flagset) for v in self.variable_vectors
            ]
            for data, _, desc, exception in (
                self.common_vectors + other_vectors
            ):
                # We must explicitly narrow exception
                if exception is not None:
                    with self.subTest(msg=f"{desc} {flagset}"):
                        self.assertRaises(
                            exception,
                            hn.Name,
                            data,
                            **TestName.flagset_to_dict(flagset),
                        )


if __name__ == "__main__":
    unittest.main()
