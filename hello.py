from flask import Flask, render_template, redirect, render_template, request, session, url_for, g
from twilio.twiml.messaging_response import MessagingResponse
from flask_socketio import SocketIO
from twilio.rest import Client
import atexit
import os
import json

class Usuarios:
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

    def __repr__(self):
        return f'<User: {self.username}>'
usuarios = []
usuarios.append(Usuarios(id=1, username='leonardo', password='ozymandias'))
usuarios.append(Usuarios(id=2, username='larissa', password='ozymandias'))
usuarios.append(Usuarios(id=3, username='leomar', password='chatone@goop'))
usuarios.append(Usuarios(id=4, username='rodrigo', password='chatone@goop'))
usuarios.append(Usuarios(id=5, username='goop', password='chatone@goop'))

online = []

app = Flask(__name__, static_url_path='/static/')
port = int(os.getenv('PORT', 8000))
app.secret_key = 'chatone@evox@2020'
socketio = SocketIO(app)

@app.before_request
def before_request():
    if 'user_id' in session:
        user = [x for x in usuarios if x.id == session['user_id']][0]
        g.user = usuarios
        print(usuarios)

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session.pop('user_id', None)

        username = request.form['username']
        password = request.form['password']

        user = [x for x in usuarios if x.username == username][0]
        if user and user.password == password:
            session['user_id'] = user.id
            return redirect(url_for('chat'))

        return redirect(url_for('login'))

    return render_template('login.html')

@app.route('/chat')
def chat():
    return render_template('chat.html')

@app.route('/chatbot', methods=['POST'])
def bot():
    whatsapp_msg = request.values.get('Body', '').lower()
    whatsapp_user = request.values.get('From', '')
    print(whatsapp_msg)
    resp = MessagingResponse()
    msg = resp.message()
    socketio.emit('whatsapp', {'mensagem':whatsapp_msg})
    return ('enviada')

@socketio.on('message')
def mensagem_cliente(data):
    print(request.sid)
    account_sid = 'ACee0cdfd07fd27a4f98644ecf9aaf739d'
    auth_token = '2aa27683e177cb361cc28b43e759ca90'
    client = Client(account_sid, auth_token)

    message = client.messages.create(
                                  from_='whatsapp:+14155238886',
                                  body=data,
                                  to='whatsapp:+554791662635'
                              )

    print(message.sid)

@socketio.on('whatsapp')
def mensagem_cliente(data):
    resp = MessagingResponse()
    msg = resp.message()
    msg.body(data.value)
    return str(resp)

@socketio.on('atendimento', namespace='atendimento1')
def receive_username(username):
    online.append({atendimento : request.sid})
    print(online)



if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=port, debug=True)
