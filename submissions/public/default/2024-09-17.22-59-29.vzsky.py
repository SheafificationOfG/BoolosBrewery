from strats import *

class Strategy(Default):
    question_limit = 3

    # Ask will always return truthfully if the person is either a mathematician or a physicist.
    def ask (self, Person, stmt): 
        return self.get_response(Person.ask(Person.ask(stmt).equals(Foo))) == Foo

    def solve(self):
        A, B, C = Alice, Bob, Charlie
        
        # if A says B is not engineer, then either A or C is engineer.
        # if A says B is engineer, then either A or B is engineer. 
        # Swapping B and C in first case means that A or B is engineer, hence C is never.
        if not self.ask(A, B.studies(Engg)): B, C = C, B
        # ask will now be truthful since C is not engineer
        if self.ask(C, B.studies(Engg)): A, B = B, A 
        # if b is engineer, then let A be by swapping, thus A will always be engineer

        c_is_math = self.ask(C, C.studies(Math)) 
        self.guess[A] = Engg
        self.guess[B] = Phys if c_is_math else Math
        self.guess[C] = Math if c_is_math else Phys
