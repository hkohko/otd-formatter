import re
from os import listdir
from re import Match
from pathlib import PurePath, Path

MAIN_DIR = PurePath(__file__).parent
RAW = MAIN_DIR.joinpath("raw")
FORMATTED = MAIN_DIR.joinpath("formatted")
is_exist_raw = Path(RAW).exists()
is_exist_formatted = Path(FORMATTED).exists

if not is_exist_raw:
    Path(RAW).mkdir()
if not is_exist_formatted:
    Path(FORMATTED).mkdir()


def add_surrounding_asterisk(match: Match):
    if match.group() is not None:
        return f"**{match.group()}**"


def replace_poster_with_empty(match: Match):
    if match.group() is not None:
        return match.group(2)


def bold_date_and_idiom(text: str):
    pattern_all = r"(\d+(?:.+|\s)(?:-|–).+\d+.+?\n(?:Idiom|idiom|Word|word):.+)"
    bolded = re.sub(pattern_all, add_surrounding_asterisk, text, flags=re.IGNORECASE)
    return bolded


def remove_english_learner_tag(text: str):
    pattern = r"@English\sLearners.+"
    remove_tag = re.sub(pattern, "", text, flags=re.IGNORECASE)
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


def quote_otd_text(text: str):
    pattern = r"(.+—\s(?:\d+|\w+).+\d{1,2}\s(?:AM|PM)\n)"
    to_quote = re.sub(pattern, r"\g<1>> ", text, flags=re.IGNORECASE)
    return to_quote


def userinput():
    raw_files = listdir(RAW)
    entry = input("type the filename: ")
    for rawfile in raw_files:
        if entry.lower() in rawfile.lower():
            to_format = rawfile
    with open(RAW.joinpath(to_format), encoding="utf-8") as file:
        sample_text = file.read()
    return to_format, sample_text


def save(filename: str, to_write: str, save: bool = True):
    if save:
        with open(
            FORMATTED.joinpath(f"formatted_{filename}"),
            encoding="utf-8",
            mode="w",
        ) as file:
            file.write(to_write)


def main(text: str):
    removed_englearner_tag = remove_english_learner_tag(text)
    removed_poster = remove_poster(removed_englearner_tag)
    del_empty_lines = remove_empty_lines(removed_poster)
    add_nl_submitter = add_newline_between_submitter(del_empty_lines)
    add_nl_equals = add_newline_before_equals(add_nl_submitter)
    add_quote = quote_otd_text(add_nl_equals)
    bolded_date_idiom = bold_date_and_idiom(add_quote)
    return bolded_date_idiom


if __name__ == "__main__":
    if not is_exist_raw:
        print(f"created {RAW}")
    if not is_exist_formatted:
        print(f"created {FORMATTED}")
    filename, text = userinput()
    result = main(text)
    save(filename, result)
