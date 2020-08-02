""" Este arquivo é destinado a modelagem e de dados de: usuários, conversas, sessões """
import datetime

class usuario_whatsapp:
    def __init__(self, mensagem, usuario):
        self.mensagem = mensagem
        self.usuario = usuario
        self.timestamp = datetime.datetime.now()

    def adicionar_session_id(self, session_id):
        self.session_id = session_id

    def mostrar_credenciais(self):
        print(self.usuario)
        print(self.timestamp)

# TESTES
# user = usuario_whatsapp('oi tudo bem', 'whatsapp+5547991662635')
# user.mostrar_credenciais()
# print(user.mensagem)
# print(user.usuario)
# print(user.timestamp)

class cliente_watson():
    def __init__(mensagem, session_id):
        self.mensagem = mensagem
        self.session_id = session_id

    def mostrar_credenciais(self):
        print(self.session_id)
