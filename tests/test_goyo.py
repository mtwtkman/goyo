import enum

import pytest

from goyo import (
   OneChoiceQuestion,
   FreeQuestion,
   ChoiceEnum,
   ClosedQuestionException,
)


def test_optional_question():
    class Q(OneChoiceQuestion):
        body = 'Are you fine?'

        class choices(ChoiceEnum):
            yes = 'y'
            no = 'n'

    q = Q()
    assert str(q.choices) == '[y/n]'
    assert str(q) == f'{q.body}\t{q.choices}: '
    answered_y = q.accept('y')
    assert answered_y.answer == Q.choices.of('y')
    assert answered_y.is_correct is True
    assert answered_y.is_('yes') is True
    assert answered_y.is_('no') is False
    assert answered_y.is_('x') is False
    assert q.accept('n').is_('no') is True
    assert q.accept('x').is_('x') is False
    assert q.accept('x').is_correct is False
    q.accept('y').done()
    assert q.is_closed
    try:
        q.accept('x')
    except ClosedQuestionException:
        pass


def test_free_question():
    class Q(FreeQuestion):
        body = "Please choose languages that you've ever used."
        multiple_answers = True
        case_insensitive = True
        answer_duplicatable = False

    q = Q()
    q.accept('python').accept('rust').accept('scala').accept('Python')
    assert q.answers == ('python', 'rust', 'scala', 'Python')
    assert q.has('python') is True
    assert q.has('ruby') is False
    q.done()
    assert q.is_closed
    try:
        q.accept('javascript')
    except ClosedQuestionException:
        pass
    q.resume()
    assert q.accept('typescript').answers == ('python', 'rust', 'scala', 'Python', 'typescript')