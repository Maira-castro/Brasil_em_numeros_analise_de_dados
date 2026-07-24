from fastapi import Depends
from ingestao import buscar_estados, buscar_indicador_populacao
from limpeza import transformar_json_em_df, limpar_estados, juntar_regiao
from agregacao import preparar



def ingestao_estados():
    return buscar_estados()



def ingestao_populacao():
    return buscar_indicador_populacao()



def limpeza_df_populacao(
    populacao = Depends(ingestao_populacao)
):
    return transformar_json_em_df(populacao)



def limpeza_df_estados(
    estados = Depends(ingestao_estados)
):
    return limpar_estados(estados)



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
        # "dados": df.to_dict(orient="records"),
        "kpis": kpis
    }