import json

import requests


def get_new_word(json_text):
    my_json = json.loads(json_text)

    json_object = my_json[0]

    name = json_object["word"]

    phonetics = json_object["phonetics"][0]["text"]

    definitions = json_object["meanings"][0]["definitions"]

    meaning = ""
    example = ""
    def_len = len(definitions)
    for i in range(def_len):
        definition = definitions[i]
        if "example" in definition.keys():
            example = definition["example"]
            meaning = definition["definition"]
            break

        elif i == def_len:
            meaning = definitions[0]["definition"]
            example = "No example has been founded"

    word = Word(name, phonetics, meaning, example)

    return word


def get_response(this_word):
    URL = "https://api.dictionaryapi.dev/api/v2/entries/en/" + this_word

    response = requests.get(URL).text

    my_word = get_new_word(response)

    print(my_word.name)
    print(my_word.example)
    print(my_word.meaning)
    print(my_word.phonetic)

    return my_word


class Word:

    def __init__(self, name, phonetic_text, meaning, example):
        self.name = name
        self.phonetic = phonetic_text
        self.meaning = meaning
        self.example = example
