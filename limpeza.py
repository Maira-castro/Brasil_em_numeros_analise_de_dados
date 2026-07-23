import pandas as pd


def json_para_df(payload):
    series = payload[0]["resultados"][0]["series"]
    linhas = []

    for s in series:

        nome = s["localidade"]["nome"]
        uf_id = int(s["localidade"]["id"])

        ano, valor = list(s["serie"].items())[-1]

        if valor in ("...", "-"):
            continue

        valor = float(valor)

        linhas.append({
            "uf_id": uf_id,
            "nome": nome,
            "ano": ano,
            "valor": valor
        })

    df = pd.DataFrame(linhas)

    df["valor"] = pd.to_numeric(df["valor"], errors="coerce")
    df = df.dropna(subset=["valor"])

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

    df = df.merge(
        df_estados[["uf_id", "regiao"]],
        on="uf_id",
        how="left"
    )

    return df
