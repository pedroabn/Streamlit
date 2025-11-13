# 📍 Cadastros Culturais do Recife — Dashboard Interativo

Este projeto apresenta um **sistema de visualização interativa** dos Cadastros Culturais do Recife utilizando:

- **Streamlit** para interface web  
- **Folium** para mapa interativo  
- **Pandas** para tratamento de dados  
- **Plotly** (opcional) para gráficos  
- **Folium plugins** para clusters, camadas e MiniMap  

O objetivo principal é permitir a exploração dos cadastros culturais por **área de atuação** e **bairro**, exibidos em um mapa dinâmico com múltiplas camadas temáticas.

---

## 🗂️ Estrutura Geral

O arquivo `main.py` é responsável por:

1. Carregar as bases de dados  
2. Construir a barra lateral de filtros  
3. Gerar indicadores descritivos da área selecionada  
4. Renderizar o mapa Folium dentro do Streamlit  
5. (Opcional) Exibir análises complementares e gráficos  

---

## 📦 Bibliotecas Utilizadas

- `streamlit`
- `pandas`
- `plotly.express`
- `folium`
- `streamlit_folium`
- `branca.colormap`
- `datetime`

---

## 📁 Carregamento das Bases

O sistema utiliza três planilhas:

- **Infopbruto.xlsx** — Informações agregadas por bairro  
- **teatros.xlsx** — Equipamentos culturais georreferenciados  
- **Cadastrados.xlsx** — Base principal dos inscritos  

Para otimizar, o carregamento da base principal usa `@st.cache_data`.

---

## 🎛 Sidebar — Filtros Interativos

A aplicação permite filtrar os inscritos por:

- **Área de atuação**
- **Bairro**

A seleção atualiza automaticamente:

- O mapa  
- Os indicadores resumidos  
- O conjunto total de marcadores  

Trecho responsável:

```python
area_a = st.selectbox("Area de atuação", df["area_atuacao"].sort_values().unique())
bairro = st.selectbox("Bairro", df["EBAIRRNOMEOF"].sort_values().unique())
