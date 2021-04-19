from flask import Flask, render_template
from flask_socketio import SocketIO
import secrets

app = Flask(__name__)
app.config['SECRET_KEY'] = secrets.token_urlsafe(16)
print(
	"\n------------------------\n" + "Secret Key: " +
	app.config['SECRET_KEY'] +
	"\n------------------------\n"
)
socketio = SocketIO(app)

f = open('log.txt', 'r')
log = eval(f.read())

@app.route('/')
def main(admin = False):
	if admin:
		return render_template('chbox.html', key = app.config['SECRET_KEY'])
	else:
		return render_template('chbox.html', key = secrets.token_urlsafe(16))

@app.route('/' + app.config['SECRET_KEY'])
def admin():
	return main(True)

def response_callback(methods = ['GET', 'POST']):
	print("Message received.")

@socketio.on('my event')
def handle_my_event(e_json, methods = ['GET', 'POST']):
	print('Event received: ' + str(e_json))

	if 'data' not in e_json:
		log.append(e_json)

		if e_json['session_id'] == app.config['SECRET_KEY']:
			if e_json['msg'] == '/clear':
				log.clear()
			elif e_json['msg'] == '/reload':
				f = open('log.txt', 'r')
				log.clear()
				for msg in eval(f.read()):
					log.append(msg)

	f = open('log.txt', 'w')
	f.write(repr(log))
	f.close()

	socketio.emit('my response', log, callback = response_callback)
	print(log)

if __name__ == '__main__':
	socketio.run(app, host = '0.0.0.0', debug = True)