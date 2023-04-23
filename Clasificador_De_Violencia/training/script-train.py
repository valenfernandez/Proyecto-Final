import spacy
import random
import json
from spacy.util import minibatch, compounding
from spacy.pipeline.textcat_multilabel import DEFAULT_MULTI_TEXTCAT_MODEL
from spacy.training import Example

TRAIN_DATA = []

# Load the SpaCy model for text classification
nlp = spacy.blank("es")
textcat = nlp.add_pipe("textcat")

# Define the text categories
textcat.add_label("Violento")
textcat.add_label("No Violento")

# Load the JSON data
with open('datos-min.json') as json_file:
    json_data = json.load(json_file)

# Convert the JSON data into a format that can be used to train a text categorizer
for data in json_data:
    text = data["text"]
    sentiment = data["sentiment"]
    if sentiment == "Violento":
        label = {"cats": {"Violento": 1, "No Violento": 0}}
    else:
        label = {"cats": {"Violento": 0, "No Violento": 1}}
    TRAIN_DATA.append((text, label))

# Train the text categorizer
nlp.begin_training()
random.seed(1)
spacy.util.fix_random_seed(1)

# Split the training data into batches and train the model on each batch
batch_size = 8
epochs = 10
max_batch_size = 64

examples = []
for text, annots in TRAIN_DATA:
    examples.append(Example.from_dict(nlp.make_doc(text), annots))
nlp.initialize(lambda: examples)

for epoch in range(epochs):
    random.shuffle(TRAIN_DATA)
    batches = minibatch(examples, size=compounding(4.0, max_batch_size, 1.001))
    for batch in batches:
        nlp.update(batch)

# Save the trained model
nlp.to_disk("sentiment_model")
