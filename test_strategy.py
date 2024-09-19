"""
Script for automatically testing user-implemented strategies.
"""

import strats.scoring as scoring

import argparse
import datetime
import glob
import os

def find_submission(file: str|None):
    submissions = glob.glob(f"{scoring.consts.PATH.SUBMISSION_FOLDER}/*.py") if file is None else [file]
    if len(submissions) != 1:
        print(f"Submission should consist of exactly one strategy file, but I found {len(submissions)}.")
        print(f"Make sure your submitted strategy is in the \"{scoring.consts.PATH.SUBMISSION_FOLDER}\" folder!")
        exit(99)
    if not os.path.exists(submissions[0]):
        print(f"{submissions[0]} does not exist!")
        exit(3)
    
    return submissions[0]

def publish_submission(difficulty: str, submission: str, date: str):
    _, file = os.path.split(submission)
    file = f"{date}_{file}"
    public = os.path.join(scoring.consts.PATH.DIFFICULTY(difficulty), file)
    assert(not os.path.exists(public))
    os.rename(submission, public)
    return public



def process_single_submission(file: str|None, publish=False, author=None, summary=None):
    submission_file = find_submission(file)
    
    print(f"Importing {submission_file}")
    submission = scoring.runner.Submission(submission_file)

    print("Puzzle variant:", submission.get_difficulty())
    print("Question limit:", submission.get_question_limit())

    print("Running submission...")
    q_avg = submission.get_question_average()
    cplx = submission.get_complexity()
    scoring.scoreboard.summary(summary, submission.get_difficulty(), q_avg, cplx, f"Question limit: {submission.get_question_limit()}")

    print("Submission passed all test cases!")
    print("Average question count:", q_avg)
    print("Solution complexity:", cplx)

    if publish:
        if author is None:
            raise RuntimeError("Submissions require an author to be published!")
        
        difficulty = submission.get_difficulty()
        date = datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%d_%H%M%S")
        public = publish_submission(difficulty, submission_file, date)

        scores = scoring.scoreboard.load_scores()
        submission.write_to_json(
            scores,
            path = public,
            author = author,
            accepted = date,
        )
        scoring.scoreboard.update_scoreboard(difficulty, scores)
        scoring.scoreboard.save_scores(scores)

def recompute_scoreboards(q_avg=False, cplx=False):
    scores = scoring.scoreboard.load_scores()

    for difficulty, table in scores.items():
        for submission_file in table:
            submission = scoring.runner.Submission(submission_file)
            submission.load_from_json(scores)
            submission.write_to_json(scores, recompute_q_avg=q_avg, recompute_cplx=cplx)

        scoring.scoreboard.update_scoreboard(difficulty, scores)

    scoring.scoreboard.save_scores(scores)

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Automated strategy test and publish.")
    parser.add_argument("--author", type=str, metavar="NAME", dest="author",
                        help="Pass author info; only relevant if pushing score.")
    parser.add_argument("--file", type=str, metavar="STRATEGY", dest="file",
                        help=f"Point to a specific strategy file. Otherwise, the strategy in the {scoring.consts.PATH.SUBMISSION_FOLDER} is used.")
    parser.add_argument("--catch-errors", action="store_true", dest="catch_errors",
                        help="Suppress error output and exit with nonzero exit code.")
    parser.add_argument("--publish", action="store_true", dest="publish",
                        help=f"Move submission to {scoring.consts.PATH.PUBLIC_FOLDER} and update scoreboard.\n"
                              "If you are not the handsome GSheaf, this argument doesn't apply to you!")
    parser.add_argument("--summary", type=str, metavar="FILE", dest="summary_file",
                        help="Write summary info to a file.")
    parser.add_argument("--refresh", action="store_true", dest="refresh",
                        help="Refresh scoreboards and exit; does not run tests.")
    parser.add_argument("--recompute-q-avg", action="store_true", dest="q_avg",
                        help="Recompute the average number of questions for all submissions. Implies `--refresh`.")
    parser.add_argument("--recompute-cplx", action="store_true", dest="cplx",
                        help="Recompute the complexity for all submissions. Implies `--refresh`.")
    
    args = parser.parse_args()

    if args.refresh or args.q_avg or args.cplx:
        recompute_scoreboards(args.q_avg, args.cplx)
        exit()
    
    try:
        process_single_submission(args.file, args.publish, args.author, args.summary_file)
    except Exception as exc:
        scoring.scoreboard.exception(args.summary_file, exc)
        if not args.catch_errors:
            raise
        exit(127)
