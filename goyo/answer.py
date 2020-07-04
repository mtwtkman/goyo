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
    def clear(self):
        ...


class AnswerBase(Generic[T], AnswerABC):
    _value: T

    def is_answered(self) -> bool:
        return self is not None

    def unwrap(self) -> T:
        return self._value

    @property
    def is_blank(self) -> bool:
        raise NotImplementedError


class Answer(AnswerBase):
    def __init__(self):
        self._value = None

    def save(self, value: str) -> 'Answer':
        self._value = value
        return self

    def show(self) -> Optional[str]:
        return self._value

    def __contains__(self, value: str) -> bool:
        return self._value == value

    def clear(self) -> 'Answer':
        self._value = None
        return self

    @property
    def is_blank(self) -> bool:
        return self._value is None

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

    def __contains__(self, value: str) -> bool:
        return value in self._value

    def clear(self) -> 'MultipleAnswer':
        self._value = []
        return self

    @property
    def is_blank(self) -> bool:
        return len(self._value) == 0

    def __len__(self) -> int:
        return len(self._value)