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
    #model_path = os.path.join(os.getcwd(), "sentiment_model")
    model_path = os.path.join(os.getcwd(), "output", "model-best")

    # load the custom-trained model
    nlp = spacy.load(model_path)

    # sample text input
    with open(file, 'r') as file:
        textList = file.read().split('\n')

    # process the text with spaCy
    for text in textList:
        doc = nlp(text)
        if (doc.cats['Violento'] > doc.cats['No Violento']):
            print("Violento\t", round(doc.cats['Violento'], 2), "\t", round(doc.cats['No Violento'], 2), "\t", text)
        else:
            print("No Violento\t", round(doc.cats['Violento'], 2), "\t", round(doc.cats['No Violento'], 2), "\t", text)


prueba_txt('pruebas.txt')
