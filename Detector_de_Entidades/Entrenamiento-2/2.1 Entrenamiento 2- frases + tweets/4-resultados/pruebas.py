import spacy
import os

# define path to custom-trained model
model_path = os.path.join(os.getcwd(), "output", "model-best")
# load the custom-trained model
nlp = spacy.load(model_path)

# sample text input
text = "Juan Martinez nacio en Hawaii el 10 de Marzo de 1961. Durante la decada del 80, empezó a aparecer en varias películas. En 1981, viajó a Argentina y fundó dos empresas. Un mes despues, en diciembre, chocó con su auto en la playa. Llamó a su amigo Luis para decirle que perdió la memoria. Cuando Luis le preguntó como recordaba su nombre, Juan se dio cuenta de que estaba bien. Le pagó 2000 pesos por ayudarlo."

# process the text with spaCy
doc = nlp(text)

# iterate over named entities and print them
for ent in doc.ents:
    print(ent.text, ent.label_)