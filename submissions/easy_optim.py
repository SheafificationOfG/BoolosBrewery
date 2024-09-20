from strats import *

class Strategy(Easy):
    # This is based on submission 20240918_001159, im just interested in lowering complexity score :)
    # I know the code is not very readable.
    question_limit = 1

    def solve(self):
        self.guess[Alice], self.guess[Bob] = [Phys, Math] if self.get_response(Alice.ask(Foo.equals(Mathematician.ask(False)))) != Bar else [Math, Phys]
