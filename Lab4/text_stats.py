import sys
import numpy as np
from collections import Counter
import json

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
    word_list = [word.replace("”", "").replace("“", "").rstrip("]").lstrip("[").rstrip("'").lstrip("'").rstrip(":").rstrip(";").rstrip("!").rstrip("?").rstrip(
        ")").lstrip("(").rstrip(".").rstrip(",") for word in word_list if word not in ["", " "] and not any(char.isdigit() for char in word)]

    return word_list


def get_word_counts(f):
    """
    Takes a read text file and returns the number of words and number of unique words in the file
    """
    word_list = get_word_list(f)

    return len(word_list), len(set(word_list))


def get_most_frequent_words(f, dict_f, chosen_word=None, top5=True):
    """
    Takes a read text file and returns a dictionary of the most frequent words with their most frequent subsequent words
    """
    word_list = get_word_list(f)

    word_counts = dict(Counter(word_list))
    word_counts = sorted(word_counts.items(), key=lambda x: x[1], reverse=True)
    
    # Only compute following words for five most frequent words
    if top5:
        word_counts = word_counts[:5]
    # Only compute following words for chosen word
    elif chosen_word is not None:
        word_counts = [(word, count) for word, count in word_counts if word == chosen_word]
    
    following_word_counts = {}
    for this_word, this_count in word_counts:
        # Get following word counts
        following_this_word_ind = [
            ind + 1 for ind, word in enumerate(word_list) if word == this_word]
        following_this_word_counts = dict(Counter(
            [word_list[ind] for ind in following_this_word_ind if ind < len(word_list)]))
        following_this_word_counts = sorted(
            following_this_word_counts.items(), key=lambda x: x[1], reverse=True)

        following_word_counts[this_word] = (
            this_count, following_this_word_counts)
        
        # Add to following_word_counts.json if not already added
        if this_word not in dict_f.keys():
            dict_f[this_word] = (this_count, following_this_word_counts)

    return following_word_counts, dict_f


def get_following_word_probs(f, dict_f, word):
    if word in dict_f.keys():
        following_this_word_counts = dict_f[word][1]
    else:
        following_word_counts, dict_f = get_most_frequent_words(f, dict_f, word, top5=False)
        following_this_word_counts= following_word_counts[word][1]

    n_words_following_this_word = sum([this_count for this_word, this_count in following_this_word_counts])
    words_following_this_word = [this_word for this_word, this_count in following_this_word_counts]
    probs_following_this_word = [this_count / n_words_following_this_word for this_word, this_count in following_this_word_counts]

    return words_following_this_word, probs_following_this_word


def get(word):
    dict_f = open("following_word_counts.json")
    following_word_counts = json.load(dict_f)

    print(following_word_counts[word])


def text_summary(f, dict_f, output_file=None):
    """
    Takes a read text file and prints all the summary stats
    """
    if output_file is not None:
        output_file = open(output_file, "a")

    letter_count = get_letter_count(f)  # Count per alphabetic letter
    for letter, count in letter_count:
        print(f"Count of {letter}: {count}", file=output_file)

    n_words, n_unique_words = get_word_counts(f)  # Word count
    print(f"Number of words: {n_words}\nNumber of unique words: {n_unique_words}", file=output_file)

    following_word_counts, dict_f = get_most_frequent_words(f, dict_f)
    following_word_counts = {
        word: (following_word_counts[word][0], following_word_counts[word][1][:3]) for word in list(following_word_counts)}
    for word, info in following_word_counts.items():
        print(f"{word} ({info[0]} occurences)", file=output_file)

        for following_word, count in info[1]:
            print(f"--{following_word}, {count}", file=output_file)

    try:
        output_file.close()
    except:
        pass


if __name__ == "__main__":
    args = sys.argv
    write_bool = 0

    if len(args) > 3:
        raise Exception("You may only pass at most two arguments")
    elif len(args) < 2:
        raise Exception("You must pass at least one file to read")
    if not args[1].endswith(".txt"):
        raise Exception("The first argument passed must be a text file.")
    if len(args) == 3:
        if not args[2].endswith(".txt"):
            raise Exception("File to save to must be a text file!")

        write_bool = 1

    # Error message if file does not exist
    try:
        f = open(args[1])
        f.close()
    except FileNotFoundError:
        raise Exception("ERROR: This file does not exist!")

    with open(args[1], encoding="utf-8") as file:
        f = file.read()

        # Open following_word_counts.json 
        following_words_file = open("following_word_counts.json", "r+")
        dict_f = json.load(following_words_file)

        if write_bool:
            text_summary(f, dict_f, output_file=args[2])
        else:
            text_summary(f, dict_f)

        # Save updated following_word_counts.json
        following_words_file.seek(0)
        json.dump(dict_f, following_words_file)
        following_words_file.close()


file = open(r"C:\Users\marij\Documents\GitHub\Intro-To-Python\Lab4\shakespeare.txt", encoding="utf-8")
f = file.read()

# file.close()