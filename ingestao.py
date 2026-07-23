import requests

URL_ESTADO = 'https://servicodados.ibge.gov.br/api/v1/localidades/estados?orderBy=nomes'
URL_POPULACAO = 'https://servicodados.ibge.gov.br/api/v3/agregados/6579/periodos/-1/variaveis/9324?localidades=N3[all]'

#------Função para buscar estado
def buscar_estados():
    try:
        response = requests.get(URL_ESTADO,timeout=30)
        response.raise_for_status()
        dados = response.json()

        #validando o tipo de resposta
        if not isinstance(dados, list) or len(dados) == 0:
            raise ValueError('Resposta de estados vazia ou em formato inesperado')

        #verificando se os campos esperados estão vindo
        for estado in dados:
            for campo in ['id', 'sigla', 'nome', 'regiao']:
                if campo not in estado:
                    raise ValueError(f'Estado sem o campo "{campo}": {estado}')

        #retornando os dados
        return dados

    #se der algum erro
    except requests.exceptions.ConnectionError:
        return 'Sem conexão com a internet'
    except requests.exceptions.Timeout:
        return 'A API demorou demais para responder'
    except requests.exceptions.HTTPError as e:
        return f'Erro HTTP: {e}'
    except ValueError as e:
        return f'Dado inválido: {e}'

#------Função para população
def buscar_indicador_populacao():
    try:
        response = requests.get(URL_POPULACAO, timeout=30)
        response.raise_for_status()
        dados = response.json()

        # validando o tipo de resposta
        if not isinstance(dados, list) or len(dados) == 0:
            raise ValueError('Resposta de população vazia ou em formato inesperado')

        if 'resultados' not in dados[0] or len(dados[0]['resultados']) == 0:
            raise ValueError('Campo "resultados" ausente ou vazio na resposta')

        if 'series' not in dados[0]['resultados'][0]:
            raise ValueError('Campo "series" ausente em "resultados"')

        return dados

    # se der algum erro
    except requests.exceptions.ConnectionError:
        return 'Sem conexão com a internet'
    except requests.exceptions.Timeout:
        return 'A API demorou demais para responder'
    except requests.exceptions.HTTPError as e:
        return f'Erro HTTP: {e}'
    except ValueError as e:
        return f'Dado inválido: {e}'

# print(buscar_indicador_populacao())