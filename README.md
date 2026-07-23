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