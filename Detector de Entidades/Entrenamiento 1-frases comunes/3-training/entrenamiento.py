def conll_as_list(f, get_header=True):
    if get_header:
        header = next(f)
    lines = f.read().split("\n\n")
    return header, lines

def train_test(f, train_num): # cambiar el train_num por un porcentaje

    header, lines = conll_as_list(f)
    train = lines[:train_num]
    test = lines[train_num:]

    with open('train.conll', 'w') as file:
        file.write(header)
        for item in train:
            file.write(str(item) + '\n\n')  # no se si aca serian uno o dos /n
    
    with open('test.conll', 'w') as file:
        file.write(header)
        for item in test:
            file.write(str(item) + '\n\n')  # no se si aca serian uno o dos /n

#python entrenamiento.py train_test frases_comunes.conll 1800
#spacy convert C:\path\test.conll C:\OutputPath\ -c conll
#spacy convert C:\path\train.conll C:\OutputPath\ -c conll

