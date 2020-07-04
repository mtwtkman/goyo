Usage
=====

Write your code.

.. code:: python
    from goto import Prompt, OneChoiceQuestion, FreeQuestion, ChoiceEnum

    class Q1(OneChoiceQuestion):
        body = 'Are you fine?'

        class Choices(ChoiceEnum):
            yes = 'y'
            no = 'n'


    class Q2(FreeQuestion):
        body = "Please choose languages that you've ever used."
        multiple_answers = True


    prompt = Prompt((Q1, Q2)).introduce('Hi').run()


Run this script.


.. code:: sh
    $ python prompt.py
    Hi

    Are you fine?   [y/n]: y
    Please choose languages that you've ever used.: elm
        Your answer: python, rust, scala, elm