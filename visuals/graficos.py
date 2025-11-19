# visuals/graficos.py
import pandas as pd
import plotly.express as px

from utils.defsbase import limpar_acento
from utils.refs import dic_sic_cad

def graph_cad(base: pd.DataFrame, area_a: str, bairro_select: str):
    df = base.copy()
    df["bairros_cep"] = (
        df["bairros_cep"]
        .apply(limpar_acento)
        .str.upper()
        .replace(
            {
                "COHAB": "COHAB - IBURA DE CIMA",
                "SÍTIO DOS PINTOS": "SÍTIO DOS PINTOS - SÃO BRÁS",
            }
        )
    )

    if area_a != "TODOS":
        df = df[df["area_atuacao"] == area_a]

    dff = (
        df.groupby(["bairros_cep", "area_atuacao"])
        .agg(cadastros=("nome", "size"))
        .reset_index()
    )
    dff = dff.sort_values(by="cadastros", ascending=False).head(5)

    fig = px.bar(
        dff,
        x="bairros_cep",
        y="cadastros",
        text_auto="cadastros",
        title=f"Top 5 bairros com mais cadastrados em {area_a}",
        labels={"bairros_cep": "Bairros", "cadastros": "Quantidade de cadastrados"},
    )
    cores = ["#494cfd" if b != bairro_select else "#d62727" for b in dff["bairros_cep"]]
    fig.update_traces(marker_color=cores)
    return fig


def graph_cad_por_bairro(base: pd.DataFrame, area_a: str, bairro_select: str):
    df = base.copy()
    df["bairros_cep"] = (
        df["bairros_cep"]
        .apply(limpar_acento)
        .str.upper()
        .replace(
            {
                "COHAB": "COHAB - IBURA DE CIMA",
                "SÍTIO DOS PINTOS": "SÍTIO DOS PINTOS - SÃO BRÁS",
            }
        )
    )

    dff = (
        df.groupby(["bairros_cep", "area_atuacao"])
        .agg(cadastros=("nome", "size"))
        .reset_index()
    )
    dff = dff.sort_values(by="cadastros", ascending=False).head(3)

    fig = (
        px.bar(
            dff,
            y="area_atuacao",
            x="cadastros",
            orientation="h",
            title=f"Top áreas de atuação com mais cadastrados em {bairro_select}",
            text_auto="cadastros",
            labels={
                "cadastros": "Quantidade de cadastrados",
                "area_atuacao": "Área de atuação",
            },
        )
        .update_yaxes(type="category", categoryorder="category ascending")
    )

    cores = ["#494cfd" if a != area_a else "#d62727" for a in dff["area_atuacao"]]
    fig.update_traces(marker_color=cores)
    return fig


def graf_scatter(df_bairros: pd.DataFrame, bairro_select: str):
    df = df_bairros.copy()
    cols = ["n_escolas", "qtd_Pracas", "Qtd_equipamentos", "compaz"]
    df["conv_social"] = df[cols].fillna(0).sum(axis=1)

    fig = px.scatter(
        df,
        x="inscritos",
        y="total_pessoas",
        title=(
            "Nº de Cadastrados por Nº total de pessoas "
            "e Espaços de convivência"
        ),
        size="conv_social",
        hover_name="EBAIRRNOMEOF",
        labels={},
    )
    cores = [
        "#494cfd" if b != bairro_select else "#d62727"
        for b in df["EBAIRRNOMEOF"]
    ]
    fig.update_traces(marker_color=cores)
    return fig


def graph_locais(sic_df: pd.DataFrame, area_a: str):
    df = sic_df.copy()
    # Mapeia estilos
    df["Estilo"] = df["Estilo"].map(dic_sic_cad)
    df["ano"] = pd.to_datetime(df["ano"], unit="D", origin="1899-12-30").dt.year

    df = (
        df.groupby(["Estilo", "ano"], as_index=False)
        .agg(inv=("valor", "sum"), projetos=("projeto", "size"))
        .sort_values(by="ano", ascending=False)
    )

    if area_a != "TODOS":
        df = df[df["Estilo"] == area_a]

    fig = (
        px.histogram(
            df,
            x="ano",
            y="inv",
            text_auto=True,
            labels={"ano": "Ano", "inv": "Investimento"},
            title=f"Investimento da área no SIC ao longo dos anos: {area_a}",
        )
        .update_xaxes(
            type="category", title_text="Ano", categoryorder="category ascending"
        )
    )

    return fig
