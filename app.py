from flask import Flask, render_template
from flask_socketio import SocketIO
import secrets

app = Flask(__name__)
app.config['SECRET_KEY'] = secrets.token_urlsafe(16)
socketio = SocketIO(app)

log = []

@app.route('/')
def main():
	return render_template('chbox.html')

def response_callback(methods = ['GET', 'POST']):
	print("Message received.")

@socketio.on('my event')
def handle_my_event(json, methods = ['GET', 'POST']):
	print('Event received: ' + str(json))
	if "data" not in json:
		log.append(json)
		print(log)
	socketio.emit('my response', log, callback = response_callback)

if __name__ == '__main__':
	socketio.run(app, host = '0.0.0.0', debug = True)