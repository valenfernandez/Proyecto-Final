from .models import Analisis, Aplicacion, Resultado, Modelo, Carpeta, Archivo, Preferencias, Grafico, Grafico_Imagen, Tabla
import json
import spacy
from spacy import displacy
import os
import pandas as pd
import altair as alt
from altair_saver import save
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from django.core.files import File 
import io



def procesar_analisis(analisis, user):
    """ 
    Esta funcion realiza el procesamiento pedido por el usuario y genera los resultados.
    Por ahora la funcion solo permite aplicar modelos de entidades y clasificadores.
    Pero se podria extender para que permita aplicar otros modelos de NLP.
    
    Parameters
    ----------

    :param: analisis (Analisis) El analisis que recibe tiene: informe vacio, fecha actual, carpeta y modelo elegidos.

    """
    carpeta = analisis.carpeta
    modelo = analisis.modelo 

    if modelo.nombre == 'entidades': #cargo ese solo modelo y lo aplico
        procesar_entidades(analisis, carpeta, user)
    elif modelo.nombre == 'clasificador': # aplico primero el modelo binario y despues el modelo multicategoria.  
        procesar_clasificador(analisis, carpeta, user)
    else:
        raise Exception("El modelo no existe ", modelo) #podria cambiar esto, intentar cargar el modelo y si no existe tirar un error. Y pasar a hacer un procesamiento 'generico' que no dependa de un modelo en particular.


def procesar_entidades(analisis, carpeta, user):
    """ 
    TODO: Lectura del archivo en utf-8. Supeuestamente debería ser el default pero no lo esta leyendo asi como es un filefield se tiene que leer con file.open("r") capaz es un problema en el modelo o en el formulario cuando se guarda el archivo.




    Esta función se encarga de procesar los archivos de una carpeta con el modelo de detección de entidades.
    Para cada archivo, se extraen los textos y se detectan las entidades.
    Luego, se arma el objeto resultado y se lo guarda en la base de datos.
    Finalmente, se arma el informe con los resultados y se lo guarda en el analisis.

    Parameters
    ----------
    :param: analisis (Analisis) El analisis que recibe tiene: informe vacio, fecha actual, carpeta y modelo elegidos.
    :param: carpeta (Carpeta) La carpeta que recibe tiene: nombre, usuario y archivos.
    :param: user (User) El usuario que realiza el analisis.

    Return
    ------
    :return: 1 (int) Si el analisis se realizo correctamente devuelve 1.


    """
    
    # 1: Cargar el modelo de spacy
    model_path = os.path.join(os.getcwd(),"analisis", "static", "modelos", "entidades" )
    nlp = spacy.load(model_path)

    colors_azul_amarillo = {"DINERO": "#00065D", 
                            "FECHA":"#2706AD", 
                            "HORA": "#5C40D0", 
                            "LUGAR": "#889AFD",
                            "MEDIDA": "#CCC5B2",
                            "MISC": "#F3D850",
                            "ORG": "#FFD500",
                            "PERSONA": "#9A7300",
                            "TIEMPO" : "#DFA000",
                            }
    
    colors_azul_rosa = {"DINERO": "#00065D", 
                            "FECHA":"#2257EC", 
                            "HORA": "#008DDE", 
                            "LUGAR": "#7A8BE6",
                            "MEDIDA": "#D2C3C3",
                            "MISC": "#FF9696",
                            "ORG": "#F94D67",
                            "PERSONA": "#E9255A",
                            "TIEMPO" : "#99001C",
                            }

    preferencia = Preferencias.objects.get(usuario = user)
    if preferencia.color == "AM":
        options = {"colors": colors_azul_amarillo}
    elif preferencia.color == "AR":
        options = {"colors": colors_azul_rosa}
    else:
        options = {}

    # 2: Extraer textos de los archivos en la carpeta
    archivos = Archivo.objects.filter(carpeta = carpeta)
    for archivo in archivos:
        with open(archivo.arch.path, "r", encoding = 'UTF-8') as f:
            lines = f.read().splitlines()
            print(lines)
        docs = list(nlp.pipe(lines))

        # 3: Armar el objeto resultado de cada uno:
        for index, doc in enumerate(docs):

            entidades = []
            for ent in doc.ents:
                entidad = {
                    "text": ent.text,
                    "label": ent.label_
                }
                entidades.append(entidad)
            entidades_json = json.dumps(entidades, ensure_ascii=False)

            texto = doc.text
            detectado = entidades_json
            html = displacy.render(doc, style="ent", options=options)
            archivo_origen = archivo
            numero_linea = index + 1
            Resultado(texto= texto, detectado = detectado, html = html, numero_linea = numero_linea, analisis = analisis, archivo_origen = archivo_origen).save()

    # 4: Procesar los resultados y armar el informe segun el modelo que sea
    armar_informe_entidades(analisis, preferencia)

    return 1

def armar_informe_entidades(analisis, preferencia): 
    """
    Esta funcion crea el archivo html que contiene el informe de los resultados de un analisis creado por un modelo de deteccion de entidades.

    Parameters
    ----------
    :param: analisis (Analisis) Es un analisis realizado previamente que ya tiene resultados asociados, de los cuales se quiere crear un informe.

    :param: preferencia (Preferencias) Es un objeto que contiene las preferencias del usuario que realizo el analisis.

    Return
    ------
    :return: 1 (int) Si los elementos del informe se crearon correctamente devuelve 1.

    """

    os.makedirs(f'analisis/static/graficos/{analisis.id}', exist_ok=True)

    resultados = Resultado.objects.filter(analisis = analisis)
    
    domain =["DINERO", "FECHA", "HORA", "LUGAR", "MEDIDA", "MISC", "ORG", "PERSONA", "TIEMPO"]
    range_ = []

    if preferencia.color == "AM":
        range_= ["#00065D","#2706AD","#5C40D0","#889AFD", "#CCC5B2","#F3D850","#FFD500","#9A7300", "#DFA000"]
    elif preferencia.color == "AR":
        range_= ["#00065D", "#2257EC","#008DDE","#7A8BE6","#D2C3C3","#FF9696","#F94D67","#E9255A","#99001C"]
    else:
        range_ = []

    
    data = []
    for resultado in resultados:
        entidades = json.loads(resultado.detectado)

        for entidad in entidades:
            data.append({
                'text': entidad['text'],
                'label': entidad['label'],
                'archivo_origen': resultado.archivo_origen.nombre,
                'numero_linea': resultado.numero_linea
            })
    df = pd.DataFrame(data)

    total_entidades = df.shape[0]

    entidades_counts = df['label'].value_counts().reset_index()#pd indice tipos de entidades y valor num de apariciones
    entidades_counts.columns = ['Etiqueta', 'Apariciones']
    tabla_entidades_count = Tabla(nombre = "Distribucion de entidades", tabla = entidades_counts.to_html(classes='table table-striped table-hover table-sm', index=False), analisis = analisis)
    tabla_entidades_count.save()



    ent_text_counts = df['text'].value_counts() #entidades que se repitan: tendrian el count en mas de 1
    repeating_entities = ent_text_counts[ent_text_counts > 1] #entidades que se repiten
    num_rep = repeating_entities.shape[0] #numero de entidades que se repiten
    if num_rep > 0:
        tabla_rep_ents = repeating_entities.reset_index()
        tabla_rep_ents.columns = ['Entidad', 'Apariciones'] 
        tabla_repeating_ents = Tabla(nombre = "Entidades que se repiten", tabla = tabla_rep_ents.to_html(classes='table table-striped table-hover table-sm', index=False), analisis = analisis)
        tabla_repeating_ents.save()


    # Cantidad de cada tipo de entidades
    chart_count_ents = alt.Chart(df, title="Distribucion de entidades").mark_bar().encode(
        x = alt.X('label:N', title='Entidades'),
        y = alt.Y('count():Q', title='N° Apariciones'),
        color = alt.Color('label', scale = alt.Scale(domain=domain, range=range_))
    )
    json_count_ents = chart_count_ents.to_json()
    grafico_cout_ents = Grafico(nombre = "Distribucion de entidades", chart = json_count_ents, analisis = analisis)
    grafico_cout_ents.save()


    #Entidades por cada archivo
    file_entity_counts = df.groupby('archivo_origen')['text'].count().reset_index()
    file_entity_counts.columns = ['archivo_origen', 'entity_count']
    chart_ents_file = alt.Chart(file_entity_counts).mark_bar().encode(
        x=alt.X('archivo_origen:N', title='Archivo'),
        y=alt.Y('entity_count:Q', title='Numero de entidades'),
        color=alt.Color('archivo_origen:N', title='File', scale = alt.Scale(range=range_)),
        tooltip=['archivo_origen:N', 'entity_count:Q']
    ).properties(
        title='Entidades por archivo'
    ).interactive()
    json_ents_file = chart_ents_file.to_json()
    grafico_ents_file = Grafico(nombre = "Entidades por archivo", chart = json_ents_file, analisis = analisis)
    grafico_ents_file.save()


    #Tipo entidades por cada archivo
    # Group and count entity labels by file
    file_label_counts = df.groupby(['archivo_origen', 'label'])['text'].count().reset_index()
    file_label_counts.columns = ['archivo_origen', 'label', 'count']
    # Create a stacked bar chart
    chart_entscomp_file = alt.Chart(file_label_counts).mark_bar().encode(
        x=alt.X('archivo_origen:N', title='File'),
        y=alt.Y('count:Q', title='Entity Count'),
        color=alt.Color('label:N', title='Entity Label',scale = alt.Scale(domain=domain, range=range_)),
        tooltip=['archivo_origen:N', 'label:N', 'count:Q']
    ).properties(
        title='Composicion de entidades por archivo'
    )
    json_entscomp_file = chart_entscomp_file.to_json()
    grafico_entscomp_file = Grafico(nombre = "Composicion de entidades por archivo", chart = json_entscomp_file, analisis = analisis)
    grafico_entscomp_file.save()

    
    ## Relacion para cada archivo: numero de entidades y linea 
    scatterplots = []
    for file_name, group_df in df.groupby('archivo_origen'):
        scatterplot = alt.Chart(group_df).mark_circle().encode(
            x=alt.X('numero_linea:O', title='Numero de lines'),
            y=alt.Y('label:N', title='Entidad'),
            color=alt.Color('label:N', title='Entidad', scale = alt.Scale(domain=domain, range=range_)),
            tooltip=['label:N', 'numero_linea:O', 'text:N']
        ).properties(
            title=f'Relación entre numero de linea y entidades en archivo {file_name}'
        )
        scatterplots.append(scatterplot)
    chart_lineas_entidades = alt.vconcat(*scatterplots)
    json_lineas_entidades = chart_lineas_entidades.to_json()
    grafico_lineas_entidades = Grafico(nombre = "Relacion entre numero de linea y entidades", chart = json_lineas_entidades, analisis = analisis)
    grafico_lineas_entidades.save()
    


    #Wordcloud de los textos de las entidades
    text = ' '.join(df['text'])
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.title('Entidades detectadas')

    wordcloud_path = f'analisis/static/graficos/{analisis.id}/wordcloud_{analisis.id}.png'
    wordcloud.to_file(wordcloud_path)
    imagen_wordcloud_total = Grafico_Imagen(nombre = "Wordcloud de entidades", analisis = analisis)
    imagen_wordcloud_total.imagen.save(wordcloud_path, File(open(wordcloud_path, 'rb')))
    imagen_wordcloud_total.save()
    
    """

    # Wordcloud por cada tipo de entidad
    
    text_by_label = df.groupby('label')['text'].apply(lambda x: ' '.join(x))
    for label, text in text_by_label.items():
        wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)

        plt.figure(figsize=(8, 4))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis('off')
        plt.title(f'Word Cloud for Entity Label: {label}')
        
        wordcloud_path = f'analisis/static/graficos/{analisis.id}/wordcloud_{label}{analisis.id}.png'
        wordcloud.to_file(wordcloud_path)

        imagen_wordcloud = Grafico_Imagen(nombre = f"Wordcloud de entidades {label}", analisis = analisis)
        imagen_wordcloud.imagen.save(wordcloud_path, File(open(wordcloud_path, 'rb')))
        imagen_wordcloud.save()
    """

    return 1



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


def procesar_clasificador(analisis, carpeta, user):

    #TODO: La funcion no da los numero de linea y deja todos los no violentos que encuentra primero y los demas despues. No quedan las cosas en orden.

    # 1: Cargar el modelo de spacy binario y el multicategoría
    
    model_path = os.path.join(os.getcwd(),"analisis", "static", "modelos", "clasificador-binario" )
    nlp = spacy.load(model_path)

    model_path_multi = os.path.join(os.getcwd(),"analisis", "static", "modelos", "clasificador-multi" )
    nlp_multi = spacy.load(model_path_multi)

    # 2: Extraer textos de los archivos en la carpeta

    archivos = Archivo.objects.filter(carpeta = carpeta)
    for archivo in archivos:
        file = archivo.arch
        with file.open("r") as f: 
            lines = f.read().splitlines()

        # TODO : chequear si el archivo es de wpp o no.

        docs_binarios = list(nlp.pipe(lines))
        violentos_text = []
        violentos_index = {}

        for index, doc in enumerate(docs_binarios):
            print(doc.cats)
            if doc.cats['Violento']> 0.8:
                if doc.text not in violentos_index:
                    violentos_index[doc.text] = [index + 1]
                else:
                    violentos_index[doc.text].append(index + 1)
                violentos_text.append(doc.text)
            else: 
                texto = doc.text
                detectado = 'No Violento'
                html = ""
                archivo_origen = archivo
                numero_linea = index + 1
                Resultado(texto= texto, detectado = detectado, html = html, numero_linea = numero_linea, analisis = analisis, archivo_origen = archivo_origen).save()
                
        

        docs_multi = list(nlp_multi.pipe(violentos_text))

        # 3: Armar el objeto resultado de cada uno:
        for doc in docs_multi:
            texto = doc.text
            detectado = max(doc.cats, key=doc.cats.get)
            html = "" #Como no hay displacy predeterminado es mejor directamente armar la tabla en el template.
            archivo_origen = archivo
            numero_linea = violentos_index[doc.text].pop(0)

            Resultado(texto= texto, detectado = detectado, html = html, numero_linea = numero_linea, analisis = analisis, archivo_origen = archivo_origen).save()

    # 4: Procesar los resultados y armar el informe segun el modelo que sea
    # analisis.informe = armar_informe_clasificador(analisis)
    analisis.save() 
    return 1
    


def armar_informe_clasificador():
    pass