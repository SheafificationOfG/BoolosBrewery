from strats import *


class Strategy(Hard):
    question_limit = 6

    def solve(self):
        # This submission is based on Rrst1 + bryker`s solution. I`m just trying to reduce complexity score :).
        # Readability suffers due to optimization of complexity score.
        words = {Foo, Bar, Baz}
        wm = {Foo: Bar, Bar: Baz, Baz: Foo}

        people = [Alice, Bob, Charlie, Dan]

        question = "((Foo is true) and (Bar is false)) xor ((Bar is true) and (Baz is false)) xor ((Baz is true) and (Foo is false)) xor (You study Phys)"

        q1l = []
        for p in people:
            if (answer := self.get_response(p.ask(question))) in q1l:
                duplicate_answer = answer
            q1l.append(answer)

            if len(q1l) == 3 and words - (q1 := set(q1l)):
                q1l += words.difference(q1)
                break

        duplicates = []
        for val, person in zip(q1l, people):
            if val != duplicate_answer:
                try:
                    if maybe:
                        pass
                except:
                    target = next(iter(words.difference({(maybe := new_answer if (new_answer := self.get_response(person.ask(f"not {question}"))) == val else next(iter(words.difference({new_answer, val}))))})))
            else:
                duplicates.append(person)

        for val, person in zip(q1l, people):
            if val != maybe and val != duplicate_answer:
                self.guess[(eng := duplicates[1] if self.get_response(person.ask(duplicates[0].studies(Engg).xor(target.equals(True)))) == target else duplicates[0])] = Engg
                break

        for val, person in zip(q1l, people):
            if person != eng:
                if val == maybe:
                    self.guess[person] = Phil
                elif val == wm[maybe]:
                    self.guess[person] = Math
                else:
                    self.guess[person] = Phys
