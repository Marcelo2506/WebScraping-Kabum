import pandas as pd
import numpy as np

df = pd.read_csv("produtos.csv", sep=";")

df.head()

df.shape

df.info()

df1 = df[['nome', 'preco', 'parcela']]

print(repr(df1['preco'].iloc[0]))

df = df.copy()
df1['preco'] = (
    df1['preco']
    .str.replace('\xa0', '', regex=False)
    .str.replace('R$', '', regex=False)
    .str.replace('.', '', regex=False)
    .str.replace(',', '.', regex=False)
    .astype(float)
)

df1[['qtd_parcelas', 'valor_parcelas']
    ] = df1['parcela'].str.split(' ', n=1, expand=True)

df1 = df1.copy()
df1['qtd_parcelas'] = (
    df1['qtd_parcelas']
    .str.replace('x', '', regex=False)
    .astype(int)
)

df1 = df1.copy()
df1['valor_parcelas'] = (
    df1['valor_parcelas']
    .str.replace('de', '', regex=False)
    .str.replace('R$', '', regex=False)
    .str.replace(' ', '', regex=False)
    .str.replace('.', '', regex=False)
    .str.replace(',', '.', regex=False)
    .astype(float)
)

df1['Valor Total Parcelado'] = df1['qtd_parcelas'] * df1['valor_parcelas']

partes = df1['nome'].str.split(' ', n=2)


def juntar_partes(lista_de_partes):
    if isinstance(lista_de_partes, list):
        return ' '.join(lista_de_partes[:2])
    return np.nan  # Ou outra forma de lidar com valores que não são listas


df1['Categorias'] = partes.apply(juntar_partes)

print(df1)
