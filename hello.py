""" Este arquivo é responsável por receber as mensagens enviadas via Whatsapp """
from flask import Flask, render_template, request
from twilio.twiml.messaging_response import MessagingResponse
import requests
import os

from watson import *
from usuarios import *
from firebase import *

app = Flask(__name__)
port = int(os.getenv('PORT', 8000))

@app.route('/')
def render():
    return render_template('index.html')

atendimento = [False]

@app.route('/chatbot', methods=['POST'])
def chatbot():
    # captamos as mensagens enviadas pela twilio
    mensagem_post = request.values.get('Body', '').lower()
    usuario_post = request.values.get('From', '')
    usuario = usuario_whatsapp(mensagem_post, usuario_post)
    print('USUARIO: ' + str(usuario.usuario)) # DEBUG:
    print('MENSAGEM: ' + str(usuario.mensagem)) # DEBUG:
    usuario.adicionar_session_id(devolver_session_id(usuario.usuario))
    print('SESSION_ID: ' + str(usuario.session_id)) # DEBUG:

    # a resposta do watson vem em formato de dicionário
    resposta_watson = conversa_watson(usuario.mensagem, usuario.session_id)

    if texto_ou_api(resposta_watson) == True:
        api_informacoes = extrair_api_infos(resposta_watson)
        print('modelagem: ' + str(type(api_informacoes)))
        api = watson_api(api_informacoes)
        api.printar()
        response_api = api.chamar_api()
        response_api_dict = json.loads(response_api.text) # agora o dado é um dict
        resposta_valida = api.validacao_api(response_api) # volta como str
        validacao_watson = conversa_watson(resposta_valida, usuario.session_id)
        resposta = formatar_texto(validacao_watson)
        print(resposta)            
        return 'mensagem para whatsapp usuario'
    else:
        # comandos para devolver resposta ao usuário
        resposta = formatar_texto(resposta_watson)
        print(resposta)
        return 'mensagem para whatsapp usuário'


    #
    # # preparando as variaveis de respostas
    # resp = MessagingResponse()
    # msg = resp.message()
    #
    # # reiniciando chatbot em caso de bug
    # if mensagem_recebida == '--reset':
    #     deletar_sessao()
    #     criar_sessao()
    #     return 'nova sessão'
    #
    # else:
    #     # condicional do atendimento humanizado
    #     while atendimento[0] == False:
    #
    #         # captar conversation id
    #
    #         # input do usuário enviado ao watson
    #         response = conversa_watson(mensagem_recebida)
    #
    #
    #         # conferir se há algo no contexto para o servidor
    #         if len(response['context']['skills']['main skill'].values()) != 1:
    #
    #             # verificando se alguma das respostas é modelo_api
    #             for valor in response['context']['skills']['main skill'].values():
    #                 if valor.get('modelo_api'):
    #                     print('tem api')
    #
    #                     # usamos a função chamadas_api para realizar todas as chamadas
    #                     print('resposta: ' + str(response['context']['skills']['main skill']['user_defined']))
    #                     api_response = chamadas_api((response['context']['skills']['main skill']['user_defined']))
    #                     str_response = str(api_response)
    #
    #                     # validação do login:
    #                     if str_response == str(b'{"Message":"099|Usu\xc3\xa1rio n\xc3\xa3o localizado."}'): # estudar b string -bytes em python
    #                         print('o usuário não logou com sucesso')
    #                         response_login= conversa_watson('login_failed')
    #                         msg.body(response_login['output']['generic'][0]['text'])
    #                         return str(resp)
    #                     else:
    #                         print('o usuário logou com sucesso')
    #                         response_login= conversa_watson('user_loged')
    #                         response_index = len(response_login['output']['generic'])
    #                         msg.body(response_login['output']['generic'][0]['text'])
    #                         return str(resp)
    #
    #             #vericação de conteudo para ser captado no contexto
    #
    #             #atendimento
    #             if response['output']['generic'][0]['text'] == '--atendimento_online':
    #                 if atendimento[0] == False:
    #                     atendimento.pop(0)
    #                     atendimento.append(True)
    #                     msg.body('você vai entrar no chat em breve')
    #                     return str(resp)
    #
    #
    #             else:
    #             # input do watson -> input do usuário
    #                 msg.body(response['output']['generic'][0]['text'])
    #                 print(response['context']['skills']['main skill'].values())
    #                 return str(resp)
    #
    #
    #



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port, debug=True)
