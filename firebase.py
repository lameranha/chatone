""" Este arquivo é destinado interação com nosso banco de dados firebase """
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from watson import criar_sessao
import datetime

# credenciais e inicialização da base de dados
cred = credentials.Certificate('chatone-f8990-firebase-adminsdk-ynume-3975b70eff.json')
firebase_admin.initialize_app(cred)
db = firestore.client()

## funções referente a sessão do usuário
def adicionar_session_id(whatsapp, session_id):
    """cria documento com o whatsapp e a sessao no watson"""

    data = {
        u'usuario': whatsapp,
        u'session_id': session_id,
        u'timestamp': datetime.datetime.now() - datetime.timedelta(hours=-3)
    }

    return db.collection(u'sessions_flow').document().set(data)
"""exemplo de aplicação da função"""
# adicionar_session_id('whatsapp+5547991662635, 'session_x')

def conferir_session_id(whatsapp):
    """consulta o firestore para ver se este número do whatsapp já tem session_id"""

    sessions_flow = db.collection(u'sessions_flow')
    consulta = sessions_flow.where(u'usuario', u'==', whatsapp).stream()
    for query in consulta:
            return str(query.to_dict().get('session_id'))
"""exemplo de aplicação da função"""
# conferir_session_id('whatsapp+5547991662635)

def devolver_session_id(whatsapp):
    """esta função sempre devolve uma session_id, se o usuário já tem ele devolve
       caso ele não tenha, é criado uma nova e devolvido"""

    if conferir_session_id(whatsapp) != None:
        return conferir_session_id(whatsapp)
    else:
        session_id = criar_sessao()
        adicionar_session_id(whatsapp, session_id)
        return session_id
"""exemplo de aplicação da função"""
# devolver_session_id('whatsapp+5547991662635) -> essa será chamada

def remover_usuario_sessions_flow(whatsapp):
    """esta função remove o usuário da database de sessions"""
    id_documento = db.collection(u'sessions_flow').where(u'usuario', u'==', whatsapp).stream()
    for documento in id_documento:
        id = documento.id
        return db.collection(u'sessions_flow').document(id).delete()
"""exemplo de aplicação da função"""
# remover_usuario_sessions_flow('whatsapp+5547991662635') -> essa será chamada

## funções referente ao ambiente no qual o usuário está
def conferir_ambiente(whatsapp):
    """esta função verifica em qual ambiente o nosso usuário se encontra no momento,
        podendo ser:   1) chatbot: falando com o watson,
                       2) atendimento humanizado: na sala de bate papo,
                       3) fila de espera: no aguardo para que alguma sala seja liberada"""

    ambiente_usuario = db.collection(u'ambiente_usuario')
    consulta = ambiente_usuario.where(u'usuario', u'==', whatsapp).stream()

    for query in consulta:
        if bool(query.to_dict().get(u'chatbot')) == True:
            return 'chatbot'
        if bool(query.to_dict().get(u'atendimento_humanizado')) == True:
            return 'atendimento_humanizado'
        if bool(query.to_dict().get(u'fila_espera')) == True:
            return 'fila_espera'
"""exemplo de aplicação da função"""
# print(conferir_ambiente('whatsapp+5547996740418')) #-> consulta numero lari
# print(conferir_ambiente('whatsapp+5547991662635')) #-> consulta numero leo

def adicionar_ambiente(whatsapp):
    """caso a função conferir_ambiente retorno com o valor de None, essa função é
       chamada para adicionar usuário em determinado ambiente"""

    data = {
        u'usuario': whatsapp,
        u'atendimento_humanizado': False,
        u'chatbot': True,
        u'fila_espera': False

    }

    return db.collection(u'ambiente_usuario').document().set(data)
"""exemplo de aplicação da função"""
# if conferir_ambiente('whatsapp+5547996740418') == None: -> essa será chamada
#     adicionar_ambiente('whatsapp+5547996740418')

def trocar_ambiente(whatsapp, novo_ambiente):
    """esta função substitui o documento que acusa o ambiente no qual o usuário está no momento
       caso ele seja direcionado para o atendimento humanizado ou a fila de espera"""

    if novo_ambiente == 'chatbot':
        data = {u'usuario': whatsapp,u'atendimento_humanizado': False,u'chatbot': True,
                u'fila_espera': False}

    if novo_ambiente == 'atendimento_humanizado':
        data = {u'usuario': whatsapp,u'atendimento_humanizado': True,u'chatbot': False,
                u'fila_espera': False}

    if novo_ambiente == 'fila_espera':
        data = {u'usuario': whatsapp,u'atendimento_humanizado': False,u'chatbot': False,
                u'fila_espera': True}

    # conseguir o doc id do usuario no coleção de ambientes
    id_documento = db.collection(u'ambiente_usuario').where(u'usuario', u'==', whatsapp).stream()
    for documento in id_documento:
        id = documento.id
        return db.collection(u'ambiente_usuario').document(id).set(data)
"""exemplo de aplicação da função"""
# print(trocar_ambiente('whatsapp+5547991662635', 'atendimento_humanizado'))
#-> essa será chamada

def remover_usuario_ambiente_usuario(whatsapp):
    """esta função remove o usuário da database de sessions"""
    id_documento = db.collection(u'ambiente_usuario').where(u'usuario', u'==', whatsapp).stream()
    for documento in id_documento:
        id = documento.id
        return db.collection(u'ambiente_usuario').document(id).delete()
"""exemplo de aplicação da função"""
# remover_usuario_ambiente_usuario('whatsapp+5547991662635') -> essa será chamada
