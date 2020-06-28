from typing import ClassVar, Optional, Tuple, Set

from .exception import ClosedQuestionException
from .choices import ChoiceEnum, ILLEGAL_CHOICE
from .answer import Answer, MultipleAnswer, AnswerBase


class QuestionBase:
    body: ClassVar[str]
    case_insensitive: ClassVar[bool] = False
    answer: AnswerBase
    delimiter: str = ': '

    def __init__(self):
        self.is_closed = False

    def done(self) -> 'QuestionBase':
        self.is_closed = True
        return self

    def resume(self) -> 'QuestionBase':
        self.is_closed = False
        return self

    def acceptable(self, answer: str) -> bool:
        return True

    def accept(self, answer: str) -> 'QuestionBase':
        if self.is_closed:
            raise ClosedQuestionException
        if self.acceptable(answer):
            return self._accept(answer)
        return self

    def _accept(self, answer: str) -> 'QuestionBase':
        raise NotImplementedError


class OneChoiceQuestion(QuestionBase):
    choices: ClassVar[ChoiceEnum]

    def __init__(self):
        super().__init__()
        self.answer = Answer()

    def _accept(self, answer: str) -> 'OneChoiceQuestion':
        self.answer.save(self.choices.of(answer))  # type: ignore
        return self

    @property
    def is_correct(self) -> bool:
        return self.answer.unwrap() is not ILLEGAL_CHOICE

    def __repr__(self) -> str:
        return f'{self.body}\t{self.choices}{self.delimiter}'


class FreeQuestion(QuestionBase):
    multiple_answers: ClassVar[bool] = True
    answer_duplicatable: ClassVar[bool] = True

    def __init__(self):
        super().__init__()
        self.answer = MultipleAnswer() if self.multiple_answers else Answer()
        self._known_answer_elements: Set[str] = set()

    def acceptable(self, answer: str) -> bool:
        s = answer if self.case_insensitive else answer.lower()
        already_known = s in self._known_answer_elements
        if not self.case_insensitive and not already_known:
            self._known_answer_elements.add(s)
        return (
            (self.answer_duplicatable and not already_known) or
            (not self.multiple_answers and len(self.answer) == 0) or
            True
        )

    def _accept(self, answer: str) -> 'FreeQuestion':
        self.answer.save(answer)
        return self

    def __repr__(self):
        return f'{self.body}{self.delimiter}'