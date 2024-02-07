import sys
from collections import Counter
import text_stats as ts


def get_following_probs(f, word):
    """
    Takes a read text file and returns a dictionary of the most frequent words with the probablity of subsequent words
    """
    word_list = ts.get_word_list(f)    
    
    following_word_ind = [ind + 1 for ind, this_word in enumerate(word_list) if this_word == word]
    following_word_counts = dict(Counter([word_list[ind] for ind in following_word_ind if ind < len(word_list)]))
    following_word_props = {word: count / sum(following_word_counts.values()) for word, count in following_word_counts.items()}
    following_word_props = sorted(following_word_props.items(), key=lambda x: x[1], reverse=True)
    

    return following_word_props[0][0]


if __name__ == "__main__":
    args = sys.argv

    if len(args) != 4:
        raise Exception("Three variables must be passed! A file to open, a starting word, and the max number of words")
    
    if not args[1].endswith(".txt"):
        raise Exception("The first argument passed must be a text file.")
    
    if not isinstance(args[2], str) or not isinstance(args[3], int):
        raise Exception("The starting word must be a string and the max number of words an integer")
    
    file_name = args[1]
    starting_word = args[2]
    max_words = args[3]
    stop = 0

    word_list = [starting_word]
    with open(file_name, encoding="utf-8") as file:
        f = file.read()

        while not stop:
            word_list.append(get_following_probs(f, word_list[-1]))
            
            if len(word_list) == max_words:
                stop = 1

    print(" ".join(word_list))
