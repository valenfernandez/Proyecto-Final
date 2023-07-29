import pandas as pd
from pyarrow.parquet import ParquetFile
import pyarrow as pa 
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


def listar_violentos(file):
    """
    Detecta las frases violentas de un archivo de texto.

    Parameters
    ----------
    :param: file (str)  Nombre del archivo de texto.

    """
    frases_violentas = []
    model_path = os.path.join(os.getcwd(), "modelo_binario", "model-best")
    nlp = spacy.load(model_path)

    with open(file, 'r') as file:
        textList = file.read().split('\n')
    for text in textList:
        doc = nlp(text)
        for key, value in doc.cats.items():
            if key == "violento" and value > 0.5:
                frases_violentas.append(text)
               




xt_nopunct = str.maketrans("", "", ".,;:¿?¡!()-_#*[]")
xt_acentos = str.maketrans("áéíóú", "aeiou")

dict = load_dictionary("0_palabras_todas.txt") # https://github.com/JorgeDuenasLerin/diccionario-espanol-txt 


pf = ParquetFile('RC_2012-01.parquet') 
df = pa.Table.to_pandas(pf.read(columns=['subreddit', 'body'])) 
with open("textos.txt", encoding="utf-8") as textos_español:
    for index, row in df.iterrows():
        texto = row.loc["body"]
        if is_lang(texto, dict) > 0.6: #no se cual seria el umbral optimo
            textos_español.write(texto + "\n")
            print(texto)

"""
violentos = listar_violentos("textos.txt")
with open('textos_violentos.txt', 'w') as f:
    for frase in violentos:
        f.write("%s\n" % frase)
"""
