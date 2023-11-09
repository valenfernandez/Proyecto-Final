import json
import random


def labelstudio_to_list(file):
    """
    Convertir el archivo json de labelstudio a una lista de diccionarios
    con el formato usado por spaCy.

    Parameters
    ----------
    :param: file (str)  Nombre del archivo json.
    
    Returns
    -------
    :return: lineas (list) Lista de diccionarios con el formato usado por spaCy.

    """
    lineas = []
    with open(file, encoding='utf-8') as json_file:
        json_data = json.load(json_file)
    with open('datos.json', 'w', encoding='utf-8') as outfile:
        for data in json_data:
            sentiment = data["sentiment"]
            if sentiment == "Violento":
                label = {"cats": {"Violento": 1, "No Violento": 0}}
            else:
                label = {"cats": {"Violento": 0, "No Violento": 1}}
            element = {"text": data["text"], "cats": label}
            lineas.append(element)
    return lineas

def train_test(lines, ratio): 
    """ 
    Dividir el conjunto de datos en entrenamiento y prueba. 
    y guardarlos en archivos json para el entrenamiento.

    Parameters
    ----------
    :param: lines (list) Lista de diccionarios con el formato usado por spaCy.
    :param: ratio (float) Proporción de datos para entrenamiento.

    """
    train_num = int(len(lines)*ratio)
    random.shuffle(lines)
    train = lines[:train_num]
    test = lines[train_num:]
    with open('train.json', 'w', encoding="utf-8") as file:
        json.dump(train, file, ensure_ascii=False)

    with open('test.json', 'w', encoding="utf-8") as file:
        json.dump(test, file, ensure_ascii=False)

    

file = 'datos-min.json'
lines = labelstudio_to_list(file)
train_test(lines, ratio = 0.7)
