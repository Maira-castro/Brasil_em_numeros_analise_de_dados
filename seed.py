# seed.py

from sqlalchemy.orm import Session

from models import Brasil, Base, db

from ingestao import (
    buscar_estados,
    buscar_indicador_populacao
)

from limpeza import (
    limpar_populacao,
    limpar_estados,
    juntar_regiao
)


URL_ESTADO = (
    "https://servicodados.ibge.gov.br/api/v1/"
    "localidades/estados?orderBy=nomes"
)

URL_POPULACAO = (
    "https://servicodados.ibge.gov.br/api/v3/"
    "agregados/6579/periodos/-25/"
    "variaveis/9324?localidades=N3[all]"
)


# cria tabela
Base.metadata.create_all(bind=db)


def executar_seed():

    session = Session(bind=db)

    try:
        # Verifica se já existem dados
        existe_registro = session.query(Brasil).first()

        if existe_registro:
            print("✅ Seed ignorada. A tabela Brasil já possui dados.")
            return
        
        print("Buscando estados...")

        estados = buscar_estados(URL_ESTADO)

        print("Buscando população...")

        populacao = buscar_indicador_populacao(URL_POPULACAO)


        print("Limpando dados...")

        df_populacao = limpar_populacao(populacao)

        df_estados = limpar_estados(estados)


        print("Juntando região...")

        df_final = juntar_regiao(
            df_populacao,
            df_estados
        )


        print("Inserindo no banco...")


        for _, linha in df_final.iterrows():

            registro = Brasil(
                uf_id=int(linha["uf_id"]),
                estado=linha["estado"],
                ano=int(linha["ano"]),
                populacao=int(linha["populacao"]),
                sigla=linha["sigla"],
                regiao=linha["regiao"]
            )


            session.add(registro)


        session.commit()

        print("✅ Seed executado com sucesso!")


    except Exception as erro:

        session.rollback()

        print(
            f"❌ Erro no seed: {erro}"
        )


    finally:

        session.close()



if __name__ == "__main__":
    executar_seed()