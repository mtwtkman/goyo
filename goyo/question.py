from contextlib import contextmanager
from typing import ClassVar, Optional, Tuple, Set, Callable, Type, Any

from .exception import ClosedQuestionException
from .choices import ChoiceEnum, ILLEGAL_CHOICE
from .answer import Answer, MultipleAnswer, AnswerBase


class QuestionBase:
    body: ClassVar[str]
    case_insensitive: ClassVar[bool] = False
    delimiter: ClassVar[str] = ': '
    answer: AnswerBase

    def __init__(self):
        self.is_closed = False
        self.resume_count = 0

    def done(self) -> 'QuestionBase':
        self.is_closed = True
        return self

    def resume(self) -> 'QuestionBase':
        self.is_closed = False
        self.resume_count += 1
        return self

    @property
    def has_resumed(self) -> bool:
        return self.resume_count > 0

    @contextmanager
    def accept_hook(self, answer: str) -> Any:
        yield

    def acceptable(self, answer: str) -> bool:
        return True

    def accept(self, answer: str) -> 'QuestionBase':
        with self.accept_hook(answer):
            if self.is_closed:
                raise ClosedQuestionException
            result = self._accept(answer) if self.acceptable(answer) else self
        return result

    def _accept(self, answer: str) -> 'QuestionBase':
        raise NotImplementedError

    def clear_answer(self) -> 'QuestionBase':
        self.answer.clear()
        return self

    @property
    def is_continuable(self) -> bool:
        raise NotImplementedError

    def display(self) -> str:
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
    def is_continuable(self) -> bool:
        return not self.is_closed and (self.answer.is_blank or self.answer.unwrap() is ILLEGAL_CHOICE or self.has_resumed)

    def display(self) -> str:
        return f'{self.body}\t{self.choices.display()}{self.delimiter}'


class FreeQuestion(QuestionBase):
    multiple_answers: ClassVar[bool] = True
    answer_duplicatable: ClassVar[bool] = True
    finish_signal: ClassVar[Tuple[str, ...]] = ('q', 'quit')

    # FIXME: When multiple_answers option is absence, these options are ignored.
    min_answer_count: ClassVar[Optional[int]]  = None
    max_answer_count: ClassVar[Optional[int]] = None


    def __init__(self):
        super().__init__()
        answer_type = self._detect_answer_type()
        self.answer = answer_type()
        self.invalid_answer = answer_type()
        self._known_answer_elements: Set[str] = set()
        self._is_received_finish_signal = False

    @classmethod
    def _detect_answer_type(cls) -> Type[AnswerBase]:
        return MultipleAnswer if cls.multiple_answers else Answer

    def validator(self, s: str):
        return True

    def _receive_finish_signal(self) -> 'FreeQuestion':
        self._is_received_finish_signal = True
        return self

    def acceptable(self, answer: str) -> bool:
        s = answer if self.case_insensitive else answer.lower()
        if s in self.finish_signal:
            self._receive_finish_signal()
            return False
        is_valid = self.validator(answer)
        if not is_valid:
            self.invalid_answer.save(answer)
            return False
        already_known = s in self._known_answer_elements
        if not self.case_insensitive and not already_known:
            self._known_answer_elements.add(s)
        return (
            (self.answer_duplicatable and not already_known) or
            self.is_answer_count_satisified or
            is_valid
        )

    @property
    def is_answer_count_satisified(self):
        return (
            (not self.multiple_answers and len(self.answer) == 0) or
            (self.multiple_answers and (self.min_answer_count or -1) <= len(self.answer) <= (self.max_answer_count or float('inf')))
        )

    def _accept(self, answer: str) -> 'FreeQuestion':
        self.answer.save(answer)
        return self

    def display(self):
        return f'{self.body}{self.delimiter}'

    @property
    def is_continuable(self) -> bool:
        return not self._is_received_finish_signal and self.is_answer_count_satisified