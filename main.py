import re
from re import Match
from os import listdir
from pathlib import PurePath

MAIN_DIR = PurePath(__file__).parent

files = next(file for file in listdir(MAIN_DIR) if PurePath(file).suffix == ".md")
pattern_most = r"(\d+.+-.+\d+.+\n(?:Idiom|idiom):.+)"  # not efficient
pattern_all = r"(\d+(?:.+|\s)(?:-|–).+\d+\n(?:Idiom|idiom):.+)"  # not efficient at all

with open(MAIN_DIR.joinpath(files), encoding="utf-8") as file:
    sample_text = file.read()


def add_surrounding_asterisk(match: Match):
    if match.group() is not None:
        return f"**{match.group()}**"


def bold_date_and_idiom():
    matches = re.sub(
        pattern_all, add_surrounding_asterisk, sample_text, flags=re.IGNORECASE
    )
    # for match in matches:
    #     print(match.group(1))
    print(matches)


def remove_english_learner_tag():
    ...
