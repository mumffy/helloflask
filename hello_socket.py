from flask import Flask, render_template, request
from flask_socketio import SocketIO, send, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socket = SocketIO(app)

@socket.on('connect')
def handle_connect():
    app.logger.info('---> connect /')
    print "user {0} connected".format(request.sid)
    emit("user joined", "user {0} has joined the chat".format(request.sid), broadcast=True, include_self=False)
    emit("user joined", "Server confirms you ({0}) have joined the chat.".format(request.sid))
    return True

@socket.on('chat message')
def handle_chat_message(message):
    print "user {0} said: {1}".format(request.sid, message)
    emit("chat broadcast", "{0} said: {1}".format(request.sid, message), broadcast=True, include_self=False)
    return

@socket.on('disconnect')
def handle_connect():
    app.logger.info('---> disconnect /')
    print "user {0} has disconnected".format(request.sid)

# disconnecting event doesn't seem to be supported
@socket.on('disconnecting')
def handle_connect():
    app.logger.info('---> disconnecting /')
    print "user {0} is disconnectING...".format(request.sid)

@app.route('/')
def index():
    app.logger.info('---> GET /')
    return render_template('socket.html', async_mode=socket.async_mode)

if __name__ == '__main__':
    socket.run(app, debug=False, use_reloader=True)