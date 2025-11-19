import pandas as pd
import unicodedata
from dics import dic_sic_cad

def colgate(df):
    df = df.copy()  # segurança nível 1
    # Mapeia estilos
    df['Estilo'] = df['Estilo'].map(dic_sic_cad)
    # Converte número de série do Excel -> datetime -> ano
    df['ano'] = (
        pd.to_datetime(df['ano'], unit='D', origin='1899-12-30').dt.year
    )
    df = (df
            .groupby(["Estilo", "ano"], as_index=False)
            .agg(
                inv = ('valor', sum),
                projetos = ('projeto','size')
            ).sort_values(by='ano', ascending=False))
    return df

def limpar_acento(txt):
    if pd.isnull(txt):
        return txt
    txt = ''.join(ch for ch in unicodedata.normalize('NFKD', txt) 
        if not unicodedata.combining(ch))
    return txt