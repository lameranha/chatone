from flask import Flask, render_template, request
from twilio.twiml.messaging_response import MessagingResponse
from watson import conversa_watson, chamadas_api
import requests
import os

app = Flask(__name__)
port = int(os.getenv('PORT', 8000))

@app.route('/')
def render():
    return render_template('index.html')

@app.route('/chatbot', methods=['POST'])
def chatbot():

    # captamos as mensagens enviadas pela twilio
    mensagem_recebida = request.values.get('Body', '').lower()
    usuario_recebido = request.values.get('From', '')
    resp = MessagingResponse()
    msg = resp.message()

    # condicional do atendimento humanizado
    while mensagem_recebida !='7':

        # input do usuário -> input do watson
        print(mensagem_recebida)
        response = conversa_watson(mensagem_recebida)

        # conferir se há algo no contexto para o servidor
        if len(response['context']['skills']['main skill'].values()) != 1:
            # verificando se alguma das respostas é modelo_api

            for valor in response['context']['skills']['main skill'].values():
                if valor.get('modelo_api'):
                    print('tem api')

                    # usamos a função chamadas_api para realizar todas as chamadas
                    print('resposta: ' + str(response['context']['skills']['main skill']['user_defined']))
                    api_response = chamadas_api((response['context']['skills']['main skill']['user_defined']))
                    str_response = str(api_response)

                    # validação do login:
                    if str_response == str(b'{"Message":"099|Usu\xc3\xa1rio n\xc3\xa3o localizado."}'): # estudar b string -bytes em python
                        print('o usuário não logou com sucesso')
                        response_login= conversa_watson('login_failed')
                        msg.body(response_login['output']['generic'][0]['text'])
                        return str(resp)
                    else:
                        print('o usuário logou com sucesso')
                        response_login= conversa_watson('user_loged')
                        response_index = len(response_login['output']['generic'])
                        msg.body(response_login['output']['generic'][0]['text'])
                        return str(resp)
                    #
                    # # validação torques
                    # if str_response == str{}

        # input do watson -> input do usuário
        msg.body(response['output']['generic'][0]['text'])
        print(response['context']['skills']['main skill'].values())
        return str(resp)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port, debug=True)
