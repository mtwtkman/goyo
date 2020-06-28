import pytest

from goyo import (
   OneChoiceQuestion,
   ChoiceEnum,
   ClosedQuestionException,
   FreeQuestion,
)

import enum


def test_optional_question():
    class Q(OneChoiceQuestion):
        body = 'Are you fine?'

        class choices(ChoiceEnum):
            yes = 'y'
            no = 'n'

    q = Q()
    assert str(q.choices) == '[y/n]'
    assert str(q) == f'{q.body}\t{q.choices}: '
    a_y = q.accept('y')
    assert a_y.answer.show() is Q.choices.yes
    assert a_y.is_correct
    assert not q.accept('x').is_correct
    q.accept('y').done()
    assert q.is_closed
    try:
        q.accept('x')
    except ClosedQuestionException:
        pass


def test_free_question():
    class Q1(FreeQuestion):
        body = "Please choose languages that you've ever used."
        multiple_answers = True
        case_insensitive = True
        answer_duplicatable = False

    q1 = Q1()
    q1.accept('python').accept('rust').accept('scala').accept('Python')
    assert q1.answer.unwrap() == ['python', 'rust', 'scala', 'Python']
    assert q1.answer.show() == ('python', 'rust', 'scala', 'Python')
    assert q1.answer.has('python')
    assert not q1.answer.has('ruby')
    q1.done()
    assert q1.is_closed
    try:
        q1.accept('javascript')
    except ClosedQuestionException:
        pass
    q1.resume()
    a = q1.accept('typescript').answer
    assert a.unwrap() == ['python', 'rust', 'scala', 'Python', 'typescript']
    assert a.show() == ('python', 'rust', 'scala', 'Python', 'typescript')

    class Q2(FreeQuestion):
        body = "What are your favorite foods?"
        multiple_answers = False

    q2 = Q2()
    q2.accept('egg')
    assert q2.answer.show() == 'egg'
    assert q2.accept('ham').answer.show() == 'ham'