# Brasil em Números - Análise de Dados

Pipeline que transforma dados públicos do IBGE em gráficos Plotly para o dashboard.

## Setup do ambiente

É necessário ter a pasta `.venv` no projeto. Se não tiver, crie:

```
python -m venv .venv
```

Ative o ambiente virtual:

**Windows:**
```
.venv\Scripts\activate
```

**Mac/Linux:**
```
source .venv/bin/activate
```

Instale as bibliotecas:

```
pip install -r requirements.txt
```

O `requirements.txt` já está no repositório com:

```
requests
pandas
plotly
fastapi
uvicorn
```

## Estrutura do pipeline

```
Ingestão → Limpeza → Agregação/KPIs → Figura Plotly
(IBGE)     (pandas)   (pandas)         (o que o React exibe)
```

## Ingestão (`ingestao.py`)

Responsável por buscar os dados crus da API do IBGE, sem chave, em português.

Duas funções disponíveis:

### `buscar_estados()`

Busca a lista de estados (UFs), usada pra depois juntar a região de cada estado com os indicadores.

```python
from ingestao import buscar_estados

estados = buscar_estados()
```

Retorna uma lista de dicionários, um por estado:

```python
[
  {"id": 11, "sigla": "RO", "nome": "Rondônia", "regiao": {"id": 1, "sigla": "N", "nome": "Norte"}},
  ...
]
```

### `buscar_indicador_populacao()`

Busca o indicador de população (agregado 6579, variável 9324), último período, todos os estados.

```python
from ingestao import buscar_indicador_populacao

populacao = buscar_indicador_populacao()
```

Retorna o JSON cru do IBGE, ainda **aninhado** — quem for fazer a limpeza precisa navegar até `populacao[0]["resultados"][0]["series"]` pra chegar na lista de estados com seus valores. Cada item de `series` tem:

```python
{
  "localidade": {"id": "23", "nome": "Ceará"},
  "serie": {"2025": "9268836"}
}
```





## Limpeza (limpeza.py)

Responsável por transformar os dados brutos retornados pelas APIs do IBGE em DataFrames organizados e prontos para análise.

## Funções disponíveis

### json_para_df(payload)

Converte o JSON retornado pela API de população em um DataFrame pandas.

### Tratamentos realizados:
- Extração dos dados da estrutura JSON.
- Conversão dos valores para tipo numérico.
- Remoção de valores inválidos ("..." e "-").
- Tratamento de erros de conversão com pd.to_numeric().
- Remoção de valores nulos com dropna().

---

### limpar_estados(estados)

Transforma os dados brutos da API de estados em um DataFrame organizado.

### Tratamentos realizados:
- Extração do ID do estado.
- Extração da sigla e nome do estado.
- Extração da região brasileira.
- Conversão do ID para tipo numérico.

Saída esperada:

| uf_id | sigla | nome_estado | regiao |
|---|---|---|---|
| 23 | CE | Ceará | NE |

---

### juntar_regiao(df, df_estados)

Realiza a junção entre os dados de população e os dados dos estados utilizando o campo `uf_id`.

Saída esperada:

| uf_id | nome | ano | valor | regiao |
|---|---|---|---|---|
| 23 | Ceará | 2025 | 9268836.0 | NE |

---

## Fluxo de utilização

```python
from ingestao import buscar_estados, buscar_indicador_populacao
from limpeza import json_para_df, limpar_estados, juntar_regiao

estados = buscar_estados()
populacao = buscar_indicador_populacao()

df_estados = limpar_estados(estados)

df = json_para_df(populacao)

df = juntar_regiao(df, df_estados)

print(df.head())
