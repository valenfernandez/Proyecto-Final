import spacy
import os

def format_msj_wpp(file):
    """
    Formatear el archivo de conversación de WhatsApp a un diccionario con los 
    mensajes de cada usuario y otro diccionario con todos los mensajes justo con su
    fecha.

    Parameters
    ----------
    :param: file (str)  Nombre del archivo de conversación de WhatsApp.

    Returns
    -------
    :return: user_texts (dict) Diccionario con los mensajes de cada usuario.
    :return: all_texts (dict) Diccionario con todos los mensajes con su fecha.
    """
    with open(file, 'r', encoding='utf-8') as file:
        user_texts = {}
        all_texts = {}
        file.readline()
        for line in file:
            if not line.strip():
                continue
            date_name_text = line.strip().split(' - ')
            if len(date_name_text) != 2:
                continue
            name_index = date_name_text[1].find(':')
            name = date_name_text[1][:name_index]
            text = date_name_text[1][name_index+2:]

            if name not in user_texts:
                user_texts[name] = []
            
            user_texts[name].append(text)
            date = date_name_text[0]
            all_texts[date] = {'User': name, 'Date': date, 'Text': text}

    return user_texts, all_texts


def prueba_txt(file):
    """
    Probar el modelo entrenado con un archivo de texto.

    Parameters
    ----------
    :param: file (str)  Nombre del archivo de texto.

    """
    # define path to custom-trained model
    #model_path = os.path.join(os.getcwd(), "sentiment_model")
    model_path = os.path.join(os.getcwd(), "output_with_sm", "model-best")

    # load the custom-trained model
    nlp = spacy.load(model_path)

    # sample text input
    with open(file, 'r') as file:
        textList = file.read().split('\n')

    # process the text with spaCy
    for text in textList:
        doc = nlp(text)
        print(doc.cats, "-", text)


def prueba_wpp(file):
    """
    Probar el modelo entrenado con un archivo de conversación de WhatsApp.

    Parameters
    ----------
    :param: file (str)  Nombre del archivo de conversación de WhatsApp.
    
    """
    # define path to custom-trained model
    model_path = os.path.join(os.getcwd(), "output_with_sm", "model-best")
    nlp = spacy.load(model_path)
    user_texts, all_texts = format_msj_wpp(file)
    for name, texts in user_texts.items():
        print(name + ":")
        for text in texts:
            doc = nlp(text)
            print(doc.cats, "-", text)

prueba_txt('pruebas.txt')

#prueba_wpp('conversacion.txt')