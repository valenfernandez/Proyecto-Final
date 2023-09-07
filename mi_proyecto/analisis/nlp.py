from .models import Analisis, Aplicacion, Resultado, Modelo, Carpeta, Archivo
import spacy
import os


def procesar_analisis(analisis):
    """ 
    Esta funcion realiza el procesamiento pedido por el usuario y genera los resultados.
    
    Parameters
    ----------

    :param: analisis (Analisis) El analisis que recibe tiene: informe vacio, fecha actual, carpeta y modelo elegidos.

    """
    carpeta = analisis.carpeta
    modelo = analisis.modelo

    # 1: Cargar el modelo

    model_path = os.path.join(os.getcwd(), "static", "modelos", modelo.nombre) #asumo que el modelo esta guardado con el mismo nombre que tengo en la base de datos
    nlp = spacy.load(model_path)

    # 2: Extraer textos de los archivos en la carpeta

    archivos = Archivo.objects.filter(carpeta = carpeta)
    for archivo in archivos:
        file = archivo.arch

        #chequear primero si es un archivo con una conversacion de whatsapp para hacer el preprocesamiento correspondiente.

        with open(file, 'r', encoding='utf-8') as f:
            lines = f.read().splitlines() # no se si esto se deberia hacer o no
        docs = list(nlp.pipe(lines))

       

        # armo el objeto resultado de cada uno:
        # cambiaria el json de detectado segun el modelo 
        for doc in docs:
            texto = doc.text
            detectado = doc.ents # en realidad esto seria un json que tengo que armar.
            archivo_origen = archivo
            numero_linea = 0 # sería la posicion en el vector capaz
            Resultado(texto= texto, detectado = detectado, numero_linea = numero_linea, analisis = analisis, archivo_origen = archivo_origen).save()



    # 4: procesar los resultados y armar el informe segun el modelo que sea
    
    pass

def armar_informe(): 
    #seria generar un html con el resumen, los graficos y estadisticas.
    #se podria usar altair 
    pass


def format_msj_wpp(file): #como se plantea la solucion se podria perder el nombre del usuario que envio el mensaje. Podria incorporarse como parte del json en 'detectado' {sentimiento: VIOLENTO, remitente: User} lo mismo con la fecha.

    #capaz en un campo 'metadata' porque el tema seria si en una carpeta a analizar hay varios archivos unos de wpp y otros no. 

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