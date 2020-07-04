import pytest

from goyo import (
   OneChoiceQuestion,
   ChoiceEnum,
   ClosedQuestionException,
   FreeQuestion,
)
from goyo.choices import ILLEGAL_CHOICE

import enum


def test_optional_question():
    class Q(OneChoiceQuestion):
        body = 'Are you fine?'

        class choices(ChoiceEnum):
            yes = 'y'
            no = 'n'

    q = Q()
    assert q.choices.display() == '[y/n]'
    assert q.display() == f'{q.body}\t{q.choices.display()}: '
    valid_answer = q.accept('y').answer
    assert valid_answer.unwrap() == valid_answer.show() == Q.choices.yes
    assert not q.is_continuable
    q.done()
    assert q.is_closed
    assert q.resume().is_closed is False
    assert q.is_continuable
    invalid_answer = q.accept('x').answer
    assert invalid_answer.unwrap() is ILLEGAL_CHOICE
    assert q.is_continuable
    q.done()
    assert not q.is_continuable
    q.clear_answer()
    assert q.answer.is_blank
    assert not q.is_continuable
    try:
        q.accept('n')
    except ClosedQuestionException:
        pass


def test_free_question():
    class Q1(FreeQuestion):
        body = "Please choose languages that you've ever used."
        multiple_answers = True
        case_insensitive = True
        answer_duplicatable = False

        def validator(self, s: str) -> bool:
            return not s.startswith('X')


    q1 = Q1()
    q1.accept('python').accept('rust').accept('scala').accept('Python')
    assert q1.answer.unwrap() == ['python', 'rust', 'scala', 'Python']
    assert q1.answer.show() == ('python', 'rust', 'scala', 'Python')
    assert 'python' in q1.answer
    assert 'ruby' not in  q1.answer
    q1.accept('Xxxx')
    assert 'Xxxx' not in q1.answer
    assert 'Xxxx' in q1.invalid_answer
    q1.accept(Q1.finish_signal[0])
    assert not q1.is_continuable
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


    class Q3(FreeQuestion):
        body = 'FOOOO!!!'
        multiple_answers = True
        min_answer_count = 1
        max_answer_count = 4

    q3 = Q3()
    assert not q3.is_answer_count_satisified
    for i in range(Q3.max_answer_count):
        q3.accept(str(i))
        assert q3.is_answer_count_satisified
    q3.accept('x')
    assert not q3.is_answer_count_satisified