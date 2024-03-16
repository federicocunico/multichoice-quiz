import argparse
import json
import os
from pprint import pprint

quiz = {
    "meta": {
        "title": "",
        "author": "",
        "licence": "",
        "homepage": "",
        "contributors": [],
    },
    "quiz": {},
}


def generate_from_file(textfile: str, dst: str, verbose: bool = True) -> None:
    assert os.path.exists(textfile), "The file does not exist"

    # dst = f"quizzes/{os.path.basename(textfile).split('.')[0]}.json"
    question_id = 0

    with open(textfile, "r", encoding="utf-8") as f:
        lines = f.readlines()
        lines = [line.strip() for line in lines]

    current_section = "default"
    current_question = {}
    start = 0
    _lock = False
    # parse sections
    max_lines = len(lines)
    for i, line in enumerate(lines):
        if line.startswith("#"):
            current_section = line[1:]
            current_section = current_section.strip()
            quiz["quiz"][current_section] = {}
            _lock = False
        else:
            if line == "" or i == max_lines - 1:
                final = i if i != max_lines - 1 else i + 1
                q = parse(lines[start:final])
                quiz["quiz"][current_section][question_id] = q
                question_id += 1
                _lock = False
            else:
                if not _lock:
                    start = i
                    _lock = True
    assert not _lock, "The last question is not properly formatted"

    with open(dst, "w", encoding="utf-8") as fp:
        json.dump(quiz, fp=fp, indent=4, ensure_ascii=False)
    if verbose: pprint(quiz)
    print(f"Quiz generated in {dst}")


def parse(lines):
    def _get_letter(i):
        return chr(ord("A") + i)

    question = lines[0]
    answers = lines[1:]
    right = []
    for i, a in enumerate(answers):
        if a.startswith("*"):
            right.append(_get_letter(i))
    answers = [a.replace("*", "") for a in answers]
    if len(right) == 0:
        raise ValueError(f"No right answer provided for the question {question}")
    # remove every space at the beginning of the lines
    answers = [a.strip() for a in answers]
    return {
        "question": question,
        "answers": {_get_letter(i): a for i, a in enumerate(answers)},
        "right": right,
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate a quiz file")
    parser.add_argument("textfile", type=str, help="The name of the quiz file")
    args = parser.parse_args()
    textfile = args.textfile
    dst = os.path.basename(textfile).split(".")[0]
    generate_from_file(textfile, dst=f"quizzes/{dst}.json")
