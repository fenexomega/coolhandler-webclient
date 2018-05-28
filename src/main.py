import eventlet
eventlet.monkey_patch()
from flask import Flask,send_from_directory
from flask import render_template
from flask_socketio import SocketIO,emit
import socket
from simplesocket import simplesocket
import json

#############
HOST = 'localhost'
PORT = 6969

#############

app = Flask(__name__)
app.config['SECRET_KEY'] = 'blablabla'
socketio = SocketIO(app)

@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/<path:path>')
def send_js(path):
    return send_from_directory('static', path)

@socketio.on('connected')
def connected(message):
    print('Novo Cliente: ' + message)

@socketio.on('shellcmd')
def receive_shell(cmd):
    global ssocket
    jobj = json.dumps(cmd)
    ssocket.sendall(jobj)


def receive_message(message):
    print("EMITINDO MESSAGE")
    print(message)
    message = json.loads(message)
    #this wasnt working until I got this
    # https://github.com/miguelgrinberg/Flask-SocketIO/issues/357
    if message['messageType'] == 'response':
        print('Enviando de volta')
        command = message['content']['message']
        socketio.emit('shellcmd',command)

def socket_goneoff():
    pass

#BUG: TCP socket is made twice. The bug has to do with flask-socketio
def start_socket():
    global ssocket
    ssocket = simplesocket(HOST,PORT,receive_message,socket_goneoff)
    ssocket.start()


# if __name__ == '__main__':
start_socket()
socketio.run(app)
