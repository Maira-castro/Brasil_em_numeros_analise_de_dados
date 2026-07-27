from fastapi import APIRouter, Depends, HTTPException
from dependencies import buscar_df_final
from agregacao import preparar
from graficos import grafico_evolucao, grafico_ranking_estados, grafico_regiao
from enum import Enum


import json

dashboard_router = APIRouter()


class TipoGrafico(str, Enum):
    evolucao = "evolucao"
    ranking = "ranking"
    regiao = "regiao"


class Regiao(str, Enum):
    brasil = "Brasil"
    norte = "N"
    nordeste = "NE"
    centro_oeste = "CO"
    sudeste = "SE"
    sul = "S"


def converter_figura(fig):
    figura = fig.to_dict()

    for trace in figura["data"]:
        for eixo in ("x", "y", "z"):
            if eixo in trace and hasattr(trace[eixo], "tolist"):
                trace[eixo] = trace[eixo].tolist()

    return figura


def gerar_dashboard(
    df,
    tipo_grafico="evolucao",
    regiao="Brasil",
    ano=None,
    ano_inicio=None,
    ano_fim=None
):
    """
    Gera o gráfico e os KPIs conforme o tipo e a região.
    """

    # Filtra os dados e calcula os KPIs
    df, kpis = preparar(df, regiao)

    # Se foi informado um ano, filtra
    if ano is not None:
        df = df[df["ano"] == ano]

    # Caso não existam dados
    if df.empty:
        return {
            "indicador": "populacao",
            "regiao": regiao,
            "figura": None,
            "kpis": kpis
        }

    if ano is None:
        ano = int(df["ano"].max())

    # Escolhe qual gráfico gerar
    if tipo_grafico == "evolucao":

        if ano_inicio is None or ano_fim is None:
            raise ValueError(
                "Para o gráfico de evolução informe ano_inicio e ano_fim."
            )

        fig = grafico_evolucao(
            df,
            ano_inicio,
            ano_fim
        )

    elif tipo_grafico == "ranking":

        fig = grafico_ranking_estados(
            df,
            ano
        )

    elif tipo_grafico == "regiao":

        fig = grafico_regiao(
            df,
            ano
        )

    else:
        raise ValueError(
            "Tipo de gráfico inválido. Utilize: evolucao, ranking ou regiao."
        )
    
    figura = converter_figura(fig) 

    print(figura["data"][0]["x"])
    print(figura["data"][0]["y"])
    
    return {
        "indicador": "populacao",
        "tipo": tipo_grafico,
        "regiao": regiao,
        "ano": ano,
        "figura": figura,
        "kpis": kpis
    }


@dashboard_router.get("/graficos")
def graficos(
    tipo: TipoGrafico = TipoGrafico.evolucao,
    regiao: Regiao = Regiao.brasil,
    ano: int | None = None,
    ano_inicio: int | None = None,
    ano_fim: int | None = None,
    df=Depends(buscar_df_final)
):
    try:

        return gerar_dashboard(
            df=df,
            tipo_grafico=tipo.value,
            regiao=regiao.value,
            ano=ano,
            ano_inicio=ano_inicio,
            ano_fim=ano_fim
        )

    except ValueError as e:

        raise HTTPException(
            status_code=400,
            detail=str(e)
        )