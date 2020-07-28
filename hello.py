from cloudant import Cloudant
from flask import Flask, render_template, request, jsonify
import atexit
import os
import json

app = Flask(__name__, static_url_path='')

port = int(os.getenv('PORT', 8000))

@app.route('/')
def root():
    return render_template('login.html')

@app.route('/chat')
def chat():
    return render_template('chat.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port, debug=True)
