"""
Spawning and interacting with game instance
"""
import os
import asyncio
import re
import subprocess

from . import types, consts

def cargo_is_supported():
    try:
        return subprocess.run(["cargo", "--version"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, universal_newlines=True).returncode == 0
    except FileNotFoundError:
        return False

class GameInstance:

    def __init__(self, *, features: list = None, num_questions: int = None):

        if num_questions is None:
            raise ValueError("Number of questions must be specified!")
        
        self._num_questions = num_questions

        if not cargo_is_supported():
            raise RuntimeError("Please install cargo before running!")
        
        cargo_args = ["--release", "--quiet"]
        if features is not None:
            cargo_args.extend(["--features",  "{}".format(' '.join(features))])
        
        self._handle = subprocess.Popen(["cargo", "run", *cargo_args],
                                        stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=None)

        self._writeln(num_questions)

        self._reset()

        if (fname := os.environ.get("STRAT_LOG")) is not None:
            self._history = open(fname, 'w')
        else:
            self._history = None

    def _reset(self):
        self._question_counter = 0
        self._question_complexity = 0
        self._log("Resetting...")
        self._read_buffer = b""

    def __del__(self):
        if hasattr(self, "_handle") and self._handle.poll() is None:
            self._handle.terminate()
        if hasattr(self, "_history") and self._history is not None:
            self._history.close()

    def _writeln(self, line):
        self._handle.stdin.write(f"{line}\n".encode())
        self._handle.stdin.flush()

        if (ret := self._handle.poll()) is not None:
            if ret != 0:
                raise RuntimeError(f"Game instance terminated unexpectedly with exit code {ret}")
            else:
                print("Game instance terminated gracefully.")
                exit()

    def _readln(self):
        return self._handle.stdout.readline()

    def _log(self, line):
        if hasattr(self, "_history") and self._history is not None:
            self._history.write(f"{line}\n")
            self._history.flush()

    def is_running(self) -> bool:
        return self._handle.poll() is None

    def ping(self) -> bool:
        match self._readln().strip():
            case b"begin":
                return True
            case b"end":
                return False
            case _:
                print("Subprocess pingback failed. Exiting...")
                exit(99)


    def ask(self, question: types.Question) -> types.Response:
        if not isinstance(question, types.Question):
            raise ValueError("You can only ask questions!")

        if self._question_counter >= self._num_questions:
            raise AssertionError(f"You have already asked your limit of {self._num_questions} question(s)!")

        self._question_counter += 1
        val = len(re.findall(r"\b\S+?\b", str(question)))
        self._question_complexity += val

        self._writeln(question)
        self._log(f"You: {question}")

        match self._readln().strip():
            case b"Foo":
                ret = consts.Foo
            case b"Bar":
                ret = consts.Bar
            case b"Baz":
                ret = consts.Baz
            case other:
                raise ValueError(f"Received unexpected input: {other}.")

        self._log(f"Response: {ret}")
        return ret

    def guess(self, **guesses):
        self._writeln("done")
        self._log("Guesses:")

        for name in ["Alice", "Bob", "Charlie", "Dan"]:
            guess = guesses.get(name)
            if guess is None:
                break
            if not isinstance(guess, types.Field):
                raise TypeError(f"Expected a field for {name}, but received {guess}! ({type(guess).__name__})")
            self._writeln(guess)
            self._log(f"{name}: {guess}")

        self._writeln("end")