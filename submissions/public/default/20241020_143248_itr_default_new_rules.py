from strats import *

class Strategy(Default):
    question_limit = 3

    def solve(self):
        answers = [Bob,Charlie,Alice]
        fields = (Engg,Phys,Math)
        def ask(other):
            answers.append(answers.pop(1 if self.get_response(Question(answers[2], answers[other].studies(fields[other//2]).iff(Foo)))==Foo else other))

        ask(0)
        ask(0)
        ask(2)

        self._guess = dict(zip(map(str, answers), fields))