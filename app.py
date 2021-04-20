from flask import Flask, render_template
from flask_socketio import SocketIO
import secrets

app = Flask(__name__)
app.config['SECRET_KEY'] = secrets.token_urlsafe(16)	# Sets the secret key
socketio = SocketIO(app)

# Load the log file into a variable
with open('log.txt', 'r') as f:
	log = eval(f.read())

@app.route('/')
def main(admin = False):
	# If the user is an admin, set their session ID to be the app's secret key
	if admin:
		return render_template('chbox.html', key = app.config['SECRET_KEY'])
	else:
		return render_template('chbox.html', key = secrets.token_urlsafe(16))

@app.route('/' + app.config['SECRET_KEY'])
def admin():
	return main(True)

# Sends useful info back to the console
def response_callback(data):
	str = f'\nResponse received:\n\tSession ID: {data["session_id"]}\n\t'
	if 'data' in data:
		str += f'Data: {data["data"]}\n'
	else:
		str += f'Username: {data["user"]}\n\tMessage: {data["msg"]}'
	print(str)

@socketio.on('my event')
def handle_my_event(e_json, methods = ['GET', 'POST']):
	if 'data' not in e_json:	# Prevents non-message data from getting in the chat log
		log.append(e_json)	# Add latest message to the log

		# Handle admin commands
		if e_json['session_id'] == app.config['SECRET_KEY']:
			if e_json['msg'] == '/clear':
				log.clear()
			elif e_json['msg'] == '/reload':
				log.clear()
				with open('log.txt', 'r') as f:
					for msg in eval(f.read()):
						log.append(msg)

	# Backup chat log to file
	with open('log.txt', 'w') as f:
		f.write(repr(log))

	socketio.emit('my response', log, callback=response_callback(e_json)) # Send chat log back to client for processing

if __name__ == '__main__':
	print(f'\n------------------------\nSecret Key: {app.config["SECRET_KEY"]}\n------------------------\n')
	socketio.run(app, host = '0.0.0.0', debug = True)