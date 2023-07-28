import json
from spacy.tokens import DocBin
import spacy
import random


def process_phrases(files_s, output_path):
    processed_phrases = []
    for file in files_s:
        file_path = file["file"]
        sentiment = file["sentiment"]
        with open(file_path, 'r', encoding = 'utf-8') as file:
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
        case "Sexual":
            return 0
        case "Física":
            return 1
        case "Económica":
            return 2
        case "Psicológica":
            return 3
        case "Simbólica":
            return 4
        case "Indefinido":
            return 5

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


files_s = [{'file': "simbolica.txt",
           'sentiment': "Simbólica"},
            {'file': "economica.txt",
            'sentiment': "Económica"},
            {'file': "psicologica.txt",
            'sentiment': "Psicológica"},
            {'file': "sexual.txt",
            'sentiment': "Sexual"},
            {'file': "fisica.txt",
            'sentiment': "Física"}
           # ,{'file': "indefinido.txt",
            #'sentiment': "Indefinido"}
]

processed_data = process_phrases(files_s, 'dataset.json')

# categories = ["Sexual", "Física", "Económica", "Psicológica", "Simbólica", "Indefinido"]
categories = ["Sexual", "Física", "Económica", "Psicológica", "Simbólica"]
nlp = spacy.blank("es")
with open('dataset.json', 'r', encoding = 'utf-8') as f:
    input_data = json.load(f)      

random.shuffle(input_data)

# select 70% of input data for training set
train_size = int(len(input_data) * 0.7)
train_data = input_data[:train_size]
test_data = input_data[train_size:]

records_train = read_json_items(train_data)
records_test = read_json_items(test_data)
docs_train = [convert_record(nlp, record, categories) for record in records_train]
docs_test = [convert_record(nlp, record, categories) for record in records_test]

out_data_train = DocBin(docs=docs_train).to_bytes()
with open('train.spacy', 'wb') as f:
    f.write(out_data_train)
out_data_test = DocBin(docs=docs_test).to_bytes()
with open('test.spacy', 'wb') as f:
    f.write(out_data_test)        
print(f'{f} converted')

#python -m spacy train config.cfg --output ./output --paths.train train.spacy --paths.dev test.spacy