from strats import *


class Strategy(Default):
    # This solution is based on vzsky`s approach, im simply trying to lower complexity score.
    engg_question_limit = 1


    def solve(self):
        ask = lambda x, y, z: self.get_response(x.ask(x.ask(y.studies(z)).equals(Foo))) == Foo

        b, c = (b, Charlie) if ask((a:=Alice), (b:=Bob), Engg) else (Charlie, b)

        if ask(c, b, Engg): a, b = b, a

        self.guess[a], self.guess[b], self.guess[c] = [Engg, Phys, Math] if ask(c, c, Math) else [Engg, Math, Phys]