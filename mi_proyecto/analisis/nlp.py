from .models import Analisis, Aplicacion, Resultado, Modelo, Carpeta, Archivo, Preferencias
import json
import spacy
from spacy import displacy
import os
import pandas as pd
import altair as alt


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
        raise Exception("El modelo no existe") #podria cambiar esto, intentar cargar el modelo y si no existe tirar un error. Y pasar a hacer un procesamiento 'generico' que no dependa de un modelo en particular.


def procesar_entidades(analisis, carpeta, user):
    
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
        file = archivo.arch
        with file.open("r") as f: #TODO chequear 
            lines = f.read().splitlines()
        docs = list(nlp.pipe(lines))

        # 3: Armar el objeto resultado de cada uno:
        for doc in docs:

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
            numero_linea = 0 # sería la posicion en el vector capaz
            Resultado(texto= texto, detectado = detectado, html = html, numero_linea = numero_linea, analisis = analisis, archivo_origen = archivo_origen).save()

    # 4: Procesar los resultados y armar el informe segun el modelo que sea
    analisis.informe = armar_informe_entidades(analisis)
    analisis.save() 
    return 1

def armar_informe_entidades(analisis): 
    """
    Esta funcion crea el archivo html que contiene el informe de los resultados de un analisis creado por un modelo de deteccion de entidades.

    Parameters
    ----------
    :param: analisis (Analisis) Es un analisis realizado previamente que ya tiene resultados asociados, de los cuales se quiere crear un informe.

    Return
    ------
    informe (str) Es un string que contiene el html del informe.

    """
    #seria generar un html con el resumen, los graficos y estadisticas.
    #se podria usar altair 

    html_template = """
            <h4>Informe de Entidades</h4>
            <script type="text/javascript">
                var chart = {{ chart|safe }};
                vegaEmbed('#vis1', chart).then(result => console.log(result)).catch(console.warn);
            </script>
        """
    resultados = Resultado.objects.filter(analisis = analisis)
    
    domain =["DINERO", "FECHA", "HORA", "LUGAR", "MEDIDA", "MISC", "ORG", "PERSONA", "TIEMPO"]
    range_AM= ["#00065D","#2706AD","#5C40D0","#889AFD", "#CCC5B2","#F3D850","#FFD500","#9A7300", "#DFA000"]
    range_AR= ["#00065D", "#2257EC","#008DDE","#7A8BE6","#D2C3C3","#FF9696","#F94D67","#E9255A","#99001C"]
    
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

    #total_entidades = df.shape[0]
    #entidades_counts = df['label'].value_counts() # esto devuelve un objeto de pandas que tiene como indice los tipos de #entidades y como valor la cantidad de veces que aparece cada uno. numero de resultados de cada tipo de entidad.
    #ent_text_counts = df['text'].value_counts() #entidades que se repitan: tendrian el count en mas de 1

    domain =['PER','LOC','MISC','ORG']
    range_= ['#00065D','#99001C','#F94D67','#D2C3C3'] #mi range va a cambiar segun el 

    # Create an Altair chart
    chart = alt.Chart(df, title="Distribucion de entidades").mark_bar().encode(
        x = alt.X('label:N', title='Entidades'),
        y = alt.Y('count():Q', title='N° Apariciones'),
        color = alt.Color('label', scale = alt.Scale(domain=domain, range=range_AR))
    ).to_html()
    
    #.to_json(indent=None)
    
    print(chart)

    informe = html_template.format(chart=chart)

    return informe



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