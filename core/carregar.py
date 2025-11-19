# core/load_data.py
import streamlit as st
import pandas as pd
import geopandas as gpd
from pathlib import Path
from utils.dics import recife
from utils.defsbase import limpar_acento

DATA_DIR = Path("dados")

@st.cache_data
def load_cad_data(path: str | None = None) -> pd.DataFrame:
    if path is None:
        path = DATA_DIR / "Cadastrados.xlsx"
    df = pd.read_excel(path)
    df['bairro'] = df['bairro'].apply(limpar_acento).str.upper()
    return df.query('bairro in @recife')

@st.cache_data
def load_geo(path: str | None = None) -> gpd.GeoDataFrame:
    if path is None:
        path = DATA_DIR / "Infopbruto.geojson"
    return gpd.read_file(path, engine="pyogrio")

@st.cache_data
def load_teatros(path: str | None = None) -> pd.DataFrame:
    if path is None:
        path = DATA_DIR / "teatros.xlsx"
    df = pd.read_excel(path)
    return df

@st.cache_data
def load_sic(path: str | None = None) -> pd.DataFrame:
    if path is None:
        path = DATA_DIR / "SIC.xlsx"
    df = pd.read_excel(path)
    return df
