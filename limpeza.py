import pandas as pd


def limpar_populacao(dados):

    registros = []

    series = dados[0]["resultados"][0]["series"]

    for estado in series:

        nome_estado = estado["localidade"]["nome"]

        serie = estado["serie"]

        for ano, valor in serie.items():

            registros.append({
                "uf_id": estado["localidade"]["id"],
                "estado": nome_estado,
                "ano": int(ano),
                "populacao": int(valor)
                })


    df = pd.DataFrame(registros)


    # ==========================
    # LIMPEZA
    # ==========================

    # remover duplicados
    df = df.drop_duplicates()


    # ordenar
    df = df.sort_values(
        by=["estado", "ano"]
    )


    # verificar valores ausentes
    df = df.dropna(
        subset=[
            "estado",
            "ano",
            "populacao"
        ]
    )


    # garantir tipos
    df["ano"] = df["ano"].astype(int)

    df["populacao"] = (
        df["populacao"]
        .astype(int)
    )

    return df


def limpar_estados(estados):
    linhas = []

    for estado in estados:
        linhas.append({
            "uf_id": int(estado["id"]),
            "sigla": estado["sigla"],
            "nome_estado": estado["nome"],
            "regiao": estado["regiao"]["sigla"]
        })

    df_estados = pd.DataFrame(linhas)

    return df_estados


def juntar_regiao(df, df_estados):

    df["uf_id"] = df["uf_id"].astype(str)
    df_estados["uf_id"] = df_estados["uf_id"].astype(str)

    df = df.merge(
        df_estados[["uf_id", "sigla", "regiao"]],
        on="uf_id",
        how="left"
    )

    return df