import spacy
import os

# define path to custom-trained model
model_path = os.path.join(os.getcwd(), "sentiment_model")

# load the custom-trained model
nlp = spacy.load(model_path)

# sample text input
with open('pruebas.txt', 'r') as file:
    text = file.read().replace('\n', '')

# process the text with spaCy
doc = nlp(text)

# iterate over named entities and print them
print(doc.cats, "-", text)