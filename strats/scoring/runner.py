"""
Script for running a test submission
"""

import strats
from .consts import KEYS
from .complexity import score as complexity_score

import importlib
import os
import sys

class Submission:

    def __init__(self, path: str):
        self._fullpath = path.replace(os.path.sep, '/')
        self._strat_path, self._strat_file = os.path.split(path)
        self._strat_file, _ = os.path.splitext(self._strat_file)

        _syspath = list(sys.path)
        sys.path.insert(0, self._strat_path)
        self._module = importlib.import_module(self._strat_file)
        sys.path.clear()
        sys.path.extend(_syspath)

        if not hasattr(self._module, "Strategy"):
            raise AttributeError(f"{self._strat_file} must define a \"Strategy\" class.")
        
        self._strategy: strats.Easy | strats.Default | strats.Hard = self._module.Strategy()
        if not isinstance(self._strategy, (strats.Easy, strats.Default, strats.Hard)):
            raise TypeError(f"{self._strategy.__qualname__} must derive from strats.Easy, strats.Default, or strats.Hard.")
    
    def load_from_json(self, json: dict):
        table: dict[str, dict] = json[self.get_difficulty()]

        if (entry := table.get(self._fullpath)) is None:
            return
        
        if (q_avg := entry.get(KEYS.Q_AVG)) is not None:
            self._q_avg: float = q_avg
        
        if (cplx := entry.get(KEYS.CPLX)) is not None:
            self._cplx: int = cplx

    def write_to_json(self, json: dict, *, path=None, author=None, accepted=None, recompute_q_avg=False, recompute_cplx=False):

        table: dict[str, dict] = json.setdefault(self.get_difficulty(), {})

        if path is None:
            path = self._fullpath

        entry = table.setdefault(path, {})

        if author is not None:
            entry[KEYS.AUTHOR] = author
        if accepted is not None:
            entry[KEYS.ACCEPTED] = accepted
        
        entry[KEYS.Q_LIMIT] = self.get_question_limit()
        entry[KEYS.Q_AVG] = self.get_question_average(recompute=recompute_q_avg)
        entry[KEYS.CPLX] = self.get_complexity(recompute=recompute_cplx)


    def get_difficulty(self) -> str:
        return self._strategy.get_difficulty()
    
    def get_question_limit(self) -> int:
        return self._strategy.get_question_limit()
    
    def get_question_average(self, *, recompute=False) -> float:
        if recompute or not hasattr(self, "_q_avg"):
            print("Running strategy...")
            self._q_avg = self._strategy.test_all_cases()

            print("All scenarios passed!")
            print("Average number of questions needed:", self._q_avg)

        return self._q_avg
    
    def get_complexity(self, *, recompute=False) -> int:
        if recompute or not hasattr(self, "_cplx"):
            with open(self._fullpath) as file:
                src = file.read()
            self._cplx = complexity_score(src)
        return self._cplx
