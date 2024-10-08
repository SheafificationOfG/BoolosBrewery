from itertools import *
from strats import *
from functools import reduce

XOR, PEOPLE, STUDIES, WORDS = lambda a, b: a.xor(b), (Alice, Bob, Charlie, Dan), (Math, Phys, Engg, Phil), (Foo,Bar,Baz)

# Checks if the study of who is less than the study of who2 (check order in STUDIES above)
def lessthan(who, who2):
    return reduce(
        lambda acc, sub: acc.and_(~who2.studies(sub)).or_(who.studies(sub)),
        [Phys, Math],
        who.studies(Engg) # who2.studies(Engg).implies(who.studies(Engg))
    )

def phil(word):
    return Philosopher.ask(True).equals(word)
def phys(word):
    return Mathematician.ask(False).equals(word)

# This has two functions, first is make it so all of FOO,BAR,BAZ with the same philosopher word are paired up
# So for example, the mathematician will always answer the same word no matter if the combination is FOO,BAR,BAZ or BAR,FOO,BAZ
# The second function is make the person answer the same word no matter if they're the mathematician or philosopher.
# So for example, if the combination is FOO,BAR,BAZ or BAR,FOO,BAZ the asked person will always answer FOO if they're math or phys
# This is split up by phil word too, so BAZ -> FOO, FOO -> BAR, BAR -> BAZ (I don't remember the exacts)
# Technically this should be combined with Sixes to actually have it do this, but since that appears less often we have it inverted
def Truthy():
    return phys(baz_).xor(Mathematician.ask(True).equals(foo_).and_(phys(bar_)))

# The rest of these are to split up the possibility space. If Alice is the person asked, the "rows" being talked about go as follows:
# 0: Alice, Bob, Charlie, Dan
# 1: Alice, Bob, Dan, Charlie
# 2: Alice, Charlie, Bob, Dan
# 3: Alice, Dan, Bob, Charlie
# 4: Alice, Charlie, Dan, Bob
# 5: Alice, Dan, Charlie, Bob
# 6: Bob, Alice, Charlie, Dan
# 7: Bob, Alice, Dan, Charlie
# 8: Charlie, Alice, Bob, Dan
# 9: Dan, Alice, Bob, Charlie
# 10: Charlie, Alice, Dan, Bob
# 11: Dan, Alice, Charlie, Bob
# They're basically sorted by (index of asker, index of lowest named person after asked, index of next lowest name person)
# "Flipping" is simply making a set of rows have the opposite boolean result

def EXCEPT(who):
    people = list(PEOPLE)
    people.remove(who)
    return people

# Tries to splits the possibility space so that:
# - FOO -> P1 or P2 can be engineers
# - BAR -> P2 or P3 can be engineers
# - BAZ -> P1 or P3 can be engineers
# The goal is to have as few possible engineers as possible in each outcome
def HELPER(offset):
    def f(who):
        def force(who, word):
            return phil(word).and_(who.studies(Engg))
        people = EXCEPT(who)
        people = people[offset:]+people[:offset]
        return force(people[0], Foo).or_(force(people[1], Bar)).or_(force(people[2], Baz))
    return f

# Flips every set of 6 rows
def Sixes(who):
    return who.studies(Math)


def LESSTHAN(i, j):
    def f(who):
        people = EXCEPT(who)
        return lessthan(people[i], people[j])
    return f

# Flips every set of three, [x,x,o,x,o,o], and every other row respectively. Helper is described above
Threes, Twos, Ones, Helper, Helper3 = LESSTHAN(0, 2), LESSTHAN(0, 1), LESSTHAN(1, 2), HELPER(0), HELPER(1)

# Flips the bottom row of each set of six
def Bottom(who):
    first, second, last = EXCEPT(who)
    return lessthan(last, second).and_(lessthan(second, first))

# Flips the top row of each set of six
def Top(who):
    first, second, last = EXCEPT(who)
    return lessthan(first, second).and_(lessthan(second, last))

# Flips all results where the Philosopher doesn't say Baz
def Wides(_):
    return ~phil(baz_)

# Flips all results where the Philosopher says Foo
def Shorts(_):
    return phil(foo_)

# Flips all rows
def All(_):
    return True

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

# Since writing (foo, bar, foo) etc. over and over takes a lot of tokens, we can instead use their index in the permutation table
KEYS = [
    j
    for i in range(7)
    for j in product(WORDS, repeat=i)
]
# A dict of (previous answers) -> (next question)
# If the value is a number, then it uses the index in the permutation of people as the solution instead of asking another question
PEOPLE_PERM = list(permutations(PEOPLE))
solution = {
    0: (Alice,(*SIXES_WIDES,Shorts,Helper)),
        1: (Charlie,(*SIXES_WIDES,Shorts,Helper3)),
            4: (Dan,(*SIXES_THREES,All)),
                13: CHARLIE_ZERO,
                    40: 16,
                    41: 22,
                    42: 22,
                14: (Dan,SIXES),
                    44: (Charlie,SIXES_TWOS),
                        133: CHARLIE_ZERO,
                            400: 12,
                            402: 2,
                        135: CHARLIE_ZERO,
                            406: 14,
                            408: 8,
                    45: BOB_ZERO,
                        137: 11,
                        138: 21,
                15: BOB_ZERO,
                    46: 8,
                    47: (Charlie,(All,)),
                        142: 10,
                        143: 14,
                    48: 20,
            5: ALICE_SIXES,
                16: (Dan,SIXES_ONES),
                    49: BOB_ZERO,
                        148: 10,
                        150: 20,
                    50: BOB_ZERO,
                        152: 11,
                        153: 21,
                    51: CHARLIE_ZERO,
                        155: 17,
                        156: 23,
                17: (Charlie,SIXES_ALL),
                    52: CHARLIE_ZERO,
                        157: 13,
                        158: 3,
                    53: BOB_ZERO,
                        160: 10,
                        162: 20,
                18: (Alice,SIXES_THREES),
                    55: (Bob,SIXES_THREES),
                        166: BOB_ZERO,
                            499: 7,
                            501: 1,
                        168: BOB_ZERO,
                            505: 10,
                            507: 20,
                    56: BOB_ZERO,
                        169: 10,
                        171: 20,
                    57: (Dan,SIXES_TWOS),
                        172: (Alice,()),
                            517: 4,
                            519: 18,
                        174: BOB_ZERO,
                            523: 10,
                            525: 20,
            6: (Bob,(*SIXES_WIDES,Threes,Ones,All)),
                19: DAN_ZERO,
                    58: 20,
                    59: (Charlie,(All,)),
                        179: 22,
                        180: 10,
                    60: 16,
                20: (Bob,(*SIXES_WIDES,All)),
                    61: BOB_ZERO,
                        184: 7,
                        185: 1,
                    62: (Alice,()),
                        187: 3,
                        189: 13,
                    63: BOB_ZERO,
                        191: 9,
                        192: 15,
                21: DAN_ZERO,
                    64: BOB_ZERO,
                        194: 8,
                        195: 14,
                    65: 21,
                    66: 11,
        # I couldn't find a person transform that made it possible to generalize for bar/baz on the second answer
        2: (Dan, (*SIXES_WIDES,Helper3,All,Threes,Ones,Bottom)),
            7: (Charlie,(*SIXES_THREES,Top)),
                22: (Bob,(Ones,)),
                    67: BOB_ZERO,
                        202: 21,
                        204: 9,
                    68: DAN_ZERO,
                        205: 16,
                        207: 22,
                    69: BOB_ZERO,
                        208: 15,
                        210: 11,
                23: (Bob,(*SIXES_TWOS,Shorts,All)),
                    70: BOB_ZERO,
                        211: 21,
                        213: 11,
                    71: BOB_ZERO,
                        215: 8,
                        216: 14,
                    72: BOB_ZERO,
                        217: 20,
                        219: 10,
                24: (Dan,SIXES_ALL),
                    73: CHARLIE_ZERO,
                        221: 12,
                        222: 2,
                    74: DAN_ZERO,
                        223: 4,
                        224: 18,
                    75: DAN_ZERO,
                        226: 11,
                        228: 21,
            8: (Bob,(*SIXES_THREES,All)),
                25: CHARLIE_ZERO,
                    76: 8,
                    77: 16,
                    78: (Dan,(All,)),
                        236: 14,
                        237: 22,
                26: BOB_ZERO,
                    79: 20,
                    80: 10,
                    81: 20,
                27: (Bob,SIXES),
                    82: BOB_ZERO,
                        247: 15,
                        249: 9,
                    84: (Dan,SIXES_THREES),
                        253: DAN_ZERO,
                            760: 16,
                            761: 22,
                        254: DAN_ZERO,
                            763: 5,
                            764: 19,
            9: ALICE_SIXES,
                28: (Alice,SIXES_TWOS),
                    85: (Charlie,SIXES_TWOS),
                        256: BOB_ZERO,
                            769: 14,
                            770: 8,
                        257: CHARLIE_ZERO,
                            772: 2,
                            773: 12,
                    86: (Bob,SIXES_TWOS),
                        259: BOB_ZERO,
                            778: 14,
                            779: 8,
                        260: BOB_ZERO,
                            781: 0,
                            782: 6,
                    87: BOB_ZERO,
                        262: 14,
                        263: 8,
                29: (Charlie,(*SIXES_THREES,Bottom)),
                    88: BOB_ZERO,
                        265: 15,
                        267: 9,
                    89: BOB_ZERO,
                        268: 14,
                        269: 8,
                    90: DAN_ZERO,
                        271: 17,
                        273: 23,
                30: (Dan,SIXES_TWOS),
                    92: DAN_ZERO,
                        278: 18,
                        279: 4,
                    93: BOB_ZERO,
                        280: 14,
                        281: 8,
        3: (Bob, (*SIXES_WIDES,Helper,Threes,Twos,Top)),
            10: ALICE_SIXES,
                31: (Bob,SIXES_ALL),
                    94: CHARLIE_ZERO,
                        284: 22,
                        285: 16,
                    96: BOB_ZERO,
                        289: 0,
                        291: 6,
                32: (Alice,SIXES_ONES),
                    97: CHARLIE_ZERO,
                        293: 22,
                        294: 16,
                    98: (Dan,SIXES_THREES),
                        296: CHARLIE_ZERO,
                            890: 22,
                            891: 16,
                        297: DAN_ZERO,
                            893: 5,
                            894: 19,
                    99: (Charlie,SIXES_THREES),
                        299: CHARLIE_ZERO,
                            899: 22,
                            900: 16,
                        300: CHARLIE_ZERO,
                            902: 3,
                            903: 13,
                33: (Dan,(*SIXES_ONES,All)),
                    100: CHARLIE_ZERO,
                        301: 17,
                        302: 23,
                    101: BOB_ZERO,
                        304: 11,
                        305: 21,
                    102: CHARLIE_ZERO,
                        308: 22,
                        309: 16,
            11: (Dan,(*SIXES_THREES,Ones,All,Shorts)),
                34: (Bob,SIXES_ONES),
                    103: CHARLIE_ZERO,
                        310: 15,
                        311: 9,
                    104: DAN_ZERO,
                        313: 5,
                        315: 19,
                    105: BOB_ZERO,
                        317: 0,
                        318: 6,
                35: (Charlie,(Ones,)),
                    106: CHARLIE_ZERO,
                        319: 17,
                        320: 9,
                    107: CHARLIE_ZERO,
                        322: 15,
                        323: 23,
                    108: BOB_ZERO,
                        325: 10,
                        326: 20,
                36: (Charlie,(*SIXES_THREES,All)),
                    109: BOB_ZERO,
                        328: 9,
                        329: 15,
                    110: BOB_ZERO,
                        331: 8,
                        332: 14,
                    111: CHARLIE_ZERO,
                        334: 22,
                        336: 16,
            12: (Charlie,(*SIXES_TWOS,All)),
                37: (Charlie,SIXES),
                    112: (Bob,SIXES_THREES),
                        338: DAN_ZERO,
                            1016: 10,
                            1017: 20,
                        339: BOB_ZERO,
                            1019: 1,
                            1020: 7,
                    113: CHARLIE_ZERO,
                        340: 17,
                        341: 23,
                38: (Charlie,SIXES_ALL),
                    115: CHARLIE_ZERO,
                        346: 16,
                        347: 22,
                    116: DAN_ZERO,
                        349: 10,
                        351: 20,
                39: CHARLIE_ZERO,
                    118: 8,
                    119: 8,
                    120: 14,
}

class Strategy(Hard):
    question_limit = 6

    def solve(self):
        def recurse(answers):
            global foo_, bar_, baz_
            WORD_OFFSET = 0 if len(answers) == 0 or answers[0] == Foo else 1 if answers[0] == Bar else 2
            foo_, bar_, baz_ = WORDS[WORD_OFFSET:]+WORDS[:WORD_OFFSET]

            v = solution[KEYS.index(answers)]
            # The try-catch just checks if you can split v into who and funcs, otherwise we know it's a number
            try:
                who, funcs = v
                recurse(answers+(self.get_response(who.ask(reduce(XOR, [f(who) for f in funcs], Truthy()))),))
            except:
                for p, s in zip(PEOPLE_PERM[v], STUDIES):
                    self.guess[p] = s
        recurse(())