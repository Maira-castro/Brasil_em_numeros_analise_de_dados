import plotly.express as px


def grafico_evolucao(df):

    df_ano = (
        df
        .groupby("ano")["populacao"]
        .sum()
        .reset_index()
    )


    fig = px.line(
        df_ano,
        x="ano",
        y="populacao",
        markers=True,
        title="Evolução da população brasileira"
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