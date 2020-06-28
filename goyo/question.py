from typing import ClassVar, Optional, Tuple
from contextlib import contextmanager

from .exception import ClosedQuestionException
from .choices import ChoiceEnum


class QuestionBase:
    body: ClassVar[str]
    case_insensitive: ClassVar[bool] = False

    def __init__(self):
        self.is_closed = False

    def done(self) -> 'QuestionBase':
        self.is_closed = True
        return self

    def resume(self) -> 'QuestionBase':
        self.is_closed = False
        return self

    @contextmanager
    def _acceptable(self):
        if self.is_closed:
            raise ClosedQuestionException
        yield

    def accept(self, answer: str) -> 'QuestionBase':
        with self._acceptable():
            return self._accept(answer)

    def _accept(self, answer: str) -> 'QuestionBase':
        raise NotImplementedError


class OneChoiceQuestion(QuestionBase):
    choices: ClassVar[ChoiceEnum]
    delimiter: str = ': '

    class ILLIGAL_CHOICE:
        ...

    def __init__(self):
        super().__init__()
        self._raw_answer: Optional[str] = Optional[None]
        self.answer: Optional['OneChoiceQuestion.Choices'] = None

    def _accept(self, answer: str) -> 'OneChoiceQuestion':
        self._raw_answer = answer
        self.answer = self.choices.of(answer)
        return self

    @property
    def is_correct(self) -> bool:
        return self.answer is not self.choices.ILLEGAL_CHOICE

    def is_(self, value: str) -> bool:
        choice = self.choices.select(value)
        if choice is self.choices.ILLEGAL_CHOICE:
            return False
        return self.answer == choice

    def __repr__(self):
        return f'{self.body}\t{self.choices}{self.delimiter}'


class FreeQuestion(QuestionBase):
    multiple_answers: ClassVar[bool] = False
    answer_duplicatable: ClassVar[bool] = False

    def __init__(self):
        super().__init__()
        self._answers = []

    @property
    def _reached_limit(self) -> bool:
        return not self.multiple_answers and len(self._answers) == 1

    def has(self, value: str) -> bool:
        return value in self._answers

    def _accept(self, value: str) -> 'FreeQuestion':
        v = value if self.case_insensitive else value.lower()
        if (
            not self._reached_limit and
            (not self.answer_duplicatable and not self.has(v))
        ):
            self._answers.append(value)
        return self

    @property
    def answers(self) -> Tuple[str, ...]:
        return tuple(self._answers)

    def __iter__(self):
        for x in self._answers:
            yield x