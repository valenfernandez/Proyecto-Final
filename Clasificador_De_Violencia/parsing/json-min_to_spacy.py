from spacy.tokens import DocBin
import spacy
import json

def read_json_items(train_data):
    for item in train_data:
        yield {
            "text": item["text"],
            "labels": [0 if item["sentiment"] == "Violento" else 1]
        }

def convert_record(nlp, record, categories):
    """Convert a record from the json into a spaCy Doc object."""
    doc = nlp.make_doc(record["text"])
    # All categories other than the true ones get value 0
    doc.cats = {category: 0 for category in categories}
    # True labels get value 1
    for label in record["labels"]:
        doc.cats[categories[label]] = 1
    return doc

def convert_files(lang: str="es"):
    categories = ["Violento", "No Violento"]
    nlp = spacy.blank(lang)
    with open('datos-min.json', 'r') as f:
        input_data = json.load(f)      

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

# Convert Files
convert_files()