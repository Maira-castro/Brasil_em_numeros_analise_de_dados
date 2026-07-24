from fastapi import APIRouter, Depends
from dependencies import get_dashboard, juntar_df_final
from graficos import grafico_evolucao, grafico_ranking_estados, grafico_regiao

import json

dashboard_router = APIRouter()


def converter_figura(fig):

    json_fig = fig.to_json()

    if json_fig is None:
        return {}

    return json.loads(json_fig)


def gerar_dashboard(df):

    ano = int(df["ano"].max())

    figuras = {

        "evolucao": converter_figura(
            grafico_evolucao(df)
        ),

        "ranking": converter_figura(
            grafico_ranking_estados(
                df,
                ano
            )
        ),

        "regiao": converter_figura(
            grafico_regiao(
                df,
                ano
            )
        )
    }

    return figuras




@dashboard_router.get("/dashboard")
def dashboard(
    dados = Depends(get_dashboard)
):
    return dados

@dashboard_router.get("/graficos")
def graficos(
    df = Depends(juntar_df_final)
):

    figuras = gerar_dashboard(df)

    print(type(figuras))
    print(figuras.keys())


    return {
        "graficos": figuras
    }
