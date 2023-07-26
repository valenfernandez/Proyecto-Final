import spacy
import os

def prueba_txt(file):
    """
    Probar el modelo entrenado con un archivo de texto.

    Parameters
    ----------
    :param: file (str)  Nombre del archivo de texto.

    """
    # define path to custom-trained model
    model_path = os.path.join(os.getcwd(), "output", "model-best")

    # load the custom-trained model
    nlp = spacy.load(model_path)

    # sample text input
    with open(file, 'r') as file:
        textList = file.read().split('\n')

    # process the text with spaCy
    for text in textList:
        if "--" in text: # Para poder agregar comentarios con '--'
            print(text)
            continue
        doc = nlp(text)
        print(text)
        for key, value in doc.cats.items():
            print(key, ":", round(value, 3), "- ", end="")

        print("")
        print("")

prueba_txt('pruebas.txt')
