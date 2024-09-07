from .game.manager import GameInstance
from .game import types

from time import sleep

class _StrategyBase:

    @classmethod
    def get_difficulty(cls) -> str:
        raise NotImplementedError
    
    @classmethod
    def get_question_limit(cls) -> int:
        if not hasattr(cls, "question_limit") or not isinstance(cls.question_limit, int) or cls.question_limit <= 0:
            raise NotImplementedError(f"Strategy must specify a positivevalue for `{cls.__name__}.question_limit`.")
        return cls.question_limit

    def __init__(self):
        features = ["test-strategy"]
        match self.get_difficulty():
            case "easy":
                features.append("easy")
            case "hard":
                features.append("hard")
            case "default":
                pass
            case other:
                raise ValueError(f"Unexpected difficulty: {other}")
        
        self._instance = GameInstance(features=features, num_questions=self.get_question_limit())
        self._guess: types.Guesses = None
    
    def solve(self):
        """
        This is the entrypoint for writing a solver
        """
        raise NotImplementedError(f"Strategy must define the function `{type(self).__name__}.solve(self)`.")
    
    def get_response(self, question: types.Question) -> types.Response:
        return self._instance.ask(question)
    
    @property
    def guess(self):
        return self._guess

    def single_case(self):
        self._instance._reset()
        self._guess = types.Guesses()
        if (ret := self.solve()) is not None:
            raise ValueError(f"Solver should not return anything, but returned {ret}.")
        self._instance.guess(**self._guess)
        return self._instance._question_counter
    
    def test_all_cases(self):
        question_count = 0
        case_count = 0
        while self._instance.is_running() and self._instance.ping():
            question_count += self.single_case()
            case_count += 1

        return question_count / case_count



class _DefaultStrategy(_StrategyBase):
    """
    Base class for strategies for the default game.
    """

    @classmethod
    def get_difficulty(cls) -> str:
        return "default"
    

class _EasyStrategy(_StrategyBase):
    """
    Base class for strategies for the easy game.
    """

    @classmethod
    def get_difficulty(cls) -> str:
        return "easy"

class _HardStrategy(_StrategyBase):
    """
    Base class for strategies for the hard game.
    """

    @classmethod
    def get_difficulty(cls) -> str:
        return "hard"