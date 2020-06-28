from abc import ABC, abstractmethod
from typing import Optional, Tuple, TypeVar, Generic


T = TypeVar('T')


class AnswerABC:
    @abstractmethod
    def save(self, value: str):
        ...

    @abstractmethod
    def show(self):
        ...

    @abstractmethod
    def has(self, value: str):
        ...


class AnswerBase(Generic[T], AnswerABC):
    _value: T

    def is_answered(self) -> bool:
        return self is not None

    def unwrap(self) -> T:
        return self._value


class Answer(AnswerBase):
    def __init__(self):
        self._value = None

    def save(self, value: str) -> 'Answer':
        self._value = value
        return self

    def show(self) -> Optional[str]:
        return self._value

    def has(self, value: str) -> bool:
        return self._value == value

    def __len__(self) -> int:
        return 0 if self._value is None else 1


class MultipleAnswer(AnswerBase):
    def __init__(self):
        self._value = []

    def save(self, value: str) -> 'MultipleAnswer':
        self._value.append(value)
        return self

    def show(self) -> Optional[Tuple[str, ...]]:
        return tuple(self._value)

    def has(self, value: str) -> bool:
        return value in self._value

    def __len__(self) -> int:
        return len(self._value)