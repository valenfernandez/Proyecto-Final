import pandas as pd
from pyarrow.parquet import ParquetFile
import pyarrow as pa 
import numpy as np
import spacy
import os



def pluralizar(w):
    """Devuelve la forma plural de una palabra.

    Parameters
    ----------
    w : str
        Palabra a pluralizar.
    
    Returns
    -------
    ret
        La palabra en plural.
    """

    ret = [w]
    if w[-1] in set("aeiouáéíóú"):
        ret.append(w + "s")
    else:
        ret.append(w + "es")
    return ret


def load_dictionary(path, *, extend = True):
    """Carga un diccionario de palabras.

    Parameters
    ----------
    path : str
        Ruta al archivo de diccionario.
    extend : bool, optional
        Si es True, extiende el diccionario con las formas plurales de las palabras.

    Returns
    -------
    ret : dict
        Diccionario de palabras.
    """
    ret = {}
    with open(path, encoding="utf-8") as fin:
        for line in fin:
            for word in pluralizar(line.strip()):
                ret[word] = True
                if extend:
                    noacc = word.translate(xt_acentos)
                    ret[noacc] = True
    return ret


def is_lang(message, langdict, *, debug=False):
    """Determina si un mensaje está escrito en español

    Parameters
    ----------
    message : str
        Mensaje a analizar.
    langdict : dict
        Diccionario de palabras.
    debug : bool, optional
        Si es True, devuelve una lista de tuplas (palabra, está en el diccionario).
    
    Returns
    -------
    score : float
        Puntuación de la probabilidad de que el mensaje esté escrito en español.
    """
    message = message.translate(xt_nopunct).lower()
    words = [ w for w in message.split() if w.strip() ]
    if len(words) <= 1:
        return 0.0
    score = sum( w in langdict for w in words ) / len(words)
    if debug:
        return [(w, w in langdict) for w in words]
    return score


def listar_violentos(file, output_file):
    """
    Detecta las frases violentas de un archivo de texto.

    Parameters
    ----------
    :param: file (str)  Nombre del archivo de texto.

    """
    print("Cargando modelo")
    model_path = os.path.join(os.getcwd(), "modelo_binario", "model-best-transformers")
    nlp = spacy.load(model_path)
    print("Modelo cargado")

    with open(output_file, 'w', encoding="utf-8") as f_output:
        with open(file, 'r', encoding="utf-8") as file:
            textList = file.read().split('\n')
        print("Texto cargado")
        docs = nlp.pipe(textList)
        for doc in docs:
            for key, value in doc.cats.items():
                if key == "Violento" and value > 0.5:
                    f_output.write(doc.text + "\n")
    return 1
               




xt_nopunct = str.maketrans("", "", ".,;:¿?¡!()-_#*[]")
xt_acentos = str.maketrans("áéíóú", "aeiou")

def extraer(file, output_file):
    dict = load_dictionary("0_palabras_todas.txt") # https://github.com/JorgeDuenasLerin/diccionario-espanol-txt 

    pf = ParquetFile(file) 
    print("archivo abierto")

    #first_ten_rows = next(pf.iter_batches(batch_size = 10000)) 
    #df = pa.Table.from_batches([first_ten_rows]).to_pandas() 

    with open(output_file,'w' , encoding="utf-8") as textos_español:
        for batch in pf.iter_batches(batch_size=10000):
            df = batch.to_pandas()
            for index, row in df.iterrows():
                texto = row.loc["body"]
                if is_lang(texto, dict) > 0.8: #no se cual seria el umbral optimo
                    textos_español.write(texto + "\n")
                    print(texto)
    return 1


""" 
folder_path = "archivos_reddit"
file_list = os.listdir(folder_path)
for filename in file_list:
    input_file_path = os.path.join(folder_path, filename)
    output_file_path = "texto_extraido/" + filename[:-8] +"-es" + ".txt"
    extraer(input_file_path, output_file_path)

# violentos = listar_violentos("RC_2012-01.txt", "RC_2012-01_violentos.txt")
#if (violentos): 
#    print("Violentos detectados")


folder_path = "texto_extraido"
input_file_path = os.path.join(folder_path, "RC_2013-01-es.txt")
output_file_path = "violentos/" + "RC_2013-01-violentos" + ".txt"
listar_violentos(input_file_path, output_file_path)
"""

folder_path = "texto_extraido"
file_list = os.listdir(folder_path)
for filename in file_list:
    input_file_path = os.path.join(folder_path, filename)
    output_file_path = "violentos/" + filename[:-4] +"-violentos" + ".txt"
    listar_violentos(input_file_path, output_file_path)
    print("Violentos detectados: ", filename)