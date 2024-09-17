from strats import *

class Strategy(Hard):
    question_limit = 7

    def solve(game):
        people = [Alice, Bob, Charlie, Dan]
        subjects = [Math, Engg, Phys, Phil]
        responses = []
        guesses = []

        for person in people:
            responses.append(game.get_response(person.ask(True)))

        found_match = False
        for i in range(4):
            for j in range(4):
              if i == j:
                continue

              if responses[i] == responses[j]:
                maybe_engg_indexes = [i,j]
                not_engg_indexes = list(filter(lambda x: x not in maybe_engg_indexes, range(4)))

                found_match = True
                break

            if found_match:
              break

        question_5_response = game.get_response(people[not_engg_indexes[0]].ask(False))

        if question_5_response == responses[not_engg_indexes[0]]:
            game.guess[people[not_engg_indexes[0]]] = Phil
            guesses.append((not_engg_indexes[0], Phil))

            maybe = responses[not_engg_indexes[0]]
            yes_or_no = list(filter(lambda x: x != maybe, [Foo, Bar, Baz]))

            math_or_phys_person_index = not_engg_indexes[1]
            other_person_index = not_engg_indexes[0]

        else:
            math_or_phys_person_index = not_engg_indexes[0]
            other_person_index = not_engg_indexes[1]

            yes_or_no = [responses[not_engg_indexes[0]], question_5_response]
            maybe = list(filter(lambda x: x not in yes_or_no, [Foo, Bar, Baz]))[0]

            if maybe == responses[not_engg_indexes[1]]:
                game.guess[people[not_engg_indexes[1]]] = Phil
                guesses.append((not_engg_indexes[1], Phil))
        
        math_or_phys_person = people[math_or_phys_person_index]
        math_or_phys_response = responses[math_or_phys_person_index]

        question_6_response = game.get_response(math_or_phys_person.ask(math_or_phys_person.ask(math_or_phys_person.studies(Math)).equals(math_or_phys_response)))

        if question_6_response == math_or_phys_response:
            game.guess[math_or_phys_person] = Math
            other_subject = Phys
            guesses.append((math_or_phys_person_index, Math))

        else:
            game.guess[math_or_phys_person] = Phys
            other_subject = Math
            guesses.append((math_or_phys_person_index, Phys))

        if len(guesses) == 1:
            game.guess[people[other_person_index]] = other_subject
            guesses.append((other_person_index, other_subject))

        question_7_response = game.get_response(math_or_phys_person.ask(math_or_phys_person.ask(people[maybe_engg_indexes[0]].studies(Engg)).equals(math_or_phys_response)))

        if question_7_response == math_or_phys_response:

            engg_index = maybe_engg_indexes[0]

        else:

            engg_index = maybe_engg_indexes[1]

        game.guess[people[engg_index]] = Engg
        guesses.append((engg_index, Engg))

        missing_index = list(filter(lambda x: x not in map(lambda y: y[0], guesses), range(4)))[0]

        missing_subject = list(filter(lambda x: x not in map(lambda y: y[1], guesses), subjects))[0]

        game.guess[people[missing_index]] = missing_subject
        guesses.append((missing_index, missing_subject))