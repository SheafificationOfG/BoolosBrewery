from .consts import PATH, KEYS

import json
import os

def _sortkey(table: dict[str, dict]):
    def score(strat: str):
        entry = table[strat]
        return (entry[KEYS.Q_AVG], entry[KEYS.CPLX], entry[KEYS.ACCEPTED])
    return score

def load_scores() -> dict[str, dict[str, dict]]:
    with open(PATH.SCORE_JSON, 'r') as score_json:
        return json.load(score_json)
    
def save_scores(scores: dict):
    with open(PATH.SCORE_JSON, 'w') as score_json:
        json.dump(scores, score_json, indent=2)

def update_scoreboard(difficulty: str, json: dict):
    scoreboard = PATH.SCOREBOARD(difficulty)
    os.makedirs(os.path.dirname(scoreboard), exist_ok=True)

    def sanitise(string: str) -> str:
        for old, new in [
            ('_', '\\_'),
            ('|', '\\|'),
        ]:
            string = string.replace(old, new)
        return string
    
    with open(scoreboard, 'w') as file:
        file.write(f"# High scores for the \"{difficulty}\" variant\n\n")
        table = json[difficulty]

        file.write("| Place | Strategy | Author | Questions | Complexity | Source |\n")
        file.write("|:-----:|:--------:|:------:|:---------:|:----------:|:------:|\n")

        for index, submission in enumerate(sorted(table, key=_sortkey(table))):

            place = {
                0: ":1st_place_medal:",
                1: ":2nd_place_medal:",
                2: ":3rd_place_medal:"
            }.get(index, f"{index+1}")
            entry = table[submission]

            strategy = "`{}`".format(os.path.splitext(os.path.split(submission)[1])[0].split('_', 2)[-1])
            author = sanitise(entry[KEYS.AUTHOR])
            if index < 3:
                author = f"**{author}**"
            questions = f"{entry[KEYS.Q_AVG]:.5f}"
            complexity = f"{entry[KEYS.CPLX]:,}"
            fname = os.path.relpath(submission, PATH.DIFFICULTY(difficulty))
            source = f"`{fname}`"

            file.write(f"| {place} | {strategy} | {author} | {questions} | {complexity} | {source} |\n")

def summary(fname: str, difficulty: str, questions: float, complexity: int, comment: str):
    if fname is None:
        return
    
    with open(fname, 'a') as file:
        file.write("## Summary\n")
        file.write("| Difficulty | Questions | Complexity | Comments |\n")
        file.write("|:----------:|:---------:|:----------:|:--------:|\n")
        file.write(f"| {difficulty} | {questions:.5f} | {complexity:,} | {comment} |\n\n")

def exception(fname: str, exc: Exception):
    if fname is None:
        return
    
    with open(fname, 'a') as file:
        file.write("## Error\n")
        file.write("| Error | Message |\n")
        file.write("|:-----:|:-------:|\n")
        file.write(f"| {type(exc).__name__} | {exc} |\n\n")