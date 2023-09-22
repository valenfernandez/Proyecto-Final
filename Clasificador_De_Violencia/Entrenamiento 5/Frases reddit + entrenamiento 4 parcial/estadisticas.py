# Adapted from convert_corpora.py script from Morgan McGuire
# https://gist.github.com/morganmcg1/a43842b847e2ff7dc78d2c3e5990bb96
from spacy.tokens import DocBin
import spacy
import json

def read_json_items(train_data):
    """
    Lee el archivo json y devuelve un generador de diccionarios con los datos de entrenamiento.
    ----------
    Parameters

    train_data: lista de diccionarios con los datos de entrenamiento.

    ----------
    Generador de diccionarios con los datos de entrenamiento.
    """
    for item in train_data:
        if "sentiment" in item:
            index = categories.index(item["sentiment"])
            count[index] = count[index] + 1

    for category in categories:
        print(category, count[categories.index(category)])

categories = ["Violento", "No Violento"]
count = [0,0]
nlp = spacy.blank("es")
with open('dataset reddit + frases entrenamiento 4.json', 'r', encoding = 'utf-8') as f:
    input_data = json.load(f) 

records = read_json_items(input_data)