from itertools import permutations
from strats import *
from functools import reduce

AND = lambda a, b: a.and_(b)
XOR = lambda a, b: a.xor(b)
PEOPLE = (Alice, Bob, Charlie, Dan)
STUDIES = (Math, Phys, Engg, Phil)

def lessthan(who, who2):
    return reduce(
        lambda acc, sub: acc.and_(who2.studies(sub).invert()).or_(who.studies(sub)),
        [Phys, Math],
        who.studies(Engg) # who2.studies(Engg).implies(who.studies(Engg))
    )

def phil(word):
    return Philosopher.ask(True).equals(word)
def phys(word):
    return Mathematician.ask(False).equals(word)

def force(who, word):
    return phil(word).and_(who.studies(Engg))

def Truthy():
    return phys(baz_).xor(Mathematician.ask(True).equals(foo_).and_(phys(bar_)))

def Sixes(who):
    return who.studies(Math)

def EXCEPT(who):
    people = list(PEOPLE)
    people.remove(who)
    return people

def LESSTHAN(i, j):
    def f(who):
        people = EXCEPT(who)
        return lessthan(people[i], people[j])
    return f

Threes = LESSTHAN(0, 2)
Twos = LESSTHAN(0, 1)
Ones = LESSTHAN(1, 2)

def Bottom(who):
    first, second, last = EXCEPT(who)
    return lessthan(last, second).and_(lessthan(second, first))

def Top(who):
    first, second, last = EXCEPT(who)
    return lessthan(first, second).and_(lessthan(second, last))

def Wides(_):
    return ~phil(baz_)

def Shorts(_):
    return phil(foo_)

def All(_):
    return True

def Tl(who):
    return Sixes(who).and_(Shorts(who))

def Tr(who):
    return Sixes(who).implies(Wides(who))

def T3(who):
    return Sixes(who).and_(Threes(who))

def HELPER(offset):
    def f(who):
        people = EXCEPT(who)
        people = people[offset:]+people[:offset]
        return force(people[0], Foo).or_(force(people[1], Bar)).or_(force(people[2], Baz))
    return f

Helper = HELPER(0)
Helper2 = HELPER(2)
Helper3 = HELPER(1)


def get_qa(who, funcs=[]):
    values = [Truthy()] + [f(who) for f in funcs]
    q = reduce(XOR, values)
    return who.ask(q)

solution = {
    (): (Alice,(Sixes,Wides,Shorts,Helper)),
    (Foo,): (Charlie,(Sixes,Wides,Shorts,Helper3)),
    (Foo,Foo): (Dan,(Sixes,Threes,All)),
    (Foo,Foo,Foo): (Charlie,()),
    (Foo,Foo,Bar): (Dan,(Sixes,)),
        (Foo,Foo,Bar,Bar): (Charlie,(Twos,Sixes)),
            (Foo,Foo,Bar,Bar,Foo): (Charlie,()),
            (Foo,Foo,Bar,Bar,Baz): (Charlie,()),
        (Foo,Foo,Bar,Baz): (Bob,()),
            (Foo,Bar,Baz,Foo,Foo): (Bob,()),
            (Foo,Bar,Baz,Foo,Baz): (Bob,()),
        (Foo,Foo,Baz,Bar): (Charlie,(All,)),
    (Foo,Foo,Baz): (Bob,()),

    (Foo,Bar): (Alice,(Sixes,)),
    (Foo,Bar,Foo): (Dan,(Ones,Sixes)),
        (Foo,Bar,Foo,Foo): (Bob,()),
        (Foo,Bar,Foo,Bar): (Bob,()),
        (Foo,Bar,Foo,Baz): (Charlie,()),
            (Foo,Bar,Baz,Baz,Foo): (Alice,()),
    (Foo,Bar,Bar): (Charlie,(Sixes,All)),
        (Foo,Bar,Bar,Foo): (Charlie,()),
        (Foo,Bar,Bar,Bar): (Bob,()),
    (Foo,Bar,Baz): (Alice,(Sixes,Threes)),
        (Foo,Bar,Baz,Foo): (Bob,(Sixes,Threes)),
        (Foo,Bar,Baz,Bar): (Bob,()),
        (Foo,Bar,Baz,Baz): (Dan,(Sixes,Twos)),
            (Foo,Bar,Baz,Baz,Baz): (Bob,()),

    (Foo,Baz): (Bob,(Sixes,Threes,Ones,Wides,All)),
    (Foo,Baz,Foo): (Dan,()),
        (Foo,Baz,Foo,Bar): (Charlie,(All,)),
    (Foo,Baz,Bar): (Bob,(Sixes,Wides,All)),
        (Foo,Baz,Bar,Foo): (Bob,()),
        (Foo,Baz,Bar,Bar): (Alice,()),
        (Foo,Baz,Bar,Baz): (Bob,()),
    (Foo,Baz,Baz): (Dan,()),
        (Foo,Baz,Baz,Foo): (Bob,()),

    # I couldn't find a generic way to transform my questions for this,
    # so I ended up just finding similar enough patterns instead of generalizing it for all 3
    (Bar,): (Dan, (Sixes,Wides,Helper3,All,Threes,Ones,Bottom)),
    (Bar,Foo): (Charlie,(Sixes,Threes,Top)),
    (Bar,Foo,Foo): (Bob,(Ones,)),
        (Bar,Foo,Foo,Foo): (Bob,()),
        (Bar,Foo,Foo,Bar): (Dan,()),
        (Bar,Foo,Foo,Baz): (Bob,()),
    (Bar,Foo,Bar): (Bob,(Sixes,Twos,Shorts,All)),
        (Bar,Foo,Bar,Foo): (Bob,()),
        (Bar,Foo,Bar,Bar): (Bob,()),
        (Bar,Foo,Bar,Baz): (Bob,()),
    (Bar,Foo,Baz): (Dan,(Sixes,All)),
        (Bar,Foo,Baz,Foo): (Charlie,()),
        (Bar,Foo,Baz,Bar): (Dan,()),
        (Bar,Foo,Baz,Baz): (Dan,()),

    (Bar,Bar): (Bob,(Threes,Sixes,All)),
    (Bar,Bar,Foo): (Charlie,()),
        (Bar,Bar,Foo,Baz): (Dan,(All,)),
    (Bar,Bar,Bar): (Bob,()),
    (Bar,Bar,Baz): (Bob,(Sixes,)),
        (Bar,Bar,Baz,Foo): (Bob,()),
        (Bar,Bar,Baz,Baz): (Dan,(Sixes,Threes)),
            (Bar,Bar,Baz,Baz,Foo): (Dan,()),
            (Bar,Bar,Baz,Baz,Bar): (Dan,()),

    (Bar,Baz): (Alice,(Sixes,)),
    (Bar,Baz,Foo): (Alice,(Sixes,Twos)),
        (Bar,Baz,Foo,Foo): (Charlie,(Sixes,Twos)),
            (Bar,Baz,Foo,Foo,Foo): (Bob,()),
            (Bar,Baz,Foo,Foo,Bar): (Charlie,()),
        (Bar,Baz,Foo,Bar): (Bob,(Sixes,Twos)),
        (Bar,Baz,Foo,Baz): (Bob,()),
    (Bar,Baz,Bar): (Charlie,(Sixes,Threes,Bottom)),
        (Bar,Baz,Bar,Foo): (Bob,()),
        (Bar,Baz,Bar,Bar): (Bob,()),
            (Bar,Baz,Foo,Bar,Foo): (Bob,()),
            (Bar,Baz,Foo,Bar,Bar): (Bob,()),
        (Bar,Baz,Bar,Baz): (Dan,()),
    (Bar,Baz,Baz): (Dan,(Sixes,Twos)),
        (Bar,Baz,Baz,Bar): (Dan,()),
        (Bar,Baz,Baz,Baz): (Bob,()),


    (Baz,): (Bob, (Sixes,Wides,Helper,Threes,Twos,Top)),
    (Baz,Foo): (Alice,(Sixes,)),
    (Baz,Foo,Foo): (Bob,(Sixes,All)),
        (Baz,Foo,Foo,Foo): (Charlie,()),
        (Baz,Foo,Foo,Baz): (Bob,()),
    (Baz,Foo,Bar): (Alice,(Sixes,Ones)),
        (Baz,Foo,Bar,Foo): (Charlie,()),
        (Baz,Foo,Bar,Bar): (Dan,(Sixes,Threes)),
            (Baz,Foo,Bar,Bar,Bar): (Charlie,()),
            (Baz,Foo,Bar,Bar,Baz): (Dan,()),
        (Baz,Foo,Bar,Baz): (Charlie,(Sixes,Threes)),
            (Baz,Foo,Bar,Baz,Bar): (Charlie,()),
    (Baz,Foo,Baz): (Dan,(Sixes,Ones,All)),
        (Baz,Foo,Baz,Foo): (Charlie,()),
        (Baz,Foo,Baz,Bar): (Bob,()),
            (Baz,Foo,Bar,Baz,Baz): (Charlie,()),
        (Baz,Foo,Baz,Baz): (Charlie,()),

    (Baz,Bar): (Dan,(Sixes,Ones,All,Threes,Shorts)),
    (Baz,Bar,Foo): (Bob,(Sixes,Ones)),
        (Baz,Bar,Foo,Foo): (Charlie,()),
        (Baz,Bar,Foo,Bar): (Dan,()),
        (Baz,Bar,Foo,Baz): (Bob,()),
    (Baz,Bar,Bar): (Charlie,(Ones,)),
        (Baz,Bar,Bar,Foo): (Charlie,()),
        (Baz,Bar,Bar,Bar): (Charlie,()),
        (Baz,Bar,Bar,Baz): (Bob,()),
    (Baz,Bar,Baz): (Charlie,(Sixes,Threes,All)),
        (Baz,Bar,Baz,Foo): (Bob,()),
        (Baz,Bar,Baz,Bar): (Bob,()),
        (Baz,Bar,Baz,Baz): (Charlie,()),

    (Baz,Baz): (Charlie,(Sixes,Twos,All)),
    (Baz,Baz,Foo): (Charlie,(Sixes,)),
        (Baz,Baz,Foo,Foo): (Bob,(Sixes,Threes)),
            (Baz,Baz,Foo,Foo,Bar): (Dan,()),
            (Baz,Baz,Foo,Foo,Baz): (Bob,()),
        (Baz,Baz,Foo,Bar): (Charlie,()),
    (Baz,Baz,Bar): (Charlie,(Sixes,All)),
        (Baz,Baz,Bar,Foo): (Charlie,()),
        (Baz,Baz,Bar,Bar): (Dan,()),
    (Baz,Baz,Baz): (Charlie,()),

    (Foo, Foo, Foo, Foo): 16, (Foo, Foo, Foo, Bar): 22, (Foo, Foo, Foo, Baz): 22, (Foo, Foo, Bar, Bar, Foo, Foo): 12, (Foo, Foo, Bar, Bar, Foo, Baz): 2, (Foo, Foo, Bar, Bar, Baz, Foo): 14, (Foo, Foo, Bar, Bar, Baz, Baz): 8, (Foo, Foo, Bar, Baz, Bar): 11, (Foo, Foo, Bar, Baz, Baz): 21, (Foo, Foo, Baz, Foo): 8, (Foo, Foo, Baz, Bar, Foo): 10, (Foo, Foo, Baz, Bar, Bar): 14, (Foo, Foo, Baz, Baz): 20, (Foo, Bar, Foo, Foo, Foo): 10, (Foo, Bar, Foo, Foo, Baz): 20, (Foo, Bar, Foo, Bar, Bar): 11, (Foo, Bar, Foo, Bar, Baz): 21, (Foo, Bar, Foo, Baz, Bar): 17, (Foo, Bar, Foo, Baz, Baz): 23, (Foo, Bar, Bar, Foo, Foo): 13, (Foo, Bar, Bar, Foo, Bar): 3, (Foo, Bar, Bar, Bar, Foo): 10, (Foo, Bar, Bar, Bar, Baz): 20, (Foo, Bar, Baz, Foo, Foo, Foo): 7, (Foo, Bar, Baz, Foo, Foo, Baz): 1, (Foo, Bar, Baz, Foo, Baz, Foo): 10, (Foo, Bar, Baz, Foo, Baz, Baz): 20, (Foo, Bar, Baz, Bar, Foo): 10, (Foo, Bar, Baz, Bar, Baz): 20, (Foo, Bar, Baz, Baz, Foo, Foo): 4, (Foo, Bar, Baz, Baz, Foo, Baz): 18, (Foo, Bar, Baz, Baz, Baz, Foo): 10, (Foo, Bar, Baz, Baz, Baz, Baz): 20, (Foo, Baz, Foo, Foo): 20, (Foo, Baz, Foo, Bar, Bar): 22, (Foo, Baz, Foo, Bar, Baz): 10, (Foo, Baz, Foo, Baz): 16, (Foo, Baz, Bar, Foo, Foo): 7, (Foo, Baz, Bar, Foo, Bar): 1, (Foo, Baz, Bar, Bar, Foo): 3, (Foo, Baz, Bar, Bar, Baz): 13, (Foo, Baz, Bar, Baz, Bar): 9, (Foo, Baz, Bar, Baz, Baz): 15, (Foo, Baz, Baz, Foo, Bar): 8, (Foo, Baz, Baz, Foo, Baz): 14, (Foo, Baz, Baz, Bar): 21, (Foo, Baz, Baz, Baz): 11, (Bar, Foo, Foo, Foo, Foo): 21, (Bar, Foo, Foo, Foo, Baz): 9, (Bar, Foo, Foo, Bar, Foo): 16, (Bar, Foo, Foo, Bar, Baz): 22, (Bar, Foo, Foo, Baz, Foo): 15, (Bar, Foo, Foo, Baz, Baz): 11, (Bar, Foo, Bar, Foo, Foo): 21, (Bar, Foo, Bar, Foo, Baz): 11, (Bar, Foo, Bar, Bar, Bar): 8, (Bar, Foo, Bar, Bar, Baz): 14, (Bar, Foo, Bar, Baz, Foo): 20, (Bar, Foo, Bar, Baz, Baz): 10, (Bar, Foo, Baz, Foo, Bar): 12, (Bar, Foo, Baz, Foo, Baz): 2, (Bar, Foo, Baz, Bar, Foo): 4, (Bar, Foo, Baz, Bar, Bar): 18, (Bar, Foo, Baz, Baz, Foo): 11, (Bar, Foo, Baz, Baz, Baz): 21, (Bar, Bar, Foo, Foo): 8, (Bar, Bar, Foo, Bar): 16, (Bar, Bar, Foo, Baz, Bar): 14, (Bar, Bar, Foo, Baz, Baz): 22, (Bar, Bar, Bar, Foo): 20, (Bar, Bar, Bar, Bar): 10, (Bar, Bar, Bar, Baz): 20, (Bar, Bar, Baz, Foo, Foo): 15, (Bar, Bar, Baz, Foo, Baz): 9, (Bar, Bar, Baz, Baz, Foo, Foo): 16, (Bar, Bar, Baz, Baz, Foo, Bar): 22, (Bar, Bar, Baz, Baz, Bar, Foo): 5, (Bar, Bar, Baz, Baz, Bar, Bar): 19, (Bar, Baz, Foo, Foo, Foo, Foo): 14, (Bar, Baz, Foo, Foo, Foo, Bar): 8, (Bar, Baz, Foo, Foo, Bar, Foo): 2, (Bar, Baz, Foo, Foo, Bar, Bar): 12, (Bar, Baz, Foo, Bar, Foo, Foo): 14, (Bar, Baz, Foo, Bar, Foo, Bar): 8, (Bar, Baz, Foo, Bar, Bar, Foo): 0, (Bar, Baz, Foo, Bar, Bar, Bar): 6, (Bar, Baz, Foo, Baz, Foo): 14, (Bar, Baz, Foo, Baz, Bar): 8, (Bar, Baz, Bar, Foo, Foo): 15, (Bar, Baz, Bar, Foo, Baz): 9, (Bar, Baz, Bar, Bar, Foo): 14, (Bar, Baz, Bar, Bar, Bar): 8, (Bar, Baz, Bar, Baz, Foo): 17, (Bar, Baz, Bar, Baz, Baz): 23, (Bar, Baz, Baz, Bar, Bar): 18, (Bar, Baz, Baz, Bar, Baz): 4, (Bar, Baz, Baz, Baz, Foo): 14, (Bar, Baz, Baz, Baz, Bar): 8, (Baz, Foo, Foo, Foo, Bar): 22, (Baz, Foo, Foo, Foo, Baz): 16, (Baz, Foo, Foo, Baz, Foo): 0, (Baz, Foo, Foo, Baz, Baz): 6, (Baz, Foo, Bar, Foo, Bar): 22, (Baz, Foo, Bar, Foo, Baz): 16, (Baz, Foo, Bar, Bar, Bar, Bar): 22, (Baz, Foo, Bar, Bar, Bar, Baz): 16, (Baz, Foo, Bar, Bar, Baz, Bar): 5, (Baz, Foo, Bar, Bar, Baz, Baz): 19, (Baz, Foo, Bar, Baz, Bar, Bar): 22, (Baz, Foo, Bar, Baz, Bar, Baz): 16, (Baz, Foo, Bar, Baz, Baz, Bar): 3, (Baz, Foo, Bar, Baz, Baz, Baz): 13, (Baz, Foo, Baz, Foo, Foo): 17, (Baz, Foo, Baz, Foo, Bar): 23, (Baz, Foo, Baz, Bar, Foo): 11, (Baz, Foo, Baz, Bar, Bar): 21, (Baz, Foo, Baz, Baz, Bar): 22, (Baz, Foo, Baz, Baz, Baz): 16, (Baz, Bar, Foo, Foo, Foo): 15, (Baz, Bar, Foo, Foo, Bar): 9, (Baz, Bar, Foo, Bar, Foo): 5, (Baz, Bar, Foo, Bar, Baz): 19, (Baz, Bar, Foo, Baz, Bar): 0, (Baz, Bar, Foo, Baz, Baz): 6, (Baz, Bar, Bar, Foo, Foo): 17, (Baz, Bar, Bar, Foo, Bar): 9, (Baz, Bar, Bar, Bar, Foo): 15, (Baz, Bar, Bar, Bar, Bar): 23, (Baz, Bar, Bar, Baz, Foo): 10, (Baz, Bar, Bar, Baz, Bar): 20, (Baz, Bar, Baz, Foo, Foo): 9, (Baz, Bar, Baz, Foo, Bar): 15, (Baz, Bar, Baz, Bar, Foo): 8, (Baz, Bar, Baz, Bar, Bar): 14, (Baz, Bar, Baz, Baz, Foo): 22, (Baz, Bar, Baz, Baz, Baz): 16, (Baz, Baz, Foo, Foo, Bar, Bar): 10, (Baz, Baz, Foo, Foo, Bar, Baz): 20, (Baz, Baz, Foo, Foo, Baz, Bar): 1, (Baz, Baz, Foo, Foo, Baz, Baz): 7, (Baz, Baz, Foo, Bar, Foo): 17, (Baz, Baz, Foo, Bar, Bar): 23, (Baz, Baz, Bar, Foo, Foo): 16, (Baz, Baz, Bar, Foo, Bar): 22, (Baz, Baz, Bar, Bar, Foo): 10, (Baz, Baz, Bar, Bar, Baz): 20, (Baz, Baz, Baz, Foo): 8, (Baz, Baz, Baz, Bar): 8, (Baz, Baz, Baz, Baz): 14
}


PEOPLE_PERM = list(permutations(tuple(PEOPLE)))
STUDIES_PERM = list(permutations(tuple(STUDIES)))
class Strategy(Hard):
    question_limit = 6

    def solve(self):
        def recurse(answers):
            global foo_, bar_, baz_
            if len(answers) == 0 or answers[0] == Foo:
                foo_, bar_, baz_ = Foo, Bar, Baz
            elif answers[0] == Bar:
                foo_, bar_, baz_ = Bar, Baz, Foo
            else:
                foo_, bar_, baz_ = Baz, Foo, Bar

            if answers not in solution:
                for p in PEOPLE:
                    self.guess[p] = Math
                return

            v = solution[answers]
            try:
                next = answers+(self.get_response(get_qa(*v)),)
            except Exception as e:
                for p, s in zip(PEOPLE_PERM[v], STUDIES):
                    self.guess[p] = s
                return
            recurse(next)
        recurse(())