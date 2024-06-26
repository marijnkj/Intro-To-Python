import sys
import numpy as np
import text_stats as ts
import json


if __name__ == "__main__":
    args = sys.argv

    if len(args) != 4:
        raise Exception("ERROR: Three variables must be passed! A file to open, a starting word, and the max number of words")
    
    if not args[1].endswith(".txt"):
        raise Exception("ERROR: The first argument passed must be a text file.")
    
    if not isinstance(args[2], str):
        raise Exception("ERROR: The starting word must be a string and the max number of words an integer")
    
    file_name = args[1]
    starting_word = args[2]
    max_words = int(args[3])
    stop = 0

    word_list = [starting_word]

    # Error message if file does not exist
    try:
        f = open(file_name)
        f.close()
    except FileNotFoundError:
        print("ERROR: This file does not exist!")

    with open(file_name, encoding="utf-8") as file:
        f = file.read()
        
        # Open following_word_counts.json 
        following_words_file = open("following_word_counts.json", "r+")
        dict_f = json.load(following_words_file)

        while not stop:
            print(word_list[-1])
            words_following_this_word, probs_following_this_word = ts.get_following_word_probs(f, dict_f, word_list[-1])
            word_list.append(np.random.choice(words_following_this_word, p=probs_following_this_word))
            
            if len(word_list) == max_words:
                stop = 1

        # Save updated following_word_counts.json
        following_words_file.seek(0)
        json.dump(dict_f, following_words_file)
        following_words_file.close()

    print(" ".join(word_list))
