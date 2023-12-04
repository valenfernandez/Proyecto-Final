import spacy
import os
from pathlib import Path

def prueba_txt(model_path):
    """
    Probar el modelo entrenado con un archivo de texto.

    Parameters
    ----------
    :param: file (str)  Nombre del archivo de texto.

    """

    # load the custom-trained model
    nlp = spacy.load(model_path)

    # sample text input
    with open("pruebas.txt", 'r') as file:
        textList = file.read().split('\n')

    # process the text with spaCy
    for text in textList:
        text = text.lower()
        text = text.replace(";", " ") \
        .replace(".", " ") \
        .replace("\"", " ") \
        .replace("/", " ") \
        .replace("\\", " ") \
        .replace("[", " ") \
        .replace("]", " ") \
        .replace("*", " ") \
        .replace("'", " ") \
        .replace("-", " ") \
        .replace("|", " ") \
        .replace("(", " ") \
        .replace(")", " ") \
        .replace("!", " ") \
        .replace("¡", " ") \
        .replace(":", " ") \
        .replace(",", " ") \
        .replace("»", " ") \
        .replace("+", " ") \
        .replace("…", " ") \
        .replace("`", " ") \
        .replace("´", " ") \
        .replace("á", "a") \
        .replace("é", "e") \
        .replace("í", "i") \
        .replace("ó", "o") \
        .replace("ú", "u") \
        .replace("ú", "u") \
        .replace("ḉ", " ") \
        .replace("”", " ") \
        .replace("“", " ") \
        .replace("  ", " ") \
        .replace("  ", " ") \
        .replace("  ", " ") \
        .strip()
        doc = nlp(text)
    # process the text with spaCy
    for text in textList:
        doc = nlp(text.lower())
        print(round(doc.cats['Violento'], 2))


path = Path(os.getcwd())
model_path_1 = os.path.join(path.parent.absolute(), "Entrenamiento 1", "pruebas", "output", "model-best")
model_path_2 = os.path.join(path.parent.absolute(), "Entrenamiento 2 con transformers", "3.pruebas", "output", "model-best")
model_path_3 = os.path.join(path.parent.absolute(), "Entrenamiento 3 con transformers", "3.pruebas", "output", "model-best")
model_path_4 = os.path.join(path.parent.absolute(), "Entrenamiento 4", "output batch 100 epocas 8", "model-best")
model_path_5 = os.path.join(path.parent.absolute(), "Entrenamiento 5", "Frases reddit + entrenamient 4 completo", "output", "model-best")
model_path_6 = os.path.join(path.parent.absolute(), "Entrenamiento 6", "output-etapa-4", "model-best")
model_path_7 = os.path.join(path.parent.absolute(), "Entrenamiento 7", "output", "model-best")
print("############## 1")
prueba_txt(model_path_1)
print("############## 2")
prueba_txt(model_path_2)
print("############## 3")
prueba_txt(model_path_3)
print("############## 4")
prueba_txt(model_path_4)
print("############## 5")
prueba_txt(model_path_5)
print("############## 6")
prueba_txt(model_path_6)
print("############## 7")
prueba_txt(model_path_7)