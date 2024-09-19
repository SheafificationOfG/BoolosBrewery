# Writing your own strategy

I think the best way to explain how to create a strategy is to actually create one, so let's implement a strategy for solving the [easy version](./variants.md#easy-mode) of the logic puzzle.

Remember in this situation that there is only Alice and Bob, one being a mathematician and the other being a physicist.
The optimal solution only requires 1 question, but to avoid spoilers (and to demonstrate some of the API), let's implement a less efficient strategy:

1. We will first ask both Alice and Bob to say "yes" in their convention. One of them will be a "foo sayer" (i.e., someone who says `foo` to mean "yes").
1. Once we know who the "foo sayer" is, we can ask them if they study Mathematics. If they say `foo`, then they do indeed study Mathematics; otherwise, they study Physics.
1. For good measure, we will also ask the "foo sayer" if the other person studies Mathematics.

## Implementing the strategy

This strategy is already implemented in `submissions/sample/tutorial.py`.
Here, we will explain the source step-by-step.

> [!WARNING]
> If you intend to submit your solution to the main repo, make sure you put your strategy file in the `submissions/` folder and **NOT** any of its subfolders!

### Strategy template

In order to ask your colleagues questions, import the `strats` module, and copy the following template:

```python
from strats import *

class Strategy(Easy):
    """
    Your strategy *must* be implemented in a class called "Strategy".
    The target puzzle variant is specified by deriving from "Easy" (as shown above), "Default", or "Hard".
    """

    question_limit = 4
    """
    Your strategy *must* specify an upper bound for how many questions it will ask.
    You will automatically fail if you ask more questions than the limit you specify.
    However, you may ask fewer questions than your allocated limit.
    Our strategy uses exactly four questinos in all cases.
    """

    def solve(game):
        """
        We will implement our strategy logic in this function!
        """
        ...
```
> [!NOTE]
> The argument to the `solve` function can be whatever you want (and, properly, it should be called `self`).
> I just picked `game` because I think it's more telling in this case.

> [!TIP]
> The `question_limit` needs only to be an *upper bound*.
> This value is used so that the game can generate all possible response sequences of the engineer.
> Since the number of possible response sequences grows *exponentially* with the number of questions, try to keep the question limit reasonable (otherwise, your submission will time out).

Now, let's go about implementing our strategy.

### Forming a question

While, in principle, you could write your questions down as strings, you'll probably have a better time using the API provided by `strats`, which tries to mirror (in a *very weak sense*) the syntax for questions.

| Type | Syntax | `strats` API |
|:----:|:------ |:------------ |
| Person | `Alice` | `strats.Alice` |
|| `Bob` | `strats.Bob` |
|| `Charlie` | `strats.Charlie` |
|| `Dan` | `strats.Dan` |
| Field | `Mathamatics` | `strats.Math` |
|| `Physics` | `strats.Phys` |
|| `Engineering` | `strats.Engg` |
|| `Philosophy` | `strats.Phil` |
| Response | `Foo` | `strats.Foo` |
|| `Bar` | `strats.Bar` |
|| `Baz` | `strats.Baz` |
| Boolean | `true` | `True` |
|| `false` | `False` |
| Question | *person* `:` *expr* `?` | `person.ask(expr)` |
| Negation | `not` *expr* | `expr.invert()` or `~expr` |
| Conjunction | *expr1* `and` *expr2* | `expr1.and_(expr2)` or `expr1 & expr2` |
| Disjunction | *expr1* `or` *expr2* | `expr1.or_(expr2)` or `expr1 \| expr2` |
| Implication | *expr1* `implies` *expr2* | `expr1.implies(expr2)` |
| Equivalence | *expr1* `iff` *expr2* | `expr1.iff(expr2)` |
| Exclusive disjunction | *expr1* `xor` *expr2* | `expr1.xor(expr2)` |
| Response comparison | *resp1* `is` *resp2* | `resp1.equals(resp2)` |
|| *resp1* `not` *resp2* | `resp1.not_equals(resp2)` |
| Field inquiry | *person* `studies` *field* | `person.studies(field)` |

For example, the question
```yaml
Bob: Charlie studies Engineering implies Alice studies Mathematics?
```
can be constructed as
```python
Bob.ask(Charlie.studies(Engg).implies(Alice.studies(Math)))
```

Close enough, eh?

### Getting responses

Calling `person.ask(...)` doesn't actually *ask* the question; it's just syntax.
To actually commit to asking a question, and getting a response, call
```python
    def solve(game):
        # ...
        response = game.get_response(question)
```
where `question` is built as described [above](#forming-a-question).
The return value will be a `strats.Response` object that we can subsequently analyse.

For example, we can ask Alice and Bob each to say "yes", and then use their responses to find the "foo sayer".

```python
    def solve(game):
        # ...

        # NOTE: this counts as *two* questions!
        alice_response = game.get_response(Alice.ask(True))
        bob_response = game.get_response(Bob.ask(True))

        if alice_response == Foo:
            foo_sayer = Alice
            bar_sayer = Bob
        else: # alice_response == Bar
            foo_sayer = Bob
            bar_sayer = Alice
```

> [!TIP]
> Python is much more expressive than my [actually supported syntax](syntax.md).
> `True` is just a Python constant, so you could replace this with any statement that Python evaluates to `True`, such as `1+1==2`, or `"g++" > "clang"`.

Once we figure out who the "foo sayer" is, our next step was to determine if they are the mathematician.
Simple enough: just ask.

```python
def solve(game):
    # ...

    foo_does_math = game.get_response(foo_sayer.ask(foo_sayer.studies(Math)))
    if foo_does_math == Foo:
        # foo_sayer studies mathematics!
        ...
    else:
        # foo_sayer studies physics!
        ...
```

### Building your guess

As you interact with your colleagues and learn partial information, you can store it in `game.guess`, which is a `strats.Guesses` instance.
Initially, all guesses are `None`.

To guess that, for instance, Alice studies mathematics, you can write:
```python
game.guess[Alice] = Math 
```

Now we can record whether or not the "foo sayer" is a mathematician!
```python
def solve(game):
    # ...

    foo_does_math = game.get_response(foo_sayer.ask(foo_sayer.studies(Math)))
    if foo_does_math == Foo:
        # foo_sayer studies mathematics!
        game.guess[foo_sayer] = Math
    else:
        # foo_sayer studies physics!
        game.guess[foo_sayer] = Phys
```

When the `solve` function returns (i.e., you call `return`, or you reach the end of the function), the contents of `game.guess` will be forwarded to the puzzle, and your guesses will be checked!

> [!IMPORTANT]
> You are free to assign any type of value to your guess for each person while you try and solve the puzzle (e.g., maybe you want `game.guess[person]` to store a set of all possible fields `peron` could be).
>
> However, when the `solve` function returns:
> - Your guesses for people present in the puzzle (e.g., Alice and Bob in easy mode) **must** be of type `strats.Field`.
> - Your guesses for people *not* present in the puzzle (e.g., Charlie and Dan in easy mode) **must** be `None`.

Now, for completeness, let's finally ask the "foo sayer" what the "bar sayer" studies.

```python
def solve(game):
    # ...

    bar_does_math = game.get_response(foo_sayer.ask(bar_sayer.studies(Math)))
    if bar_does_math == Foo:
        # bar_sayer studies mathematics!
        game.guess[bar_sayer] = Math
    else:
        # bar_sayer studies physics!
        game.guess[bar_sayer] = Phys
```

## Evaluating your strategy

Once you have written your strategy, you can test it by simply running
```sh
python3 test_strategy.py --file path/to/your/strategy.py
# NOTE: If your strategy is in submissions/, then you can just run test_strategy.py with no arguments!
```
from the root directory of the repo.

> [!NOTE]
> If the process seems to hang (and you're sure your solution isn't to blame), it might be because of how subprocess IO pipes are buffering (surely it's not a deadlock!).
> You may find success running
> ```sh
> stdbuf -oL python3 test_strategy --file path/to/your/strategy.py
> ```
> instead.

## Troubleshooting

If your strategy is failing, Python's detailed error messages or the game's log info should hopefully help you patch things up.
If this doesn't seem like enough information, you can also dump the strategy's interaction history with the various iterations of the game by setting the `STRAT_LOG` file:
```sh
STRAT_LOG=path/to/dump/file.dump python3 test_strategy.py --file path/to/your/strategy.py
```


# Submitting your strategy

If you have a strategy you're proud of, try merging it with the main repo by making a pull request.

Before making a pull request, please ensure the following:

- You only submit **one strategy**.
- Your submission is in the `submissions/` folder and **not a subfolder** therein.
- Your submission actually [passes](#evaluating-your-strategy).
    You should be able to run `python3 test_strategy.py` with no arguments!
- Document your strategy so that everyone can appreciate your cleverness!

> [!IMPORTANT]
> This is a public repo, and solutions are open-source, so please be mindful of your choice of words, file names, variable names, etc.

## Scoring criteria

Submissions are sorted first by the **average number of questions** required to solve the puzzle, where the average runs over all possible scenarios.

For submissions that solve the puzzle in the same average number of questions, they are then sorted based on **minimal "complexity"**.
What is complexity?
Well, it roughly corresponds to the size of the [abstract syntax tree](https://en.wikipedia.org/wiki/Abstract_syntax_tree) of your solution.
In simpler terms, this measures the "size" of the program, but is more refined than basing size on "number of lines" or "file size"; in particular, you are **not** punished for comments, large variable names, etc.

> The purpose of the "complexity" metric is to encourage more submissions, even if you can't beat the current best strictly in terms of number of questions.
> If you think you have a slicker way of implementing an existing strategy, this is also fair game!
>
> Note also that this criterion was whipped together, so may be **subject to change** (depending on if people find ways to abuse the current metric; it isn't very well-thought-out).

If, somehow, submissions tie both on the average number of questions *and* the complexity score, then submissions are sorted by acceptance date.