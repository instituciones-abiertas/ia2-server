import re
from text_to_num import alpha2digit


def remove_multiple_strings(cur_string, replace_list):
    for cur_word in replace_list:
        cur_string = cur_string.replace(cur_word, "")
    return cur_string


def text_es_to_num(str):
    return alpha2digit(str, "es")


def find_replace_multi_ordered(string, dictionary):
    # sort keys by length, in reverse order
    for item in sorted(dictionary.keys(), key=len, reverse=True):
        string = re.sub(item, dictionary[item], string)
    return string
