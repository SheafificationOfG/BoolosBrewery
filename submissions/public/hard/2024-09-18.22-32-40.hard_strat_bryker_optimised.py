from strats import *

class Strategy(Hard):
    question_limit = 6

    def solve(game):
        # First we will ask each person the same question
        # The mathematician, physicist, and philosopher will each give different
        # answers and the engineer will duplicate an answer
        # therefore the two people who give unique answers are not the engineer
        
        words = [Foo, Bar, Baz]
        people = [Alice, Bob, Charlie, Dan]
        question = \
            "((Foo is true) and (Bar is false)) xor " + \
            "((Bar is true) and (Baz is false)) xor " + \
            "((Baz is true) and (Foo is false)) xor " + \
            "(You study Phys)"

        q1 = []
        for p in people:
            answer = game.get_response(p.ask(question))
            if answer in q1:
                duplicate_answer = answer
            q1.append(answer)

            # if there has been a duplicate response after three questions we know 
            # that the fourth response will be the unused word and can thus save a 
            # question, reducing the average number of questions needed

            if len(q1) == 3 and set(words)-set(q1):
                missing_answer = [word for word in words if word not in q1]
                q1 += missing_answer
                break
                

        duplicates = []
        for i in range(4):
            if q1[i] != duplicate_answer:
                non_eng = people[i]
                original_answer = q1[i]
            else:
                duplicates.append(people[i])

        # Next ask one of the non-engineers the opposite of the first question
        # if they answer the same as last time then they are the philosopher
        # and that answer is 'maybe'
        # otherwise the answer they have not said in either question means 'maybe'

        new_answer = game.get_response(non_eng.ask("not (%s)" % question)) # invert the question
        if new_answer == original_answer:
            maybe = new_answer
        else:
            maybe = [Foo, Bar, Baz]
            maybe.remove(new_answer)
            maybe.remove(original_answer)
            maybe = maybe[0]
        yes_no = [Foo, Bar, Baz]
        yes_no.remove(maybe)

        for i in range(4):
            if q1[i] != maybe and q1[i] != duplicate_answer:
                helpful_person = people[i]

        # once we have identified a non-philosopher non-engineer we can ask them which of the two 
        # who answered the same way is the engineer

        q3 = game.get_response(helpful_person.ask(duplicates[0].studies(Engg).xor(yes_no[0].equals(True))))

        remaining_people = [Alice, Bob, Charlie, Dan]
        if q3 == yes_no[0]:
            eng = duplicates[1]
        else:
            eng = duplicates[0]
        game.guess[eng] = Engg
        remaining_people.remove(eng)

        # lastly we need to use the first question to deduce which of 
        # the remaining two is the mathematician
        if maybe == Foo:
            math_answer = Bar
        if maybe == Bar:
            math_answer = Baz
        if maybe == Baz:
            math_answer = Foo

        for i in range(4):
            if q1[i] == maybe and people[i] != eng:
                philo = people[i]
            if q1[i] == math_answer and people[i] != eng:
                math = people[i]
        game.guess[philo] = Phil
        remaining_people.remove(philo)
        game.guess[math] = Math
        remaining_people.remove(math)

        game.guess[remaining_people[0]] = Phys