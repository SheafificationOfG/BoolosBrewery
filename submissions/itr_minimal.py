from strats import *

class Strategy(Default):
    engg_question_limit = 1

    def solve(self):
        answers = [Bob,Charlie,Alice]
        fields = (Engg,Phys,Math)

        for i in [0,0,2]:
            answers.append(answers.pop(1 if self.get_response(Question(answers[2], answers[i].studies(fields[i // 2]).iff(Foo))) == Foo else i))

        self._guess = dict(zip(map(str, answers), fields))