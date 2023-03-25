import spacy
import os

# define path to custom-trained model
model_path = os.path.join(os.getcwd(), "output", "model-best")

# load the custom-trained model
nlp = spacy.load(model_path)

# sample text input
text = ("Juan Martinez nacio en Hawaii el 10 de Marzo de 1961. Durante la decada del 80 "
", empezó a aparecer en varias películas. En 1981, viajó a Argentina y fundó dos empresas. " 
"Un mes despues, en diciembre, chocó con su auto en la playa. Llamó a su amigo Luis para decirle que perdió la memoria. " 
"Cuando Luis le preguntó como recordaba su nombre, Juan se dio cuenta de que estaba bien. Le pagó 2000 pesos por ayudarlo. "
"Luis viajó dos noches despues, en el teatro municipal, para ir a un recital de musica de su grupo favorito, Los Rockeros. "
"Durante el recital, a las 0 AM, se prendieron 12 luminarias para celebrar la llegada de Año Nuevo. Luis y sus amigos laura y marcos "
"prendieron tres velas para acompañar. Se fueron a sus casas, alrededor de las tres y media de la mañana. Tardaron 25 minutos en llegar.")

# process the text with spaCy
doc = nlp(text)

# iterate over named entities and print them
for ent in doc.ents:
    print(ent.text, ent.label_)