from strats import *

class Strategy(Default):
    engg_question_limit = 1

    def solve(self):
        answers = ["Bob","Charlie","Alice"]
        fields = (Engg,Phys,Math)
        def ask(other):
            answers.append(answers.pop(1 if self.get_response(Question(answers[2], f'{answers[other]} studies {fields[other//2]} iff Foo'))==Foo else other))

        ask(0)
        ask(0)
        ask(2)

        self._guess = dict(zip(answers, fields))