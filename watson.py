import requests
from ibm_watson import AssistantV2
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

# iniciando o watson AssistantV2
authenticator = IAMAuthenticator('n-nlrLAlu2bR_P1asIguBBZC09wBAvWLQMktUbvz8Y1E')
service = AssistantV2(version='2020-04-01', authenticator=authenticator)
assistant_id = '522e182d-ef6b-4917-9f6f-1c19bc0790a1'

# criar sessão
session_id = service.create_session(assistant_id = assistant_id).get_result()['session_id']

# imprimir a saida do dialogo se, houver.
def conversa_watson(texto):
    response = service.message(assistant_id, session_id, input={'message_type': 'text', 'text': texto, 'options':{'return_context':True}}).get_result()
    return response

def chamadas_api(documento):
    API = documento.get('modelo_api')
    argumentos = '\r\n ' + str(documento.get('argumentos'))
    print(argumentos)
    if API == 'login':
        url = "http://dev.nfeservices.com.br:65000/GOOP/Login"
        payload = argumentos
        headers = {
        'Content-Type': 'text/plain'
        }
        response = requests.request("POST", url, headers=headers, data = payload).text.encode('utf8')
        return response
    if API == 'torques':
        # { "Carro": "Ford Focus", "Ano": "2015", "Cilindradas": "2.0", "Motor": "Duratec", "Valvulas": "16V", "Combustivel":"Flex" }
        url = "http://dev.nfeservices.com.br:65000/GOOP/Torque"

        payload = "{\r\n\"Carro\": \"Ford Focus\",\r\n\"Ano\": \"2015\",\r\n\"Cilindradas\": \"2.0\",\r\n\"Motor\": \"Duratec\",\r\n\"Valvulas\": \"16V\",\r\n\"Combustivel\":\"Flex\"\r\n}"
        headers = {
        		'UserKey': 'Dbi58Dg95BgNcJrvnK3nAp/M1mF0rMkyxq334m9WdgiezQ7UFD7HBW9mWfiY2bd1aR19bGpU3u2Wzftp/heXTg==',
        		'Content-Type': 'text/plain'
        }
        response = requests.request("GET", url, headers=headers, data = payload)
        return response

# deletando a sessão
#service.delete_session(assistant_id = assistant_id, session_id = session_id)
