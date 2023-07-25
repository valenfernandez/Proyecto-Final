import pandas as pd

def extraer_subreddits(subreddits, reddit_file):
    """Extrae los subreddits de una lista de subreddits.

    Parameters
    ----------
    subreddits : list
        Lista de subreddits.

    Returns
    -------
    list
        Lista de frases extraidas de los subrredits.
    """
    pass


from pyarrow.parquet import ParquetFile
import pyarrow as pa 

pf = ParquetFile('RC_2012-01.parquet') 
# first_rows = next(pf.iter_batches(batch_size = 10000)) 
# df = pa.Table.from_batches([first_rows]).to_pandas() 

df = pa.Table.to_pandas(pf.read(columns=['subreddit', 'body'])) 

arg_df = df[df["subreddit"] == 'argentina' ]

for index, row in arg_df.iterrows():
    print(row.loc["body"])