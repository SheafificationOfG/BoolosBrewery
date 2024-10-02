from itertools import permutations
from strats import *
from functools import reduce

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
Helper3 = HELPER(1)

def get_qa(who, funcs=[]):
    values = [Truthy()] + [f(who) for f in funcs]
    q = reduce(XOR, values)
    return who.ask(q)

SIXES = Sixes,
SIXES_ALL = Sixes,All
SIXES_WIDES = Sixes,Wides
SIXES_ONES = Sixes,Ones
SIXES_TWOS = Sixes,Twos
SIXES_THREES = Sixes,Threes

BOB_ZERO = Bob,()
CHARLIE_ZERO = Charlie,()
DAN_ZERO = Dan,()

ALICE_SIXES = Alice,SIXES
DAN_SIXES_TWOS = Dan,SIXES_TWOS

solution = {
    (): (Alice,(*SIXES_WIDES,Shorts,Helper)),
    (Foo,): (Charlie,(*SIXES_WIDES,Shorts,Helper3)),
    (Foo,Foo): (Dan,(*SIXES_THREES,All)),
    (Foo,Foo,Foo): CHARLIE_ZERO,
    (Foo,Foo,Bar): (Dan,SIXES),
        (Foo,Foo,Bar,Bar): (Charlie,SIXES_TWOS),
            (Foo,Foo,Bar,Bar,Foo): CHARLIE_ZERO,
            (Foo,Foo,Bar,Bar,Baz): CHARLIE_ZERO,
        (Foo,Foo,Bar,Baz): BOB_ZERO,
            (Foo,Bar,Baz,Foo,Foo): BOB_ZERO,
            (Foo,Bar,Baz,Foo,Baz): BOB_ZERO,
        (Foo,Foo,Baz,Bar): (Charlie,(All,)),
    (Foo,Foo,Baz): BOB_ZERO,

    (Foo,Bar): ALICE_SIXES,
    (Foo,Bar,Foo): (Dan,SIXES_ONES),
        (Foo,Bar,Foo,Foo): BOB_ZERO,
        (Foo,Bar,Foo,Bar): BOB_ZERO,
        (Foo,Bar,Foo,Baz): CHARLIE_ZERO,
            (Foo,Bar,Baz,Baz,Foo): (Alice,()),
    (Foo,Bar,Bar): (Charlie,SIXES_ALL),
        (Foo,Bar,Bar,Foo): CHARLIE_ZERO,
        (Foo,Bar,Bar,Bar): BOB_ZERO,
    (Foo,Bar,Baz): (Alice,SIXES_THREES),
        (Foo,Bar,Baz,Foo): (Bob,SIXES_THREES),
        (Foo,Bar,Baz,Bar): BOB_ZERO,
        (Foo,Bar,Baz,Baz): (Dan,SIXES_TWOS),
            (Foo,Bar,Baz,Baz,Baz): BOB_ZERO,

    (Foo,Baz): (Bob,(*SIXES_WIDES,Threes,Ones,All)),
    (Foo,Baz,Foo): DAN_ZERO,
        (Foo,Baz,Foo,Bar): (Charlie,(All,)),
    (Foo,Baz,Bar): (Bob,(*SIXES_WIDES,All)),
        (Foo,Baz,Bar,Foo): BOB_ZERO,
        (Foo,Baz,Bar,Bar): (Alice,()),
        (Foo,Baz,Bar,Baz): BOB_ZERO,
    (Foo,Baz,Baz): DAN_ZERO,
        (Foo,Baz,Baz,Foo): BOB_ZERO,

    # I couldn't find a generic way to transform my questions for this,
    # so I ended up just finding similar enough patterns instead of generalizing it for all 3
    (Bar,): (Dan, (*SIXES_WIDES,Helper3,All,Threes,Ones,Bottom)),
    (Bar,Foo): (Charlie,(*SIXES_THREES,Top)),
    (Bar,Foo,Foo): (Bob,(Ones,)),
        (Bar,Foo,Foo,Foo): BOB_ZERO,
        (Bar,Foo,Foo,Bar): DAN_ZERO,
        (Bar,Foo,Foo,Baz): BOB_ZERO,
    (Bar,Foo,Bar): (Bob,(*SIXES_TWOS,Shorts,All)),
        (Bar,Foo,Bar,Foo): BOB_ZERO,
        (Bar,Foo,Bar,Bar): BOB_ZERO,
        (Bar,Foo,Bar,Baz): BOB_ZERO,
    (Bar,Foo,Baz): (Dan,SIXES_ALL),
        (Bar,Foo,Baz,Foo): CHARLIE_ZERO,
        (Bar,Foo,Baz,Bar): DAN_ZERO,
        (Bar,Foo,Baz,Baz): DAN_ZERO,

    (Bar,Bar): (Bob,(*SIXES_THREES,All)),
    (Bar,Bar,Foo): CHARLIE_ZERO,
        (Bar,Bar,Foo,Baz): (Dan,(All,)),
    (Bar,Bar,Bar): BOB_ZERO,
    (Bar,Bar,Baz): (Bob,SIXES),
        (Bar,Bar,Baz,Foo): BOB_ZERO,
        (Bar,Bar,Baz,Baz): (Dan,SIXES_THREES),
            (Bar,Bar,Baz,Baz,Foo): DAN_ZERO,
            (Bar,Bar,Baz,Baz,Bar): DAN_ZERO,

    (Bar,Baz): ALICE_SIXES,
    (Bar,Baz,Foo): (Alice,SIXES_TWOS),
        (Bar,Baz,Foo,Foo): (Charlie,SIXES_TWOS),
            (Bar,Baz,Foo,Foo,Foo): BOB_ZERO,
            (Bar,Baz,Foo,Foo,Bar): CHARLIE_ZERO,
        (Bar,Baz,Foo,Bar): (Bob,SIXES_TWOS),
        (Bar,Baz,Foo,Baz): BOB_ZERO,
    (Bar,Baz,Bar): (Charlie,(*SIXES_THREES,Bottom)),
        (Bar,Baz,Bar,Foo): BOB_ZERO,
        (Bar,Baz,Bar,Bar): BOB_ZERO,
            (Bar,Baz,Foo,Bar,Foo): BOB_ZERO,
            (Bar,Baz,Foo,Bar,Bar): BOB_ZERO,
        (Bar,Baz,Bar,Baz): DAN_ZERO,
    (Bar,Baz,Baz): (Dan,SIXES_TWOS),
        (Bar,Baz,Baz,Bar): DAN_ZERO,
        (Bar,Baz,Baz,Baz): BOB_ZERO,


    (Baz,): (Bob, (*SIXES_WIDES,Helper,Threes,Twos,Top)),
    (Baz,Foo): ALICE_SIXES,
    (Baz,Foo,Foo): (Bob,SIXES_ALL),
        (Baz,Foo,Foo,Foo): CHARLIE_ZERO,
        (Baz,Foo,Foo,Baz): BOB_ZERO,
    (Baz,Foo,Bar): (Alice,SIXES_ONES),
        (Baz,Foo,Bar,Foo): CHARLIE_ZERO,
        (Baz,Foo,Bar,Bar): (Dan,SIXES_THREES),
            (Baz,Foo,Bar,Bar,Bar): CHARLIE_ZERO,
            (Baz,Foo,Bar,Bar,Baz): DAN_ZERO,
        (Baz,Foo,Bar,Baz): (Charlie,SIXES_THREES),
            (Baz,Foo,Bar,Baz,Bar): CHARLIE_ZERO,
    (Baz,Foo,Baz): (Dan,(*SIXES_ONES,All)),
        (Baz,Foo,Baz,Foo): CHARLIE_ZERO,
        (Baz,Foo,Baz,Bar): BOB_ZERO,
            (Baz,Foo,Bar,Baz,Baz): CHARLIE_ZERO,
        (Baz,Foo,Baz,Baz): CHARLIE_ZERO,

    (Baz,Bar): (Dan,(*SIXES_THREES,Ones,All,Shorts)),
    (Baz,Bar,Foo): (Bob,SIXES_ONES),
        (Baz,Bar,Foo,Foo): CHARLIE_ZERO,
        (Baz,Bar,Foo,Bar): DAN_ZERO,
        (Baz,Bar,Foo,Baz): BOB_ZERO,
    (Baz,Bar,Bar): (Charlie,(Ones,)),
        (Baz,Bar,Bar,Foo): CHARLIE_ZERO,
        (Baz,Bar,Bar,Bar): CHARLIE_ZERO,
        (Baz,Bar,Bar,Baz): BOB_ZERO,
    (Baz,Bar,Baz): (Charlie,(*SIXES_THREES,All)),
        (Baz,Bar,Baz,Foo): BOB_ZERO,
        (Baz,Bar,Baz,Bar): BOB_ZERO,
        (Baz,Bar,Baz,Baz): CHARLIE_ZERO,

    (Baz,Baz): (Charlie,(*SIXES_TWOS,All)),
    (Baz,Baz,Foo): (Charlie,SIXES),
        (Baz,Baz,Foo,Foo): (Bob,SIXES_THREES),
            (Baz,Baz,Foo,Foo,Bar): DAN_ZERO,
            (Baz,Baz,Foo,Foo,Baz): BOB_ZERO,
        (Baz,Baz,Foo,Bar): CHARLIE_ZERO,
    (Baz,Baz,Bar): (Charlie,SIXES_ALL),
        (Baz,Baz,Bar,Foo): CHARLIE_ZERO,
        (Baz,Baz,Bar,Bar): DAN_ZERO,
    (Baz,Baz,Baz): CHARLIE_ZERO,

    (Foo, Foo, Foo, Foo): 16, (Foo, Foo, Foo, Bar): 22, (Foo, Foo, Foo, Baz): 22, (Foo, Foo, Bar, Bar, Foo, Foo): 12, (Foo, Foo, Bar, Bar, Foo, Baz): 2, (Foo, Foo, Bar, Bar, Baz, Foo): 14, (Foo, Foo, Bar, Bar, Baz, Baz): 8, (Foo, Foo, Bar, Baz, Bar): 11, (Foo, Foo, Bar, Baz, Baz): 21, (Foo, Foo, Baz, Foo): 8, (Foo, Foo, Baz, Bar, Foo): 10, (Foo, Foo, Baz, Bar, Bar): 14, (Foo, Foo, Baz, Baz): 20, (Foo, Bar, Foo, Foo, Foo): 10, (Foo, Bar, Foo, Foo, Baz): 20, (Foo, Bar, Foo, Bar, Bar): 11, (Foo, Bar, Foo, Bar, Baz): 21, (Foo, Bar, Foo, Baz, Bar): 17, (Foo, Bar, Foo, Baz, Baz): 23, (Foo, Bar, Bar, Foo, Foo): 13, (Foo, Bar, Bar, Foo, Bar): 3, (Foo, Bar, Bar, Bar, Foo): 10, (Foo, Bar, Bar, Bar, Baz): 20, (Foo, Bar, Baz, Foo, Foo, Foo): 7, (Foo, Bar, Baz, Foo, Foo, Baz): 1, (Foo, Bar, Baz, Foo, Baz, Foo): 10, (Foo, Bar, Baz, Foo, Baz, Baz): 20, (Foo, Bar, Baz, Bar, Foo): 10, (Foo, Bar, Baz, Bar, Baz): 20, (Foo, Bar, Baz, Baz, Foo, Foo): 4, (Foo, Bar, Baz, Baz, Foo, Baz): 18, (Foo, Bar, Baz, Baz, Baz, Foo): 10, (Foo, Bar, Baz, Baz, Baz, Baz): 20, (Foo, Baz, Foo, Foo): 20, (Foo, Baz, Foo, Bar, Bar): 22, (Foo, Baz, Foo, Bar, Baz): 10, (Foo, Baz, Foo, Baz): 16, (Foo, Baz, Bar, Foo, Foo): 7, (Foo, Baz, Bar, Foo, Bar): 1, (Foo, Baz, Bar, Bar, Foo): 3, (Foo, Baz, Bar, Bar, Baz): 13, (Foo, Baz, Bar, Baz, Bar): 9, (Foo, Baz, Bar, Baz, Baz): 15, (Foo, Baz, Baz, Foo, Bar): 8, (Foo, Baz, Baz, Foo, Baz): 14, (Foo, Baz, Baz, Bar): 21, (Foo, Baz, Baz, Baz): 11, (Bar, Foo, Foo, Foo, Foo): 21, (Bar, Foo, Foo, Foo, Baz): 9, (Bar, Foo, Foo, Bar, Foo): 16, (Bar, Foo, Foo, Bar, Baz): 22, (Bar, Foo, Foo, Baz, Foo): 15, (Bar, Foo, Foo, Baz, Baz): 11, (Bar, Foo, Bar, Foo, Foo): 21, (Bar, Foo, Bar, Foo, Baz): 11, (Bar, Foo, Bar, Bar, Bar): 8, (Bar, Foo, Bar, Bar, Baz): 14, (Bar, Foo, Bar, Baz, Foo): 20, (Bar, Foo, Bar, Baz, Baz): 10, (Bar, Foo, Baz, Foo, Bar): 12, (Bar, Foo, Baz, Foo, Baz): 2, (Bar, Foo, Baz, Bar, Foo): 4, (Bar, Foo, Baz, Bar, Bar): 18, (Bar, Foo, Baz, Baz, Foo): 11, (Bar, Foo, Baz, Baz, Baz): 21, (Bar, Bar, Foo, Foo): 8, (Bar, Bar, Foo, Bar): 16, (Bar, Bar, Foo, Baz, Bar): 14, (Bar, Bar, Foo, Baz, Baz): 22, (Bar, Bar, Bar, Foo): 20, (Bar, Bar, Bar, Bar): 10, (Bar, Bar, Bar, Baz): 20, (Bar, Bar, Baz, Foo, Foo): 15, (Bar, Bar, Baz, Foo, Baz): 9, (Bar, Bar, Baz, Baz, Foo, Foo): 16, (Bar, Bar, Baz, Baz, Foo, Bar): 22, (Bar, Bar, Baz, Baz, Bar, Foo): 5, (Bar, Bar, Baz, Baz, Bar, Bar): 19, (Bar, Baz, Foo, Foo, Foo, Foo): 14, (Bar, Baz, Foo, Foo, Foo, Bar): 8, (Bar, Baz, Foo, Foo, Bar, Foo): 2, (Bar, Baz, Foo, Foo, Bar, Bar): 12, (Bar, Baz, Foo, Bar, Foo, Foo): 14, (Bar, Baz, Foo, Bar, Foo, Bar): 8, (Bar, Baz, Foo, Bar, Bar, Foo): 0, (Bar, Baz, Foo, Bar, Bar, Bar): 6, (Bar, Baz, Foo, Baz, Foo): 14, (Bar, Baz, Foo, Baz, Bar): 8, (Bar, Baz, Bar, Foo, Foo): 15, (Bar, Baz, Bar, Foo, Baz): 9, (Bar, Baz, Bar, Bar, Foo): 14, (Bar, Baz, Bar, Bar, Bar): 8, (Bar, Baz, Bar, Baz, Foo): 17, (Bar, Baz, Bar, Baz, Baz): 23, (Bar, Baz, Baz, Bar, Bar): 18, (Bar, Baz, Baz, Bar, Baz): 4, (Bar, Baz, Baz, Baz, Foo): 14, (Bar, Baz, Baz, Baz, Bar): 8, (Baz, Foo, Foo, Foo, Bar): 22, (Baz, Foo, Foo, Foo, Baz): 16, (Baz, Foo, Foo, Baz, Foo): 0, (Baz, Foo, Foo, Baz, Baz): 6, (Baz, Foo, Bar, Foo, Bar): 22, (Baz, Foo, Bar, Foo, Baz): 16, (Baz, Foo, Bar, Bar, Bar, Bar): 22, (Baz, Foo, Bar, Bar, Bar, Baz): 16, (Baz, Foo, Bar, Bar, Baz, Bar): 5, (Baz, Foo, Bar, Bar, Baz, Baz): 19, (Baz, Foo, Bar, Baz, Bar, Bar): 22, (Baz, Foo, Bar, Baz, Bar, Baz): 16, (Baz, Foo, Bar, Baz, Baz, Bar): 3, (Baz, Foo, Bar, Baz, Baz, Baz): 13, (Baz, Foo, Baz, Foo, Foo): 17, (Baz, Foo, Baz, Foo, Bar): 23, (Baz, Foo, Baz, Bar, Foo): 11, (Baz, Foo, Baz, Bar, Bar): 21, (Baz, Foo, Baz, Baz, Bar): 22, (Baz, Foo, Baz, Baz, Baz): 16, (Baz, Bar, Foo, Foo, Foo): 15, (Baz, Bar, Foo, Foo, Bar): 9, (Baz, Bar, Foo, Bar, Foo): 5, (Baz, Bar, Foo, Bar, Baz): 19, (Baz, Bar, Foo, Baz, Bar): 0, (Baz, Bar, Foo, Baz, Baz): 6, (Baz, Bar, Bar, Foo, Foo): 17, (Baz, Bar, Bar, Foo, Bar): 9, (Baz, Bar, Bar, Bar, Foo): 15, (Baz, Bar, Bar, Bar, Bar): 23, (Baz, Bar, Bar, Baz, Foo): 10, (Baz, Bar, Bar, Baz, Bar): 20, (Baz, Bar, Baz, Foo, Foo): 9, (Baz, Bar, Baz, Foo, Bar): 15, (Baz, Bar, Baz, Bar, Foo): 8, (Baz, Bar, Baz, Bar, Bar): 14, (Baz, Bar, Baz, Baz, Foo): 22, (Baz, Bar, Baz, Baz, Baz): 16, (Baz, Baz, Foo, Foo, Bar, Bar): 10, (Baz, Baz, Foo, Foo, Bar, Baz): 20, (Baz, Baz, Foo, Foo, Baz, Bar): 1, (Baz, Baz, Foo, Foo, Baz, Baz): 7, (Baz, Baz, Foo, Bar, Foo): 17, (Baz, Baz, Foo, Bar, Bar): 23, (Baz, Baz, Bar, Foo, Foo): 16, (Baz, Baz, Bar, Foo, Bar): 22, (Baz, Baz, Bar, Bar, Foo): 10, (Baz, Baz, Bar, Bar, Baz): 20, (Baz, Baz, Baz, Foo): 8, (Baz, Baz, Baz, Bar): 8, (Baz, Baz, Baz, Baz): 14
}


PEOPLE_PERM = list(permutations(tuple(PEOPLE)))
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

            v = solution[answers]
            try:
                recurse(answers+(self.get_response(get_qa(*v)),))
            except Exception as e:
                for p, s in zip(PEOPLE_PERM[v], STUDIES):
                    self.guess[p] = s
        recurse(())