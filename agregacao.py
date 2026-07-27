####################### feito pela eveline ######################################

def preparar(df, regiao="Brasil"):
    # Filtra pela região escolhida
    if regiao != "Brasil":
        df_ord = df[df["regiao"] == regiao].copy()
    else:
        df_ord = df.copy()

    # Ordena do maior para o menor valor
    df_ord = df_ord.sort_values(
        by="populacao",
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
        "total": df_ord["estado"].nunique(),

        "maior": {
            "estado": df_ord.iloc[0]["estado"],
            "populacao": float(df_ord.iloc[0]["populacao"])
        },

        "menor": {
            "estado": df_ord.iloc[-1]["estado"],
            "populacao": float(df_ord.iloc[-1]["populacao"])
        },

        "media": float(df_ord["populacao"].mean())
    }

    return df_ord, kpis