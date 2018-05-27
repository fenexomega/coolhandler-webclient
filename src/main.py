import eventlet
eventlet.monkey_patch()
from flask import Flask,send_from_directory
from flask import render_template
from flask_socketio import SocketIO,emit
import socket
from simplesocket import simplesocket

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


def receive_message(message):
    print("EMITINDO MESSAGE")
    #this wasnt working until I got this
    # https://github.com/miguelgrinberg/Flask-SocketIO/issues/357
    socketio.emit('newshell',message)
    print(message)

def socket_goneoff():
    pass

def start_socket():
    tcp = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    tcp.connect((HOST,PORT))
    ssocket = simplesocket(tcp,receive_message,socket_goneoff)
    ssocket.start()


if __name__ == '__main__':
    start_socket()
    socketio.run(app)
