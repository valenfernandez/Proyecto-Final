Seguir los pasos que se encuentran en: [https://labelstud.io/guide/export.html#spaCy](https://labelstud.io/guide/export.html#spaCy).

En concreto:

1. Exportar de Label Studio en formato CONLL2003.

2. Cambiar la primer línea en el archivo .conll por la siguiente:
    
    `-DOCSTART- -X- O O`

3. Desde la línea de comandos convertir el archivo .conll a .spacy:

    `spacy convert /path/to/<filename>.conll -c conll .`

Con eso ya estamos listos para entrenar. Para eso vamos a consultar la
documentación de spaCy al respecto: [https://spacy.io/usage/training#quickstart](https://spacy.io/usage/training#quickstart).

Comandos de spaCy importantes:

1. `python -m spacy init fill-config base_config.cfg config.cfg`

2. `python -m spacy train config.cfg --output ./output --paths.train dataset_train.spacy --paths.dev dataset_validation.spacy`

Para hacer split entre train/test/validación se puede separar el archivo CONLL
cada doble salto de línea (\\n\\n), obviando la primera línea del mismo. Luego
se podría hacer un shuffle y armar los archivos correspondientes de acuerdo a
la distribución que se quiera lograr.

