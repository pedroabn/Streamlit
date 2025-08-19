# Vamos gerar um app Streamlit completo e um CSV de exemplo para você testar localmente.
# Arquivos que serão criados:
# - /mnt/data/app_times_streamlit.py
# - /mnt/data/exemplo_jogadores.csv

# import os, textwrap, pandas as pd

# app_code = app_times_streamlit.py
# -----------------------------------------------------------
# App Streamlit para montar 4 times balanceados (1 por nível 1..5)
# Autor: ChatGPT (GPT-5 Thinking)
# Requisitos: pip install streamlit pandas
# Execução:   streamlit run app_times_streamlit.py

from dataclasses import dataclass
from typing import Dict, List, Tuple
from collections import defaultdict
import streamlit as st
import pandas as pd
import openpyxl
import io
import json

st.set_page_config(page_title="Times Balanceados (4x5)", layout="wide")

# =====================
# 1) Modelagem e regras
# =====================

@dataclass(frozen=True)
class Player:
    nome: str
    nivel: Dict[str, int]  # {"classificacao":1..5, "sub":1..5}


def validar_elenco(df: pd.DataFrame, n_times: int = 4, n_classes: int = 5) -> Tuple[bool, Dict[int,int], Dict[int,int]]:
    """
    Checa se há exatamente n_times jogadores em cada classificação 1..n_classes.
    Retorna (ok, faltantes_dict, excedentes_dict).
    """
    counts = df.groupby("classificacao")["nome"].count().to_dict()
    falt = {}
    exc  = {}
    for c in range(1, n_classes+1):
        qtd = counts.get(c, 0)
        if qtd < n_times:
            falt[c] = n_times - qtd
        elif qtd > n_times:
            exc[c] = qtd - n_times
    ok = (len(falt) == 0 and len(exc) == 0)
    return ok, falt, exc


def snake_distribute(rows: List[dict], team_keys: List[str], reverse_round: bool) -> Dict[str, List[dict]]:
    """
    Distribui lista de jogadores 'rows' nos times em ordem snake (ida/volta).
    """
    distrib = {k: [] for k in team_keys}
    order = list(range(len(team_keys)))
    if reverse_round:
        order = list(reversed(order))

    for idx, row in zip(order, rows):
        distrib[team_keys[idx]].append(row)
    return distrib


def montar_times_balanceados(df: pd.DataFrame, n_times: int = 4, n_classes: int = 5) -> Dict[str, List[dict]]:
    """
    Estratégia:
      - Para cada classificação (1..5), ordenar por sub desc
      - Distribuir em snake draft alternando a direção a cada classificação
    """
    ok, falt, exc = validar_elenco(df, n_times=n_times, n_classes=n_classes)
    if not ok:
        msgs = []
        if falt:
            msgs.append("Faltando jogadores por classificação: " + ", ".join([f"{c} (faltam {k})" for c,k in falt.items()]))
        if exc:
            msgs.append("Excedentes por classificação: " + ", ".join([f"{c} (+{k})" for c,k in exc.items()]))
        raise ValueError("Elenco incompatível com balanceamento perfeito. " + " | ".join(msgs))

    team_keys = [f"Time {i+1}" for i in range(n_times)]
    times = {k: [] for k in team_keys}

    reverse_round = False
    for c in range(1, n_classes+1):
        bloco = df[df["classificacao"] == c].sort_values("sub", ascending=False).copy()
        rows = bloco.to_dict(orient="records")
        part = snake_distribute(rows, team_keys, reverse_round)
        # agregar ao dicionário final
        for tk in team_keys:
            times[tk].extend(part[tk])
        reverse_round = not reverse_round

    return times


def metricas_times(times: Dict[str, List[dict]]) -> pd.DataFrame:
    data = []
    for t, elenco in times.items():
        soma_sub = sum(p["sub"] for p in elenco)
        media_sub = soma_sub / len(elenco) if elenco else 0.0
        data.append({"Time": t, "Jogadores": len(elenco), "Soma_Sub": soma_sub, "Media_Sub": round(media_sub, 2)})
    df = pd.DataFrame(data).sort_values("Soma_Sub", ascending=False)
    return df


# =====================
# 2) Entrada dos dados
# =====================

st.title("⚽️ Montador de Times Balanceados (4 times × 5 jogadores)")
st.caption("Cada time recebe 1 jogador por **classificação (1..5)**. O **sub** (1..5) diferencia a força dentro da mesma classificação.")

with st.sidebar:
    st.header("Entrada de dados")
    st.markdown("**Formato esperado de colunas:** `nome`, `classificacao`, `sub`.")

    uploaded = st.file_uploader("Carregar CSV ou Excel", type=["xlsx","csv"])
    usar_exemplo = st.button("Usar exemplo pronto", type="secondary")

def carregar_ou_exemplo(uploaded, usar_exemplo: bool) -> pd.DataFrame:
    if uploaded is not None:
        try:
            if uploaded.name.lower().endswith(".xlsx"):
                df = pd.read_excel(uploaded)
            else:
                df = pd.read_csv(uploaded)
        except Exception as e:
            st.error(f"Falha ao ler arquivo: {e}")
            return pd.DataFrame()
    elif usar_exemplo:
        # Gera 20 jogadores (4 por classificação, subs variados)
        rows = []
        for c in range(1, 6):
            subs = [5,4,3,2]
            for i, s in enumerate(subs, start=1):
                rows.append({"nome": f"Jogador_C{c}_#{i}", "classificacao": c, "sub": s})
        df = pd.DataFrame(rows)
    else:
        df = pd.DataFrame()
    return df

df_raw = carregar_ou_exemplo(uploaded, usar_exemplo)

def limpar_validar(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return df
    # Padroniza nomes
    df = df.rename(columns={c: c.strip().lower() for c in df.columns})
    req = {"nome", "classificacao", "sub"}
    if not req.issubset(df.columns):
        st.warning(f"Colunas faltando. Necessárias: {req}. Encontradas: {list(df.columns)}")
        return pd.DataFrame()

    df = df[list(req)].copy()
    # Remove linhas vazias
    df = df.dropna(subset=["nome", "classificacao", "sub"])

    # Coerção de tipos
    try:
        df["classificacao"] = df["classificacao"].astype(int)
        df["sub"] = df["sub"].astype(int)
    except Exception:
        st.error("Não foi possível converter 'classificacao' e 'sub' para inteiros.")
        return pd.DataFrame()

    # Regras de domínio 1..5
    mask_ok = df["classificacao"].between(1,5) & df["sub"].between(1,5)
    invalidos = df[~mask_ok]
    if not invalidos.empty:
        st.warning("Removendo linhas com valores fora do intervalo 1..5 em 'classificacao' ou 'sub'.")
        df = df[mask_ok]

    # Normaliza nomes (strip)
    df["nome"] = df["nome"].astype(str).str.strip()

    return df.reset_index(drop=True)

df = limpar_validar(df_raw)

st.subheader("📋 Dados de entrada")
if df.empty:
    st.info("Carregue um arquivo ou clique em **Usar exemplo pronto** na barra lateral.")
else:
    st.dataframe(df, use_container_width=True, hide_index=True)

# =====================
# 3) Ajustes por classe (excedentes)
# =====================

def aplicar_selecao_por_classe(df: pd.DataFrame, n_times: int = 4) -> pd.DataFrame:
    """
    Se houver mais de n_times jogadores em alguma classificação,
    permite ao usuário escolher exatamente n_times via multiselect.
    Por padrão, seleciona top n_times por 'sub' (desc).
    """
    dfs = []
    for c in range(1,6):
        bloco = df[df["classificacao"] == c].copy()
        qtd = len(bloco)
        if qtd == 0:
            # deixamos vazio; validação final apontará falta
            dfs.append(bloco)
            continue
        if qtd <= n_times:
            dfs.append(bloco)
            continue

        st.markdown(f"**Classificação {c}**: {qtd} jogadores (excedentes). Selecione {n_times}:")
        bloco = bloco.sort_values("sub", ascending=False)
        options = list(bloco.index)
        default_idxs = options[:n_times]
        key = f"selecionar_c{c}"
        sel = st.multiselect(
            f"Escolha {n_times} jogadores para a classificação {c}",
            options=options,
            default=default_idxs,
            format_func=lambda idx: f"{bloco.loc[idx,'nome']} (sub {bloco.loc[idx,'sub']})",
            key=key
        )
        if len(sel) != n_times:
            st.warning(f"Você deve selecionar exatamente {n_times}. Usando seleção padrão (top {n_times} por sub).")
            sel = default_idxs
        dfs.append(bloco.loc[sel])

    return pd.concat(dfs, axis=0).reset_index(drop=True)

st.divider()
st.subheader("🛠️ Ajustes (se houver excedentes por classificação)")
if not df.empty:
    df_aj = aplicar_selecao_por_classe(df, n_times=4)
else:
    df_aj = df

# =====================
# 4) Montagem dos times
# =====================

st.divider()
st.subheader("🧩 Montagem dos times")

if df_aj.empty:
    st.info("Carregue dados válidos para montar os times.")
else:
    ok, falt, exc = validar_elenco(df_aj, n_times=4, n_classes=5)
    if not ok:
        col1, col2 = st.columns(2)
        with col1:
            if falt:
                st.error("Faltando jogadores por classificação:")
                falt_df = pd.DataFrame([{"classificacao": c, "faltando": k} for c,k in falt.items()])
                st.dataframe(falt_df, hide_index=True, use_container_width=True)
        with col2:
            if exc:
                st.warning("Excedentes por classificação (reduza usando a seção de ajustes):")
                exc_df = pd.DataFrame([{"classificacao": c, "excedentes": k} for c,k in exc.items()])
                st.dataframe(exc_df, hide_index=True, use_container_width=True)
        st.stop()

    try:
        times = montar_times_balanceados(df_aj, n_times=4, n_classes=5)
    except Exception as e:
        st.error(str(e))
        st.stop()

    # Exibição dos times
    cols = st.columns(4)
    export_rows = []
    for i, (tname, elenco) in enumerate(times.items()):
        with cols[i]:
            st.markdown(f"### {tname}")
            tdf = pd.DataFrame(elenco).sort_values(["classificacao","sub"], ascending=[True, False])
            st.dataframe(tdf, hide_index=True, use_container_width=True)
            export_rows.extend([{**r, "time": tname} for r in elenco])

    # Métricas
    st.subheader("📈 Métricas dos times")
    met = metricas_times(times)
    st.dataframe(met, hide_index=True, use_container_width=True)
    st.bar_chart(met.set_index("Time")["Soma_Sub"])

    # Downloads
    out_df = pd.DataFrame(export_rows).sort_values(["time","classificacao","sub"], ascending=[True, True, False])
    csv_bytes = out_df.to_csv(index=False).encode("utf-8")
    json_bytes = out_df.to_json(orient="records", force_ascii=False).encode("utf-8")

    st.download_button("⬇️ Baixar CSV dos times", data=csv_bytes, file_name="times_balanceados.csv", mime="text/csv")
    st.download_button("⬇️ Baixar JSON dos times", data=json_bytes, file_name="times_balanceados.json", mime="application/json")

st.caption("Dica: Se quiser mudar a estratégia (ex.: randomizar dentro da classificação), posso adicionar um seletor no topo.")
'''

sample_csv = """nome,classificacao,sub
Jogador_C1_#1,1,5
Jogador_C1_#2,1,4
Jogador_C1_#3,1,3
Jogador_C1_#4,1,2
Jogador_C2_#1,2,5
Jogador_C2_#2,2,4
Jogador_C2_#3,2,3
Jogador_C2_#4,2,2
Jogador_C3_#1,3,5
Jogador_C3_#2,3,4
Jogador_C3_#3,3,3
Jogador_C3_#4,3,2
Jogador_C4_#1,4,5
Jogador_C4_#2,4,4
Jogador_C4_#3,4,3
Jogador_C4_#4,4,2
Jogador_C5_#1,5,5
Jogador_C5_#2,5,4
Jogador_C5_#3,5,3
Jogador_C5_#4,5,2
"""

os.makedirs("/mnt/data", exist_ok=True)
with open("/mnt/data/app_times_streamlit.py", "w", encoding="utf-8") as f:
    f.write(app_code)

with open("/mnt/data/exemplo_jogadores.csv", "w", encoding="utf-8") as f:
    f.write(sample_csv)

print("Arquivos criados:")
print("- /mnt/data/app_times_streamlit.py")
print("- /mnt/data/exemplo_jogadores.csv")
'''
