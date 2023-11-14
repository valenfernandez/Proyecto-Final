# Adapted from convert_corpora.py script from Morgan McGuire
# https://gist.github.com/morganmcg1/a43842b847e2ff7dc78d2c3e5990bb96
from spacy.tokens import DocBin
import spacy
import json
import random

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
            yield {
                "text": item["text"],
                "labels": [0 if item["sentiment"] == "Violento" else 1]
            }

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


categories = ["Violento", "No Violento"]
nlp = spacy.blank("es")
with open('clean-dataset-mayusculas-aleatorias.json', 'r', encoding = 'utf-8') as f:
    input_data = json.load(f)     

random.shuffle(input_data) 

unique_violento = list({ each['text'] : each for each in input_data if each['sentiment'] == 'Violento'}.values())
unique_no_violento = list({ each['text'] : each for each in input_data if each['sentiment'] == 'No Violento'}.values())

# select 70% of input data for training set
train_size_violento = int(len(unique_violento) * 0.7)
train_size_no_violento = int(len(unique_no_violento)* 0.7)

train_data_violento = unique_violento[:train_size_violento]
test_data_violento = unique_violento[train_size_violento:]
train_data_no_violento = unique_no_violento[:train_size_no_violento]
test_data_no_violento = unique_no_violento[train_size_no_violento:]

test_data = test_data_violento + test_data_no_violento
train_data = train_data_no_violento + train_data_violento

random.shuffle(test_data) 
random.shuffle(train_data) 

print(len(train_data))
print(len(test_data))

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