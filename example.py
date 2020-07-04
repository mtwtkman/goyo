from contextlib import contextmanager

from goyo import OneChoiceQuestion, FreeQuestion, Prompt, ChoiceEnum


class Q1(OneChoiceQuestion):
    body = 'Please chose your favorite animal'

    class choices(ChoiceEnum):
        dog = 'dog'
        cat = 'cat'


class Q2(FreeQuestion):
    body = 'What do you like fruits?'
    multiple_answers = True

    @contextmanager
    def accept_hook(self, answer):
        yield
        print(f'your answer: {self.answer.show()}')


q1 = Q1()
q2 = Q2()
prompt = Prompt((q1, q2))
prompt.start()
print(prompt.collect())