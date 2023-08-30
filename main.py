import re
from re import Match
from os import listdir
from pathlib import PurePath

MAIN_DIR = PurePath(__file__).parent

files = next(file for file in listdir(MAIN_DIR) if PurePath(file).suffix == ".md")
pattern_most = r"(\d+.+-.+\d+.+\n(?:Idiom|idiom):.+)"  # not efficient
pattern_all = r"(\d+(?:.+|\s)(?:-|–).+\d+\n(?:Idiom|idiom):.+)"  # not efficient at all

with open(MAIN_DIR.joinpath("sample_text.md"), encoding="utf-8") as file:
    sample_text = file.read()


def add_surrounding_asterisk(match: Match):
    if match.group() is not None:
        return f"**{match.group()}**"


def replace_poster_with_empty(match: Match):
    if match.group() is not None:
        return match.group(2)


def bold_date_and_idiom():
    bolded = re.sub(
        pattern_all, add_surrounding_asterisk, sample_text, flags=re.IGNORECASE
    )
    # for match in matches:
    #     print(match.group(1))
    return bolded


def remove_english_learner_tag(bolded: str):
    pattern = r"@English\sLearners.+"
    remove_tag = re.sub(pattern, "", bolded, flags=re.IGNORECASE)
    return remove_tag


def remove_poster(removed_tag: str):
    pattern = r"(.+\s—\s.+)(\n={10,})"
    remove_poster = re.sub(
        pattern, replace_poster_with_empty, removed_tag, flags=re.IGNORECASE
    )
    return remove_poster


if __name__ == "__main__":
    bolded = bold_date_and_idiom()
    with open(MAIN_DIR.joinpath("BOLDED.md"), encoding="utf-8", mode="w") as file:
        file.write(bolded)
    removed_tag = remove_english_learner_tag(bolded)
    with open(MAIN_DIR.joinpath("REMOVED_TAG.md"), encoding="utf-8", mode="w") as file:
        file.write(removed_tag)
    removed_poster = remove_poster(removed_tag)
    with open(
        MAIN_DIR.joinpath("REMOVED_POSTER.md"), encoding="utf-8", mode="w"
    ) as file:
        file.write(removed_poster)
