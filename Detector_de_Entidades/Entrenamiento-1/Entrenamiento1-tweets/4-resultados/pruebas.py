import spacy
import os

# define path to custom-trained model
model_path = os.path.join(os.getcwd(), "output", "model-best")

# load the custom-trained model
nlp = spacy.load(model_path)

# sample text input
text = "Juan Martinez nacio en Hawaii el 10 de Marzo de 1961."

# process the text with spaCy
doc = nlp(text)

# iterate over named entities and print them
for ent in doc.ents:
    print(ent.text, ent.label_)