import pandas as pd

df1 = pd.read_csv(
    'produtos.csv', sep=";")

print(df1.head())
