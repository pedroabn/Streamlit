# 📍 **Cadastros Culturais do Recife — Dashboard Interativo**

Este projeto apresenta um **dashboard web interativo** para visualização, análise e exploração dos **Cadastros Culturais do Recife**, conectando:

* 🎭 Fazedores de cultura
* 🗺️ Mapa georreferenciado por bairro
* 📊 Indicadores sociodemográficos
* 💰 Informações de investimentos via SIC
* 📈 Gráficos analíticos segmentados por área e território

---

# 🧱 **Arquitetura do Projeto**

A aplicação segue uma arquitetura modular dividida em camadas:

```
cultura-recife-dashboard/
│
├── app.py                  # Streamlit principal (mínimo e limpo)
│
├── core/                   # Camada de lógica e processamento
│   ├── carregar.py        # Carregamento das bases (com cache)
│   ├── metricas.py          # Cálculo das métricas e indicadores
│   ├── filtros.py          # Funções de filtragem
│
├── visuals/                # Visualizações e UI
│   ├── mapa.py             # Renderização do mapa Folium
│   ├── graficos.py         # Gráficos Plotly
│
├── utils/                  # Funções auxiliares
│   ├── defsbase.py         # Listas e dicionários de apoio
│   ├── refs.py             # Funções de limpeza de texto
│
├── dados/                   # Bases de dados
│   ├── Cadastrados.xlsx
│   ├── SIC.xlsx
│   ├── teatros.xlsx
│   ├── Infopbruto.geojson
││
└── README.md
```

---

# 📦 **Tecnologias Utilizadas**

### **Backend / Processamento**

* **Python 3.10+**
* Pandas
* GeoPandas (pyogrio)
* Folium

### **Frontend / Dashboard**

* **Streamlit**
* streamlit-folium
* Plotly Express

### **Outros**

* Branca colormap
* Unicodedata (limpeza de texto)
* Estrutura modular seguindo boas práticas Python

---

# 🚀 **Principais Funcionalidades**

### 🔎 **Filtro por Área de Atuação**

O usuário seleciona uma área cultural (ex.: Dança, Música, Cultura Popular), e todos os gráficos, mapa e indicadores são ajustados dinamicamente.

### 🏙️ **Filtro por Bairro**

Permite focar análises em territórios específicos:

* total de inscritos
* espaços sociais
* população vulnerável
* percentual de pessoas negras
* etc.

### 🗺️ **Mapa Interativo com Camadas**

O dashboard inclui:

* Cluster de fazedores por área
* Cluster total
* Polígonos dos bairros do Recife
* Equipamentos culturais (teatros)

Com controle de camadas agrupadas via **GroupedLayerControl**.

### 📊 **Gráficos Analíticos**

O dashboard exibe:

* Investimentos ao longo dos anos (SIC)
* Top 5 bairros com mais cadastrados por área
* Top áreas dentro de um bairro
* Scatter de espaços de convivência

### 🧮 **Métricas instantâneas**

O sistema calcula automaticamente:

* Nº de cadastrados
* Bairro mais presente
* Idade média
* % de inscritos no bairro
* % de pessoas negras
* Nº de escolas, praças e equipamentos

---

# ⚙️ **Como Rodar Localmente**

### 1. Clone o repositório

```bash
git clone https://github.com/seu-usuario/cultura-recife-dashboard.git
cd cultura-recife-dashboard
```

### 2. Crie o ambiente virtual

```bash
python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Coloque suas bases na pasta `/dados`

```
dados/
 ├── Cadastrados.xlsx
 ├── SIC.xlsx
 ├── teatros.xlsx
 └── Infopbruto.geojson
```

### 5. Execute o Streamlit

```bash
streamlit run app.py
```

---

# 🌐 **Deploy (Streamlit Cloud)**

O projeto está configurado para deploy rápido graças à nova estrutura modular e ao uso intensivo de `@st.cache_data`.

Certifique-se de incluir no repositório:

* `requirements.txt`
* pasta `data/` com arquivos **não muito grandes**
* `pyogrio` para leitura do GeoJSON

---

# 🧩 **Detalhes da Arquitetura Modular**

### **1. `core/carregar.py`**

Centraliza todo carregamento, sempre com `cache_data`, evitando que o app rode operações pesadas no startup.

### **2. `core/metricas.py`**

Contém:

* `dict_area()` → métricas gerais da área selecionada
* `dados_Area_bairro()` → métricas específicas para o bairro

Ambas livres de dependências globais.

### **3. `visuals/mapa.py`**

Um arquivo único dedicado ao Folium:

* performance otimizada
* clusters separados por área
* controle de camadas
* GeoJSON renderizado apenas quando necessário

### **4. `visuals/graficos.py`**

Todos os gráficos Plotly isolados, facilitando manutenção e expansão.

### **5. `utils/`**

Funções de suporte, como:

* limpeza de acentos
* dicionários de mapeamento
* listas de bairros do Recife

---

# 🧪 **Testabilidade**

A divisão modular permite testar:

* filtros isoladamente
* cálculos de métricas sem Streamlit
* gráficos com DataFrames sintéticos
* carregamento de dados via mocks

---

# 🔧 **Extensões Futuras**

* Conectar ao banco de dados em vez de XLSX
* Criar API para atualização automática
* Adicionar séries temporais de métricas culturais
* Adicionar painel de indicadores municipais (ODS, SDG, IPVU)
* Integrar com dados de eventos da PCR

---

# 📄 **Licença**

Este projeto é distribuído sob a licença MIT — uso livre e aberto.

---

# 🤝 **Contribuições**

Pull requests são bem-vindos!
Sugestões de melhorias, novas métricas ou novos datasets culturais podem ser submetidos através das Issues.
