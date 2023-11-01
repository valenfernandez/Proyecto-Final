from spacy.tokens import DocBin
import spacy
import json
import random

categories = ["Violento", "No Violento"]
nlp = spacy.blank("es")
with open('dataset.json', 'r', encoding = 'utf-8') as f:
    input_data = json.load(f)  

    unique = list({ each['text'] : each for each in input_data if len(each['text']) < 200}.values())

with open('Data.json'.format(1), 'w', encoding='utf-8') as file:
    json.dump(unique, file, ensure_ascii=False)
