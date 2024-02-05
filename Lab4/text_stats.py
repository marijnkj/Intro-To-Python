import sys
import numpy as np
import Counter

# for arg in sys.argv:
#     print(arg)

with open("Lab4\shakespeare.txt", encoding="utf-8") as file:
    f = file.read()
    f = f.replace("\n", " ").lower()
    
    # Count per alphabetic letter    
    letter_count = {letter: f.count(letter) for letter in "abcdefghijklmnopqrstuvwxyz"}    
    letter_count = sorted(letter_count.items(), key=lambda x: x[1], reverse=True)

    for letter, count in letter_count:
        print(f"Count of {letter}: {count}")

    # Word count
    word_list = f.split(" ")
    word_list = [word.rstrip(".").rstrip(")").lstrip("(") for word in word_list if word not in ["", " "] and not any(char.isdigit() for char in word)]
    print(f"Number of words: {len(word_list)}")

    # Number of unique words
    print(f"Number of unique words: {len(set(word_list))}")
    print(Counter(word_list))