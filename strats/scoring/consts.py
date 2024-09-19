"""
Constants
"""

import os
from enum import Enum

class PATH:
    SUBMISSION_FOLDER = "submissions"
    PUBLIC_FOLDER = os.path.join(SUBMISSION_FOLDER, "public")
    SCORE_JSON = os.path.join(PUBLIC_FOLDER, "scores.json")

    @classmethod
    def DIFFICULTY(cls, difficulty: str):
        return os.path.join(cls.PUBLIC_FOLDER, difficulty)

    @classmethod
    def SCOREBOARD(cls, difficulty: str):
        return os.path.join(cls.DIFFICULTY(difficulty), "README.md")

class KEYS:
    AUTHOR   = "author"
    ACCEPTED = "accepted_on"
    Q_LIMIT  = "question_limit"

    Q_AVG = "question_avg"
    CPLX = "complexity"

