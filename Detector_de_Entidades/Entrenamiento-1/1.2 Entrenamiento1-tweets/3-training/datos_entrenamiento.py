import random 

def conll_as_list(f, get_header=True):
    if get_header:
        header = next(f)
    lines = f.read().split("\n\n")
    return header, lines

def train_test(f, ratio): 
    header, lines = conll_as_list(f)
    train_num = int(len(lines)*ratio)
    random.shuffle(lines)
    train = lines[:train_num]
    test = lines[train_num:]

    with open('train.conll', 'w', encoding="utf-8") as file:
        file.write(header)
        for item in train:
            file.write(str(item) + '\n\n')  
    
    with open('test.conll', 'w', encoding="utf-8") as file:
        file.write(header)
        for item in test:
            file.write(str(item) + '\n\n')  

#Convertir conll a .spacy:
#spacy convert C:\Users\Valentina\Downloads\test.conll C:\Users\Valentina\Downloads\ -c conll
#spacy convert C:\path\train.conll C:\OutputPath\ -c conll

#Entrenamiento:
#python -m spacy train config.cfg --output ./output --paths.train train.spacy --paths.dev test.spacy

train_test(open('../2-datasets etiquetados/tweets.conll', encoding="utf-8"), 0.8)
 