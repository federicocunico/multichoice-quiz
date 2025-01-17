import argparse
import os
from generate_quizfile import generate_from_file
from quizgame import Colors, Quiz

myquiz = Quiz()
myquiz.clear()
print(Colors.blue(myquiz.BANNER))
print("")
parser = argparse.ArgumentParser(formatter_class=argparse.MetavarTypeHelpFormatter)
parser.add_argument("quiz_text_file", type=str, help="Path of the TXT file with questions")
parser.add_argument(
    "--t",
    nargs="?",
    type=int,
    help="THRESHOLD for passing the quiz in percent (rounded). Show success or failure message at the end.",
)
parser.add_argument(
    "--l",
    nargs="?",
    type=int,
    help="LIMIT the number of questions in a quiz. No effect if number of available question less then limit.",
)
parser.add_argument(
    "--randomize", action="store_true", help="randomize the order of questions"
)
parser.add_argument("-i", action="store_true", help="print available quizzes and exit")
# parser.print_help()
args = parser.parse_args()
if args.i:
    print(myquiz.listGames())
    exit()
else:
    os.makedirs("quizzes", exist_ok=True)
    # expecting quizname a file name
    assert os.path.isfile(args.quiz_text_file), f"File {args.quiz_text_file} not found"
    dst = os.path.join(
        "quizzes", os.path.basename(args.quiz_text_file).replace(".txt", ".json")
    )
    generate_from_file(args.quiz_text_file, dst=dst, verbose=False)
    args.quizname = os.path.basename(dst).replace(".json", "")

    myquiz.playQuiz(args)
