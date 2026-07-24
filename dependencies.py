from fastapi import Depends
from ingestao import buscar_estados, buscar_indicador_populacao
from limpeza import limpar_populacao, limpar_estados, juntar_regiao
from agregacao import preparar

URL_ESTADO = 'https://servicodados.ibge.gov.br/api/v1/localidades/estados?orderBy=nome'
URL_POPULACAO = 'https://servicodados.ibge.gov.br/api/v3/agregados/6579/periodos/-1/variaveis/9324?localidades=N3[all]'

def ingestao_estados():
    return buscar_estados(URL_ESTADO)



def ingestao_populacao():
    return buscar_indicador_populacao(URL_POPULACAO)



def limpeza_df_populacao(
    populacao = Depends(ingestao_populacao)
):
    return limpar_populacao(populacao)



def limpeza_df_estados(
    estados = Depends(ingestao_estados)
):
    dados = limpar_estados(estados)
    # print(dados.to_string())
    return dados



def juntar_df_final(
    df_pop = Depends(limpeza_df_populacao),
    df_estados = Depends(limpeza_df_estados)
):
    return juntar_regiao(df_pop, df_estados)



def get_dashboard(
    df = Depends(juntar_df_final)
):
    df, kpis = preparar(df)

    return {
        "dados": df.to_dict(orient="records"),
        "kpis": kpis
    }