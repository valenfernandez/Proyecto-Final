import json
import random


def labelstudio_to_list(file):
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

    #TODO> CHEQUEAR QUE EL FORMATO DEL JSON SEA CORRECTO (ese formato es : {}{}{} )
    #  Y PUEDA SER CONVERTIDO A .SPACY Y LUEGO SE PUEDA ENTRENAR o Si tenemos que 
    # cambiar el write de los json para que esten en formato: [{},{}]

    train_num = int(len(lines)*ratio)
    random.shuffle(lines)
    train = lines[:train_num]
    test = lines[train_num:]
    with open('train.json', 'w', encoding="utf-8") as file:
        for item in train:
            file.write(json.dumps(item, ensure_ascii=False) + "\n")  
    
    with open('test.json', 'w', encoding="utf-8") as file:
        for item in test:
            file.write(json.dumps(item, ensure_ascii=False) + "\n")  
    

file = 'datos-min.json'
lines = labelstudio_to_list(file)
train_test(lines, ratio = 0.7)
