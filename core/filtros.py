import pandas as pd

def filtrar_por_bairro(df: pd.DataFrame, coluna_bairro: str, bairro: str) -> pd.DataFrame:
    if bairro == "TODOS":
        return df
    return df[df[coluna_bairro] == bairro]

def filtrar_por_area(df: pd.DataFrame, coluna_area: str, area: str) -> pd.DataFrame:
    if area == "TODOS":
        return df
    return df[df[coluna_area] == area]