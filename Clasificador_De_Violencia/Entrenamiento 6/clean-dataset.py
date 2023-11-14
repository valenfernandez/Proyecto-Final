from spacy.tokens import DocBin
import spacy
import json
import random

def cleanText(dictElement):
    dictText = dictElement['text'].lower().replace(";", " ") \
    .replace(".", " ") \
    .replace("\"", " ") \
    .replace("/", " ") \
    .replace("\\", " ") \
    .replace("[", " ") \
    .replace("]", " ") \
    .replace("*", " ") \
    .replace("'", " ") \
    .replace("-", " ") \
    .replace("|", " ") \
    .replace("(", " ") \
    .replace(")", " ") \
    .replace("!", " ") \
    .replace("¡", " ") \
    .replace(":", " ") \
    .replace(",", " ") \
    .replace("»", " ") \
    .replace("+", " ") \
    .replace("…", " ") \
    .replace("`", " ") \
    .replace("´", " ") \
    .replace("á", "a") \
    .replace("é", "e") \
    .replace("í", "i") \
    .replace("ó", "o") \
    .replace("ú", "u") \
    .replace("ú", "u") \
    .replace("ḉ", " ") \
    .replace("  ", " ") \
    .replace("  ", " ") \
    .replace("  ", " ") \
    .strip() \

    wordList = list(dictText)

#    for x in range(0, len(wordList) // 2):
#        pasarUnCaracterAMayuscula(wordList)

    print("".join(wordList))

    dictElement.update({'text': "".join(wordList), 'sentiment': dictElement['sentiment']})
    return dictElement

def pasarUnCaracterAMayuscula(wordList):
    randomCharacter = random.randint(0, len(wordList) - 1)

    while wordList[randomCharacter] == ' ':
        randomCharacter = random.randint(0, len(wordList) - 1)

    wordList[randomCharacter] = wordList[randomCharacter].upper()

categories = ["Violento", "No Violento"] 
nlp = spacy.blank("es")
with open('dataset.json', 'r', encoding = 'utf-8') as f:
    input_data = json.load(f)  

    unique = list({ each['text'] : cleanText(each) for each in input_data if len(each['text']) < 200}.values())

with open('clean-dataset-mayusculas-aleatorias.json'.format(1), 'w', encoding='utf-8') as file:
    json.dump(unique, file, ensure_ascii=False)
