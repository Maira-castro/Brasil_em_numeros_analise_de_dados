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

Responsável por transformar os dados brutos retornados pela API do IBGE em um DataFrame pronto para análise.

### Funções disponíveis

#### json_para_df(payload)

Converte o JSON retornado pela API em um DataFrame pandas.

##### Tratamentos realizados

- Extração dos dados da estrutura JSON.
- Conversão dos valores para tipo numérico.
- Remoção de valores inválidos ("..." e "-").
- Tratamento de erros de conversão com `pd.to_numeric()`.
- Remoção de valores nulos com `dropna()`.

##### Exemplo de uso

```python
from limpeza import json_para_df

df = json_para_df(populacao)
```

##### Saída esperada

| uf_id | nome | ano | valor |
|--------|--------|--------|--------|
| 23 | Ceará | 2025 | 9268836.0 |

---

#### juntar_regiao(df, estados)

Adiciona ao DataFrame a região de cada estado utilizando os dados retornados pela função `buscar_estados()`.

##### Exemplo de uso

```python
from limpeza import juntar_regiao

df = juntar_regiao(df, estados)
```

##### Saída esperada

| uf_id | nome | ano | valor | regiao |
|--------|--------|--------|--------|--------|
| 23 | Ceará | 2025 | 9268836.0 | NE |

---

### Fluxo de utilização

```python
from ingestao import buscar_estados, buscar_indicador_populacao
from limpeza import json_para_df, juntar_regiao

estados = buscar_estados()
populacao = buscar_indicador_populacao()

df = json_para_df(populacao)
df = juntar_regiao(df, estados)

print(df.head())
```

### Resultado

Ao final da etapa de limpeza, os dados ficam estruturados em um DataFrame contendo:

- `uf_id` → código da Unidade Federativa.
- `nome` → nome do estado.
- `ano` → ano do indicador.
- `valor` → valor numérico da população.
- `regiao` → sigla da região brasileira (N, NE, CO, SE, S).

Esta etapa garante que os dados estejam limpos, consistentes e prontos para as etapas de agregação, cálculo de KPIs e geração de gráficos Plotly.