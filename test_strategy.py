"""
Script for automatically testing user-implemented strategies for the Foobar puzzle.
"""

import strats

import argparse
import datetime
import glob
import importlib
import json
import os
import sys

SUBMISSION_FOLDER = "submissions"
PUBLIC_FOLDER = os.path.join(SUBMISSION_FOLDER, "public")

SCORE_JSON = os.path.join(PUBLIC_FOLDER, "scores.json")

AUTHOR = "author"
ACCEPTED = "accepted_on"
Q_LIMIT = "question_limit"
Q_AVG = "question_avg"

def find_submission(file):
    submissions = glob.glob(f"{SUBMISSION_FOLDER}/*.py") if file is None else [file]
    if len(submissions) != 1:
        print(f"Submission should consist of exactly one strategy file, but I found {len(submissions)}.")
        print(f"Make sure your submitted strategy is in the \"{SUBMISSION_FOLDER}\" folder!")
        exit(99)
    if not os.path.exists(submissions[0]):
        print(f"{submissions[0]} does not exist!")
        exit(3)
    
    return submissions[0]

def publish_submission(difficulty: str, submission: str, date: str):
    _, file = os.path.split(submission)
    file = f"{date}.{file}"
    public = os.path.join(PUBLIC_FOLDER, difficulty, file)
    assert(not os.path.exists(public))
    os.rename(submission, public)
    return public

def summary(fname, difficulty, score, comment):
    if fname is None:
        return
    with open(fname, 'a') as file:
        file.write("| Difficulty | Score | Comments |\n")
        file.write("|:----------:|:-----:|:-------- |\n")
        file.write(f"| {difficulty} | {score} | {comment}\n")


def update_scoreboard(difficulty: str, json: dict):
    scoreboard = os.path.join(PUBLIC_FOLDER, difficulty, "README.md")
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

        file.write("| Place | Strategy | Author | Score | Date | Source |\n")
        file.write("|:-----:|:--------:|:------:|:-----:|:----:|:------ |\n")

        for index, submission in enumerate(sorted(table, key=lambda s: (table[s][Q_AVG], table[s][ACCEPTED]))):
            
            place = f"{index+1}." if index > 0 else ":trophy:"
            author = sanitise(table[submission][AUTHOR])
            name = "`{}`".format(os.path.splitext(os.path.split(submission)[1])[0].split('.', 2)[-1])
            if index < 3:
                author = f"**{author}**"
            score = f"{table[submission][Q_AVG]:.5f}"
            date = table[submission][ACCEPTED].split('.', 1)[0]
            fname = os.path.relpath(submission, os.path.join(PUBLIC_FOLDER, difficulty))
            source = f"`{fname}`"

            file.write(f"| {place} | {name} | {author} | {score} | {date} | {source} |\n")

def refresh_scoreboards():
    with open(SCORE_JSON, 'r') as score_json:
        scores = json.load(score_json)
    for difficulty in ["easy", "default", "hard"]:
        update_scoreboard(difficulty, scores)

if __name__ == "__main__" and not sys.flags.interactive:

    parser = argparse.ArgumentParser(description="Automated strategy test and publish.")
    parser.add_argument("--author", type=str, metavar="NAME", dest="author",
                        help="Pass author info; only relevant if pushing score.")
    parser.add_argument("--file", type=str, metavar="STRATEGY", dest="file",
                        help=f"Point to a specific strategy file. Otherwise, the strategy in the {SUBMISSION_FOLDER} is used.")
    parser.add_argument("--catch-errors", action="store_true", dest="catch_errors",
                        help="Suppress error output and exit with nonzero exit code.")
    parser.add_argument("--publish", action="store_true", dest="publish",
                        help=f"Move submission to {PUBLIC_FOLDER} and update scoreboard.\n"
                              "DO NOT ENABLE if you are just testing your submission!")
    parser.add_argument("--summary", type=str, metavar="FILE", dest="summary_file",
                        help="Write summary info to a file.")


    args = parser.parse_args()

    submission = find_submission(args.file)

    strat_path, strat_file = os.path.split(submission)
    strat_file, _ = os.path.splitext(strat_file)

    sys.path.insert(0, strat_path)

    print(f"Importing \"{strat_file}\" from {strat_path}...")
    strat = importlib.import_module(strat_file)

    print("Initialising strategy...")
    if not hasattr(strat, "Strategy") or not issubclass(strat.Strategy, (strats.Easy, strats.Default, strats.Hard)):
        print(f"Failed to locate \"Strategy\" class deriving from strats.{{Easy, Default, Hard}}.")
        exit(11)
    
    strategy = strat.Strategy()
    difficulty = strategy.get_difficulty()
    question_limit = strategy.get_question_limit()
    print("Puzzle variant:", difficulty)
    print("Question limit:", question_limit)

    print("Running strategy...")
    try:
        avg_question_num = strategy.test_all_cases()
    except Exception as exc:
        if not args.catch_errors:
            raise
        summary(args.summary_file, difficulty, type(exc).__name__, f"{exc}")
        exit(127)

    print("All puzzle scenarios passed!")
    print("Average number of questions needed:", avg_question_num)
    summary(args.summary_file, difficulty, avg_question_num, f"Question limit: {question_limit}")

    if not args.publish:
        exit(0)
    
    date = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d.%H-%M-%S")
    public = publish_submission(difficulty, submission, date)
    
    author = args.author
    if author is None:
        author = strat_file

    print(f"Adding {author}'s strategy to {SCORE_JSON} as {public}...")

    with open(SCORE_JSON, 'r') as score_json:
        scores = json.load(score_json)

    table = scores[difficulty]
    
    table[public] = {
        AUTHOR: author,
        ACCEPTED: date,
        Q_LIMIT: question_limit,
        Q_AVG: avg_question_num,
    }

    with open(SCORE_JSON, 'w') as score_json:
        json.dump(scores, score_json, indent=2)

    print("Updating score board...")
    update_scoreboard(difficulty, scores)