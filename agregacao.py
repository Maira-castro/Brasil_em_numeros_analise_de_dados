####################### feito pela eveline ######################################

def preparar(df, regiao="Brasil"):
    # Filtra pela região escolhida
    if regiao != "Brasil":
        df_ord = df[df["regiao"] == regiao].copy()
    else:
        df_ord = df.copy()

    # Ordena do maior para o menor valor
    df_ord = df_ord.sort_values(
        by="valor",
        ascending=False
    )

    # Caso não existam dados para a região escolhida
    if df_ord.empty:
        kpis = {
            "total": 0,
            "maior": None,
            "menor": None,
            "media": None
        }

        return df_ord, kpis

    # Calcula os KPIs
    kpis = {
        "total": len(df_ord),

        "maior": {
            "nome": df_ord.iloc[0]["nome"],
            "valor": float(df_ord.iloc[0]["valor"])
        },

        "menor": {
            "nome": df_ord.iloc[-1]["nome"],
            "valor": float(df_ord.iloc[-1]["valor"])
        },

        "media": float(df_ord["valor"].mean())
    }

    return df_ord, kpis