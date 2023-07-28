import json
from spacy.tokens import DocBin
import spacy
import random


def process_phrases(file,sentiment , output_path):
    processed_phrases = []
    with open(file, 'r', encoding = 'utf-8') as file:
        lines = file.readlines()
        for i, line in enumerate(lines):
            phrase = line.strip()
            processed_phrase = {
                    "text": phrase,
                    "id": i + 1,
                    "sentiment": sentiment,
                    "annotator": 1,
                    "annotation_id": i + 1,
                    "created_at": "2023-07-13T00:00:00.000000Z",
                    "updated_at": "2023-07-13T00:00:00.000000Z",
                    "lead_time": 8.342
                }
            processed_phrases.append(processed_phrase)
        with open(output_path, 'w', encoding = 'utf-8') as file:
            json.dump(processed_phrases, file, indent=4, ensure_ascii=False)

def read_json_items(train_data):
    """
    Lee el archivo json y devuelve un generador de diccionarios con los datos de entrenamiento.
    ----------
    Parameters

    train_data: lista de diccionarios con los datos de entrenamiento.

    ----------
    Generador de diccionarios con los datos de entrenamiento.
    """
    count = 0;
    for item in train_data:
        if "sentiment" not in item:
            count = count + 1
        if "sentiment" in item: #Para descartar a los items que fueron salteados y no tienen sentiment
            yield {
                "text": item["text"],
                "labels": [getSentimentValue(item["sentiment"])]
            }

def getSentimentValue(sentiment) :
    match sentiment:
        case "Violento":
            return 1
        case "No Violento":
            return 2

def convert_record(nlp, record, categories):
    """
    Convierte los datos de entrenamiento en un objeto Doc de spaCy.
    ----------
    Parameters

    nlp: Objeto de spaCy.
    record: Diccionario con los datos de entrenamiento.
    categories: Lista de categorías. (violento, no violento)

    ----------
    Returns

    doc: Objeto Doc de spaCy.
    """
    doc = nlp.make_doc(record["text"])
    # All categories other than the true ones get value 0
    doc.cats = {category: 0 for category in categories}
    # True labels get value 1
    for label in record["labels"]:
        doc.cats[categories[label]] = 1
    return doc


processed_data = process_phrases("frases_violentas_extra.txt","Violento", 'dataset_2.json')