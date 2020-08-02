""" Este arquivo é destinado a integração com o watson via API, sendo responsavel por pegar os outputs do watson """
import json
import requests
from ibm_watson import AssistantV2
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

# classe das api_response
class watson_api:
    def __init__(self, api_infos_dict):
        """coletando as informações da chamada da api"""
        modelo = api_infos_dict.get('modelo')
        self.modelo = modelo
        url = api_infos_dict.get('url')
        self.url = url
        argumentos = str(api_infos_dict.get('argumentos'))
        self.argumentos = argumentos
        metodo = api_infos_dict.get('metodo')
        self.metodo = metodo
        if modelo == 'login':
            self.header = {'Content-Type': 'text/plain'}
        else:
            self.header = {'UserKey': 'Dbi58Dg95BgNcJrvnK3nAp/M1mF0rMkyxq334m9WdgiezQ7UFD7HBW9mWfiY2bd1aR19bGpU3u2Wzftp/heXTg==', 	'Content-Type': 'text/plain'}

    def printar(self):
        print('modelo: ' + str(self.modelo))
        print('url: ' + str(self.url))
        print('header: ' + str(self.header))
        print('argumentos: ' + str(self.argumentos))
        print('metodo: ' + str(self.metodo))

    def chamar_api(self):
        response_api = requests.request(self.metodo, self.url, headers=self.header, data=self.argumentos)
        return response_api # response models -> .text para converter para string

    def validacao_api(self, response_api):
        if response_api == str(b'{"Message":"099|Usu\xc3\xa1rio n\xc3\xa3o localizado."}'):
            return 'login_failed'
        else:
            return 'user_loged'


# iniciando o watson AssistantV2
authenticator = IAMAuthenticator('n-nlrLAlu2bR_P1asIguBBZC09wBAvWLQMktUbvz8Y1E')
service = AssistantV2(version='2020-04-01', authenticator=authenticator)
assistant_id = '522e182d-ef6b-4917-9f6f-1c19bc0790a1'


def criar_sessao():
    session_id = service.create_session(assistant_id = assistant_id).get_result()['session_id']
    return session_id

# imprimir a saida do dialogo se, houver.
def conversa_watson(mensagem, session_id_usuario):
    response = service.message(assistant_id, session_id_usuario, input={'message_type': 'text', 'text': mensagem, 'options':{'return_context':True, 'debug':True}}).get_result()
    return response

# deletando a sessão'
def deletar_sessao():
    service.delete_session(assistant_id = assistant_id, session_id = session_id)
    return 'sessão deletada'

# texto ou api
def texto_ou_api(response_dict):
    """analizar se devemos coletar api do watson ou resposta para o usuário"""
    if response_dict['output']['generic'][0].get('text') == '--API':
        return True
    else:
        return False

def formatar_texto(response_dict):
    resposta = response_dict['output']['generic'][0].get('text')
    return resposta #em string

def extrair_api_infos(response_dict):
    """extrari a api e devolver um dicionario apenas com os dados da API"""
    api_json = response_dict['context']['skills']['main skill']['user_defined'].get('API')
    return api_json #em dicionário
