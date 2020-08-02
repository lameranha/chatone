class api_lab:
    def __init__(self):



"""
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
        url = "http://dev.nfeservices.com.br:65000/GOOP/Torque"

        payload = "{\r\n\"Carro\": \"Ford Focus\",\r\n\"Ano\": \"2015\",\r\n\"Cilindradas\": \"2.0\",\r\n\"Motor\": \"Duratec\",\r\n\"Valvulas\": \"16V\",\r\n\"Combustivel\":\"Flex\"\r\n}"
        headers = {
        		'UserKey': 'Dbi58Dg95BgNcJrvnK3nAp/M1mF0rMkyxq334m9WdgiezQ7UFD7HBW9mWfiY2bd1aR19bGpU3u2Wzftp/heXTg==',
        		'Content-Type': 'text/plain'
        }
        response = requests.request("GET", url, headers=headers, data = payload)
        return response
"""
