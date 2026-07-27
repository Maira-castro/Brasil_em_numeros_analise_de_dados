import plotly.express as px


def grafico_evolucao(df, ano_inicio: int, ano_fim: int):
    # Garante que o menor ano fique primeiro
    if ano_inicio > ano_fim:
        ano_inicio, ano_fim = ano_fim, ano_inicio

    # Filtra o período
    df_filtrado = df[
        (df["ano"] >= ano_inicio) &
        (df["ano"] <= ano_fim)
    ]

    # Agrupa por ano
    df_ano = (
        df_filtrado
        .groupby("ano", as_index=False)["populacao"]
        .sum()
    )

    # Cria o gráfico
    fig = px.line(
        df_ano,
        x="ano",
        y="populacao",
        markers=True,
        title=f"Evolução da população brasileira ({ano_inicio} - {ano_fim})"
    )

    fig.update_layout(
        xaxis_title="Ano",
        yaxis_title="População"
    )

    return fig



def grafico_ranking_estados(df, ano):

    df_ano = df[
        df["ano"] == ano
    ]


    df_ano = (
        df_ano
        .sort_values(
            "populacao",
            ascending=False
        )
        .head(10)
    )


    fig = px.bar(
        df_ano,
        x="estado",
        y="populacao",
        title=f"Estados mais populosos - {ano}"
    )


    return fig



def grafico_regiao(df, ano):

    df_ano = df[
        df["ano"] == ano
    ]


    regiao = (
        df_ano
        .groupby("regiao")["populacao"]
        .sum()
        .reset_index()
    )


    fig = px.pie(
        regiao,
        names="regiao",
        values="populacao",
        title=f"População por região - {ano}"
    )


    return fig