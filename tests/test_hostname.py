import unittest
from typing import ClassVar, Union, Type, Tuple, Set, NamedTuple, Generator
from itertools import combinations

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


known_flags: set[str] = {"allow_idna", "allow_underscore", "allow_empty"}


def flagset_to_dict(flags: set[str]) -> dict[str, bool]:
    return {f: f in flags for f in known_flags}


# I haven't learned enough about generics to make this generic Collectable while
# yielding the same type as the argument
def powerset(s: set[str]) -> Generator[set[str], None, None]:
    # explicitly start at 0 to not forget that the empty set is in the powerset
    for r in range(0, len(s) + 1):
        for result in combinations(s, r):
            yield set(result)


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

    def test_default(self) -> None:
        # default flags are {"allow_idna"}

        flagset = {"allow_idna"}
        other_vectors = [v.to_vector(flagset) for v in self.variable_vectors]
        for data, expected, desc, _ in self.common_vectors + other_vectors:
            with self.subTest(msg=desc):
                result = hn.is_hostname(data)
                self.assertEqual(result, expected)

    def test_flag_combinations(self) -> None:
        for flagset in powerset(known_flags):
            other_vectors = [
                v.to_vector(flagset) for v in self.variable_vectors
            ]
            vectors: list[TestVector] = self.common_vectors + other_vectors
            for data, expected, desc, _ in vectors:
                with self.subTest(msg=f"{desc} {flagset}"):
                    result = hn.is_hostname(data, **flagset_to_dict(flagset))
                    self.assertEqual(result, expected)

    def test_exceptions(self) -> None:
        # Should promgrammatically construct this
        for flagset in powerset(known_flags):
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
                            hn.from_text,
                            data,
                            **flagset_to_dict(flagset),
                        )

    def test_type(self) -> None:
        self.assertRaises(exc.NotAStringError, hn.from_text, 1)


if __name__ == "__main__":
    unittest.main()
