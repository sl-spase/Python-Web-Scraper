import math
import re
import argparse


def syllables_counter(str_):
    list_of_words = str_.split(" ")
    syllables = 0
    polysyllables = 0
    vowels = ["a", "e", "i", "o", "u", "y"]
    for word in list_of_words:
        word = word.lower()
        # print(word)
        if word[-1].isalpha() and word[-1] == "e":
            word = word[0:-1]
        elif len(word) > 2 and not word[-1].isalpha() and word[-2] == "e":
            word = word[0:-2]
        is_prev_vowel = False
        temp_syllables = 0
        for char in word:
            if char in vowels and is_prev_vowel is False:
                is_prev_vowel = True
                temp_syllables += 1
            elif char not in vowels:
                is_prev_vowel = False
        if temp_syllables == 0:
            syllables += 1
        if temp_syllables > 2:
            polysyllables += 1
        syllables += temp_syllables
    return str(syllables) + " " + str(polysyllables)


def probability_based_scores_counter(score_):
    if score_ <= 4.9:
        return "10"
    elif score_ <= 5.9:
        return "12"
    elif score_ <= 6.9:
        return "14"
    elif score_ < 7.9:
        return "16"
    elif score_ <= 8.9:
        return "18"
    elif score_ <= 9.9:
        return "24"
    else:
        return "25"


def scores_counter(score_):
    if score_ <= 1:
        return "5"
    elif score_ <= 2:
        return "7"
    elif score_ <= 3:
        return "7"
    elif score_ <= 4:
        return "9"
    elif score_ <= 5:
        return "10"
    elif score_ <= 6:
        return "11"
    elif score_ <= 7:
        return "12"
    elif score_ <= 8:
        return "13"
    elif score_ <= 9:
        return "14"
    elif score_ <= 10:
        return "15"
    elif score_ <= 11:
        return "16"
    elif score_ <= 12:
        return "17"
    elif score_ <= 13:
        return "18"
    else:
        return "25"


def char_counter(str_):
    list_ = str_.split(" ")
    total_chars = 0
    for i in list_:
        total_chars += len(i)
    return total_chars


def ARI(chars_, words_counter_, sentences_counter_):
    return 4.71 * (chars_ / words_counter_) + 0.5 * (words_counter_ / sentences_counter_) - 21.43


def FK(words_counter_, sentences_counter_, syllables_):
    return 0.39 * (words_counter_ / sentences_counter_) + 11.8 * (syllables_ / words_counter_) - 15.59


def SMOG(polysyllables_, sentences_counter_):
    return 1.043 * math.sqrt((polysyllables_ * 30) / sentences_counter_) + 3.1291


def CL(chars_, words_counter_, sentences_counter_):
    return 5.89 * (chars_ / words_counter_) - 30 * (sentences_counter_ / words_counter_) - 15.8


def probability_based(diff_words_counter_, words_counter_, sentences_counter_):
    return 0.1579 * (diff_words_counter_ / words_counter_) * 100 + 0.0496 * (words_counter_ / sentences_counter_)


def metrics(ari_=False, fk_=False, smog_=False, cl_=False, pb_=False, all_=False):
    if all_:
        ari_ = True
        fk_ = True
        smog_ = True
        cl_ = True
        pb_ = True
    ages = 0
    if ari_:
        score_ = ARI(chars, words_counter, sentences_counter)
        age = scores_counter(score_)
        ages += int(age)
        print(f"Automated Readability Index: {round(score_, 2)} (about {age}-year-olds).")
    if fk_:
        score_ = FK(words_counter, sentences_counter, int(syllables))
        age = scores_counter(score_)
        ages += int(age)
        print(f"Flesch–Kincaid readability tests: {round(score_, 2)} (about {age}-year-olds).")
    if smog_:
        score_ = SMOG(int(polysyllables), sentences_counter)
        age = scores_counter(score_)
        ages += int(age)
        print(f"Simple Measure of Gobbledygook: {round(score_, 2)} (about {age}-year-olds).")
    if cl_:
        score_ = CL(chars, words_counter, sentences_counter)
        age = scores_counter(score_)
        ages += int(age)
        print(f"Coleman–Liau index: {round(score_, 2)} (about {age}-year-olds).")
    if pb_:
        score_ = 3.6365 if percentage_of_diff_word() > 5 else 0
        score_ += probability_based(diff_words_counter, words_counter, sentences_counter)
        age = probability_based_scores_counter(score_)
        ages += int(age)
        print(f"Probability-based score: {round(score_, 2)} (about {age}-year-olds)")

    if all_:
        print()
        print(f"This text should be understood in average by {ages / 5}-year-olds.")


def percentage_of_diff_word():
    return words_counter * (diff_words_counter / 100)


parser = argparse.ArgumentParser()
parser.add_argument("--infile")
parser.add_argument("--words")
args = parser.parse_args()
file = open(args.infile, "r")

diff_words = []
with open(args.words, "r") as file_diff_words:
    for line in file_diff_words:
        line = line.lower()
        line = line.strip().split()
        diff_words.extend(line)
# print(diff_words)

text = "".join(file.read().splitlines())

file_diff_words.close()
file.close()
split_text = filter(None, re.compile("[.!?]").split(text))
sentences_counter = 0
words_counter = 0
diff_words_counter = 0
diff_words_list = []
for sentence in split_text:
    sentences_counter += 1
    words_per_string = re.compile("\\s+").split(sentence.strip().replace(",", "").replace("(", "").replace(")", "").replace(":", ""))
    for word in words_per_string:
        word = word.lower()
        # print(word)
        if word.lower() not in diff_words:
            diff_words_list.append(word.lower())
            diff_words_counter += 1
        words_counter += 1

syllables, polysyllables = syllables_counter(text).split(" ")
chars = char_counter(text)

print(f"Words: {words_counter}")
print(f"Difficult words: {diff_words_counter}")
print(f"Sentences: {sentences_counter}")
print(f"Characters: {chars}")
print(f"Syllables: {syllables}")
print(f"Polysyllables: {polysyllables}")
calc_type = input("Enter the score you want to calculate (ARI, FK, SMOG, CL, all): ")
print()
if "ARI" == calc_type:
    metrics(True, False, False, False, False, False)
elif "FK" == calc_type:
    metrics(False, True, False, False, False, False)
elif "SMOG" == calc_type:
    metrics(False, False, True, False, False, False)
elif "CL" == calc_type:
    metrics(False, False, False, True, False, False)
elif "PB" == calc_type:
    metrics(False, False, False, False, True, False)
elif "all" == calc_type:
    metrics(False, False, False, False, False, True)

