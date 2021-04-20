// Connect to Flask's Socket.IO
let socket = io.connect('http://' + document.domain + ':' + location.port);

let getFormData = function(id) {
	return $(`input.${id}`).val().replace(/</g, '');
}

// When user connects to socket (When they load the page)
socket.on('connect', function() {
	// Sends message back to the server with the users session ID as soon as they are connected
	socket.emit('my event', {
		'session_id': session_id,
		'data': 'User Connected'
	});
	
	$('form').on('submit', function(e) {
		e.preventDefault();	// Prevents the default function of submitting the form

		// Get username and message from the DOM
		let username = getFormData('username');
		let msg = getFormData('message');

		// Sends form data to the server
		if (username !== "" && msg !== "" && username[0] !== ' ' && msg[0] !== ' ') {	// Check for valid username and message
			socket.emit('my event', {
				'session_id': session_id,
				'user': username,
				'msg': msg
			});
		}

		$('input.message').val('').focus();	// Clears message box and focuses on it to allow for more input
	});
});

let loadResponse = function(log) {
	// Makes sure there are messages to be shown
	if (log.length > 0) {
		$('#chatbox').empty();	// Clears entire chatbox, this allows me to edit old messages for ALL users

		// Prints all individual messages from the chat log
		for (i in log) {
			if (typeof log[i].user !== typeof(undefined)) {	// Makes sure the message has a username, so join notifications and other non-message data isn't printed
				$('#chatbox').append(`<div><b>${log[i].user}</b>: ${log[i].msg}`);
				$('#chatbox').scrollTop($('#chatbox')[0].scrollHeight);	// Scrolls to printed message, in the context of this loop it keeps users stay scrolled the newest messages.
			}
		}
	}
	// If there are no messages to be displayed
	else {
		$('#chatbox').empty();
		$('#chatbox').append(`
			<i style="text-decoration: underline;">
				The start of a fresh chat! Make yourself at home :)
			</i>`
		);
	}
}

// Runs when the client receives the chat log from the server
socket.on('my response', function(log) { loadResponse(log) });