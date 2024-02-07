import sys
import numpy as np
from collections import Counter


def prep_text(f):
    f = f.replace("\n", " ").replace("\t", " ").replace(
        "_", "").replace("--", " ").lower()

    return f


def get_letter_count(f):
    """
    Takes a read text file and returns an ordered list of tuples containing each alphabetic letter and its count in the text
    """
    # Make sure all letters are lowercase and that there aren't any newlines or tabs
    f = prep_text(f)

    # Count per alphabetic letter
    letter_count = {letter: f.count(letter)
                    for letter in "abcdefghijklmnopqrstuvwxyz"}
    letter_count = sorted(letter_count.items(),
                          key=lambda x: x[1], reverse=True)

    return letter_count


def get_word_list(f):
    """
    Takes a read text file and returns a list of all words. A word does not contain numerical characters, quotation marks, or punctuation marks
    """
    # Make sure all letters are lowercase and that there aren't any newlines or tabs
    f = prep_text(f)

    # Word count
    word_list = f.split(" ")
    word_list = [word.replace("”", "").replace("“", "").rstrip("'").lstrip("'").rstrip(":").rstrip(";").rstrip("!").rstrip("?").rstrip(
        ")").lstrip("(").rstrip(".").rstrip(",") for word in word_list if word not in ["", " "] and not any(char.isdigit() for char in word)]

    return word_list


def get_word_counts(f):
    """
    Takes a read text file and returns the number of words and number of unique words in the file
    """
    word_list = get_word_list(f)

    return len(word_list), len(set(word_list))


def get_most_frequent_words(f):
    """
    Takes a read text file and returns a dictionary of the most frequent words with their most frequent subsequent words
    """
    word_list = get_word_list(f)

    word_counts = dict(Counter(word_list))
    word_counts = sorted(word_counts.items(),
                         key=lambda x: x[1], reverse=True)[:5]

    following_word_counts = {}
    for this_word, this_count in word_counts:
        following_this_word_ind = [
            ind + 1 for ind, word in enumerate(word_list) if word == this_word]
        following_this_word_counts = dict(
            Counter([word_list[ind] for ind in following_this_word_ind]))
        following_this_word_counts = sorted(
            following_this_word_counts.items(), key=lambda x: x[1], reverse=True)[:3]

        following_word_counts[this_word] = (
            this_count, following_this_word_counts)

    return following_word_counts


def text_summary(f, file=None):
    """
    Takes a read text file and prints all the summary stats
    """
    if file is not None:
        file = open(file, "a")

    letter_count = get_letter_count(f)  # Count per alphabetic letter
    for letter, count in letter_count:
        print(f"Count of {letter}: {count}", file=file)

    n_words, n_unique_words = get_word_counts(f)  # Word count
    print(f"Number of words: {n_words}\nNumber of unique words: {
          n_unique_words}", file=file)

    following_word_counts = get_most_frequent_words(f)
    for word, info in following_word_counts.items():
        print(f"{word} ({info[0]} occurences)", file=file)

        for following_word, count in info[1]:
            print(f"--{following_word}, {count}", file=file)


if __name__ == "__main__":
    args = sys.argv

    print(args)

    if len(args) > 2:
        raise Exception("You may only pass at most two arguments")
    elif len(args) < 1:
        raise Exception("You must pass at least one file to read")

    if not args[1].endswith(".txt"):
        raise Exception("The first argument passed must be a text file.")

    if len(args) == 3:
        if not args[2].endswith(".txt"):
            raise Exception("File to save to must be a text file!")

        write_bool = 1
    else:
        write_bool = 0

    with open(args[1], encoding="utf-8") as file:
        f = file.read()

        if write_bool:
            text_summary(f, file=args[2])
        else:
            text_summary(f)
