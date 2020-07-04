from contextlib import contextmanager
from typing import Sequence, Optional, Callable, Any

from .question import QuestionBase


class Prompt:
    def __init__(self, questions: Sequence[QuestionBase]):
        self.questions = questions
        self._prologue: Optional[str] = None
        self._epilogue: Optional[str] = None
        self._input_reader: Callable[[Any], str] = input
        self.current_question: QuestionBase = questions[0]

    def input_reader(self, f: Callable[[Any], str]) -> 'Prompt':
        self._input_reader = f
        return self

    def prologue(self, s: str) -> 'Prompt':
        self._prologue = s
        return self

    def epilogue(self, s: str) -> 'Prompt':
        self._epilogue = s
        return self

    @contextmanager
    def _onstage(self):
        if self._prologue:
            print(self.prologue)
        yield
        if self._epilogue:
            print(self.epilogue)
        return

    def ask(self, question: QuestionBase) -> 'Prompt':
        while not question.is_closed:
            answer = self._input_reader(question.display())
            question.accept(answer)
            if not question.is_continuable:
                question.done()
        return self

    def start(self) -> 'Prompt':
        with self._onstage():
            for q in self.questions:
                self.current_question = q
                self.ask(q)
        return self

    def collect(self):
        return {q: q.answer.unwrap() for q in self.questions}