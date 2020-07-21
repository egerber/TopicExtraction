import pickle
import hashlib


def save_dictionary(dictionary, filename):
    dict_file = open(filename, "wb")
    pickle.dump(dictionary, dict_file)
    dict_file.close()


def read_dictionary(filename):
    a_file = open(filename, "rb")
    dictionary = pickle.load(a_file)

    return dictionary


def flatten(nested_list):
    return [item for sublist in nested_list for item in sublist]


def string2numeric_hash(text):
    if not type(text) == str:
        return -1
    return int(hashlib.md5(text.encode('utf-8')).hexdigest()[:8], 16)
