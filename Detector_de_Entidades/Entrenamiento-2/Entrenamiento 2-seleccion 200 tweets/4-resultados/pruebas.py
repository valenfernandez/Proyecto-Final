import spacy

# define path to custom-trained model
model_path = "C:/Users/Valentina/Desktop/Proyecto_Final/Proyecto-Final/Detector_de_Entidades/Entrenamiento-2/Entrenamiento 2- frases + tweets/4-resultados/output/model-best"

# load the custom-trained model
nlp = spacy.load(model_path)

# sample text input
text = "Juan Martinez nacio en Hawaii el 10 de Marzo de 1961."

# process the text with spaCy
doc = nlp(text)

# iterate over named entities and print them
for ent in doc.ents:
    print(ent.text, ent.label_)