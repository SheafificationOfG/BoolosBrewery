"""
Strategy classes, used for interfacing with the Foobar game.

When deriving one of the strategy classes, you need to provide the following:
-   <strategy>.num_questions: the max number of questions you plan to ask
-   <strategy>.solve(): the entrypoint for the strategy.
"""
from ._backend import _DefaultStrategy, _EasyStrategy, _HardStrategy

class Default(_DefaultStrategy):
    pass

class Easy(_EasyStrategy):
    pass

class Hard(_HardStrategy):
    pass