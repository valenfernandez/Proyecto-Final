import spacy
import os

# define path to custom-trained model
model_path = os.path.join(os.getcwd(), "output_with_sm", "model-best")

# load the custom-trained model
nlp = spacy.load(model_path)

# sample text input
with open('pruebas.txt', 'r') as file:
    textList = file.read().split('\n')

# process the text with spaCy
for text in textList:
    doc = nlp(text)

    # iterate over named entities and print them
    print(doc.cats, "-", text)