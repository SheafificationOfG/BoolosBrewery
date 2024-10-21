from strats import *


class Strategy(Easy):
    engg_question_limit = 0

    def solve(self):
        # To Alice: Does the mathematician use the word "Foo" as "No"?
        response = self.get_response(Alice.ask(Foo.equals(Mathematician.ask(False))))
        if response == Bar:
            self.guess[Alice] = Math
            self.guess[Bob] = Phys
        else:
            self.guess[Alice] = Phys
            self.guess[Bob] = Math

