from dataclasses import dataclass
from enum import Enum
from functools import cache
import math
from typing import Self
from strats import Alice, Bob, Charlie, Dan, Math, Phys, Engg, Phil, Foo, Bar, Baz
from strats.game.types import Expr, Field, Person, Response
from strats.strategy import Hard
from itertools import permutations

# import logging
# logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class RuleSet:
    math_true: Response
    phys_true: Response
    phil_always: Response | None = None

    def __repr__(self):
        return f"[{self.math_true} {self.phys_true}]"


@dataclass(frozen=True)
class State:
    field_mapping: tuple[tuple[Person, Field], ...]
    response_options: frozenset[RuleSet]

    def __repr__(self):
        return f"{self.field_mapping}, {[*self.response_options]}"


@dataclass
class MutableState:
    field_mapping: tuple[tuple[Person, Field], ...]
    response_options: set[RuleSet]

    def __repr__(self):
        return f"{self.field_mapping}, {self.response_options}"


@dataclass(frozen=True)
class FieldQuery:
    field: Field
    target: Person

    def __repr__(self):
        return f"Does {self.target} study {self.field}?"


class operator(Enum):
    NOT = "not"
    EQ = "eq"
    NEQ = "neq"
    AND = "and"
    OR = "or"
    IMPLIES = "implies"
    IFF = "iff"
    XOR = "xor"


truth_table = {
    operator.AND: (0, 0, 0, 1),
    operator.OR: (0, 1, 1, 1),
    operator.IMPLIES: (1, 1, 0, 1),
    operator.IFF: (1, 0, 0, 1),
    operator.XOR: (0, 1, 1, 0),
}


@dataclass(frozen=True)
class ExprTNode:
    left: Self | Response | FieldQuery | bool
    right: Self | Response | FieldQuery | bool | None
    op: operator

    def __repr__(self):
        if self.right is None:
            return f"{self.op}  ({self.left})"
        else:
            return f"({self.left}  {self.op}  {self.right})"

    def evaluate_child(self, child: Self | Response | FieldQuery | bool) -> Expr:
        match child:
            case ExprTNode():
                return child.generate_expr()
            case FieldQuery():
                return child.target.studies(child.field)
            case Response():
                return Expr(str(child).capitalize())
            case bool():
                return Expr(child)

    def generate_expr(self) -> Expr:
        left = self.evaluate_child(self.left)
        right = self.evaluate_child(self.right) if self.op != operator.NOT else None  # type: ignore

        match self.op:
            case operator.NOT:
                return left.invert()
            case operator.EQ:
                return Expr(f"({left} is {right})")
            case operator.NEQ:
                return Expr(f"({left} not {right})")
            case operator.AND:
                return left.and_(right)
            case operator.OR:
                return left.or_(right)
            case operator.IMPLIES:
                return left.implies(right)
            case operator.IFF:
                return left.iff(right)
            case operator.XOR:
                return left.xor(right)


ExprT = ExprTNode | Response | FieldQuery | bool


@cache
def generate_ExprT(
    responses: tuple[Response, ...],
    fields: tuple[Field, ...],
    persons: tuple[Person, ...],
) -> tuple[ExprTNode, ...]:
    fieldQueries = [FieldQuery(field, person) for field in fields for person in persons]
    possible_nodes: list[bool | Response | FieldQuery] = [
        True,
        False,
        *fieldQueries,
    ]

    ret: list[ExprTNode] = []

    # for left in possible_nodes:
    #     ret.append(ExprTNode(left, None, operator.NOT))

    for op in operator:
        for left in possible_nodes:
            if op == operator.NOT:
                ret.append(ExprTNode(left, None, op))
                continue
            for right in possible_nodes + [*responses]:
                ret.append(ExprTNode(left, right, op))

    return tuple(ret)


@cache
def generate_states(
    persons: tuple[Person, ...],
    fields: tuple[Field, ...],
    responses: tuple[Response, ...],
) -> tuple[State, ...]:
    field_mappings = [
        tuple((field, response) for field, response in zip(persons, perm))
        for perm in permutations(fields, len(fields))
    ]

    response_options = set(
        RuleSet(*responses) for responses in permutations(responses, len(responses))
    )

    states = tuple(
        State(field_mapping, frozenset(response_options))
        for field_mapping in field_mappings
    )

    return states


@cache
def evaluate_node(
    node: ExprTNode | Response | FieldQuery | bool,
    state: State,
    true_response: Response,
    false_response: Response,
) -> Response:
    match node:
        case Response():
            return node

        case bool():
            return true_response if node else false_response

        case FieldQuery():
            for person, field in state.field_mapping:
                if person == node.target:
                    return true_response if field == node.field else false_response
            raise ValueError(f"Person {node.target} not found in state {state}")

    left = evaluate_node(node.left, state, true_response, false_response)
    if left not in (true_response, false_response):
        return left

    if node.op == operator.NOT:
        if left == true_response:
            return false_response
        return true_response

    right = evaluate_node(node.right, state, true_response, false_response)  # type: ignore

    if right not in (true_response, false_response):
        return right

    if node.op == operator.EQ:
        return true_response if left == right else false_response

    if node.op == operator.NEQ:
        return true_response if left != right else false_response

    truth_index = ((left == true_response) << 1) + (right == true_response)

    return true_response if truth_table[node.op][truth_index] else false_response


@cache
def evaluate_state(
    state: State, target: Person, ast: ExprT, responses: tuple[Response, ...]
) -> dict[Response, State]:
    response_map = {
        response: MutableState(state.field_mapping, set()) for response in responses
    }

    for rules in state.response_options:
        field = next(
            (field for person, field in state.field_mapping if person == target)
        )

        if field == Engg:
            response_map[rules.math_true].response_options.add(rules)
            response_map[rules.phys_true].response_options.add(rules)
            if rules.phil_always:
                response_map[rules.phil_always].response_options.add(rules)
            continue

        if field == Phil:
            response_map[rules.phil_always].response_options.add(rules)  # type: ignore
            continue

        if field == Math:
            true_response, false_response = rules.math_true, rules.phys_true

        else:
            true_response, false_response = rules.phys_true, rules.math_true

        res = evaluate_node(ast, state, true_response, false_response)

        if res not in (true_response, false_response):
            res = false_response

        response_map[res].response_options.add(rules)

    return {
        response: State(state.field_mapping, frozenset(state.response_options))
        for response, state in response_map.items()
    }


@cache
def evaluate_states(
    states: tuple[State, ...],
    target: Person,
    ast: ExprT,
    responses: tuple[Response, ...],
) -> dict[Response, tuple[State, ...]]:
    response_map = {response: [] for response in responses}

    for state in states:
        state_outcomes = evaluate_state(state, target, ast, responses)

        for response, state in state_outcomes.items():
            if state.response_options:
                response_map[response].append(state)

    return {response: tuple(states) for response, states in response_map.items()}


@cache
def get_best_query(
    states: tuple[State, ...],
    persons: tuple[Person, ...],
    fields: tuple[Field, ...],
    responses: tuple[Response, ...],
) -> tuple[ExprTNode, Person]:
    options = generate_ExprT(responses, fields, persons)
    best_query = (options[0], persons[0], [10000 for _ in responses])

    target = tuple(len(states) / len(responses) for _ in responses)

    for askee in persons:
        for option in options:
            state_spread = evaluate_states(states, askee, option, responses)

            best_query = min(
                best_query,
                (option, askee, tuple(len(states) for states in state_spread.values())),
                key=lambda x: math.dist(target, x[2]),
            )

    return best_query[:2]


class Strategy(Hard):
    question_limit = 10

    def solve(self):
        possible_bools = (Foo, Bar, Baz)
        persons = (Alice, Bob, Charlie, Dan)
        fields = (Math, Phys, Engg, Phil)

        states = generate_states(persons, fields, possible_bools)
        # logger.info(f"Starting states: {states}")

        while len(states) > 1:
            expr_t, person = get_best_query(
                tuple(states), persons, fields, possible_bools
            )

            state_spread = evaluate_states(states, person, expr_t, possible_bools)

            # logger.info(f"question asked: {expr_t}")
            answer = self.get_response(person.ask(expr_t.generate_expr()))
            # logger.info(f"{person}: {answer}")

            states = state_spread[answer]

            # logger.info("Remaining states:")
            # for state in states:
            # logger.info(state)

        if len(states) == 0:
            return

        for person, field in states[0].field_mapping:
            self.guess[person] = field
