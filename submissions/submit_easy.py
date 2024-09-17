from strats import Alice, Bob, Math, Phys, Foo
from strats.strategy import Easy

class Strategy(Easy):
    question_limit = 1


    def solve(game):

        query = Alice.ask(Alice.studies(Math).iff(Foo))

        res = game.get_response(query)

        if res == Foo:
            game.guess[Alice] = Math
            game.guess[Bob] = Phys
        else:
            game.guess[Alice] = Phys
            game.guess[Bob] = Math

        