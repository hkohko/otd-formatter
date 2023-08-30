import re
from re import Match
from pathlib import PurePath

MAIN_DIR = PurePath(__file__).parent

with open(MAIN_DIR.joinpath("sample_text.md"), encoding="utf-8") as file:
    sample_text = file.read()


def add_surrounding_asterisk(match: Match):
    if match.group() is not None:
        return f"**{match.group()}**"


def replace_poster_with_empty(match: Match):
    if match.group() is not None:
        return match.group(2)


def bold_date_and_idiom(text: str):
    pattern_all = r"(\d+(?:.+|\s)(?:-|–).+\d+\n(?:Idiom|idiom):.+)"
    bolded = re.sub(pattern_all, add_surrounding_asterisk, text, flags=re.IGNORECASE)
    return bolded


def remove_english_learner_tag():
    pattern = r"@English\sLearners.+"
    remove_tag = re.sub(pattern, "", sample_text, flags=re.IGNORECASE)
    return remove_tag


def remove_poster(text: str):
    pattern = r"(.+\s—\s.+)(\n={10,})"
    remove_poster = re.sub(
        pattern, replace_poster_with_empty, text, flags=re.IGNORECASE
    )
    return remove_poster


def remove_empty_lines(text: str):
    return text.replace("\n\n", "\n")


def add_newline_between_submitter(text: str):
    pattern = r"(.+—\s(?:\d+|\w+).+\d{1,2}\s(?:AM|PM))"
    add_nl = re.sub(pattern, r"\n\g<1>", text, flags=re.IGNORECASE)
    return add_nl


def add_newline_before_equals(text: str):
    pattern = r"(={10,})"
    add_nl = re.sub(pattern, r"\n\g<1>", text, flags=re.IGNORECASE)
    return add_nl

if __name__ == "__main__":
    removed_englearner_tag = remove_english_learner_tag()
    removed_poster = remove_poster(removed_englearner_tag)
    del_empty_lines = remove_empty_lines(removed_poster)
    add_nl_submitter = add_newline_between_submitter(del_empty_lines)
    add_nl_equals = add_newline_before_equals(add_nl_submitter)
    bolded_date_idiom = bold_date_and_idiom(add_nl_equals)
    with open(MAIN_DIR.joinpath("BOLDED.md"), encoding="utf-8", mode="w") as file:
        file.write(bolded_date_idiom)
