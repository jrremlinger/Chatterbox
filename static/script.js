var socket = io.connect('http://' + document.domain + ':' + location.port);

		socket.on('connect', function() {
			socket.emit('my event', {
				'data': 'User Connected',
				'session_id': user_id
			});
			
			var form = $('form').on('submit', function(e) {
				e.preventDefault();
				let username = $('input.username').val();
				let msg = $('input.message').val();

				if (username !== "" && msg !== "" && username[0] !== ' ' && msg[0] !== ' ') {
					socket.emit('my event', {
						'session_id': user_id,
						'user': username,
						'msg': msg
					});
				}

				$('input.message').val('').focus();
			});
		});

		socket.on('my response', function(response) {
			if (response.length > 0) {
				// console.log(response);
				$('#chatbox').empty();

				for (message of response) {
					if (typeof message.user !== typeof(undefined)) {
						$('#chatbox').append(`<div><b>${message.user}</b>: ${message.msg}`);
						$('#chatbox').scrollTop($('#chatbox')[0].scrollHeight);
					}
				}
			}
			else {
				$('#chatbox').empty();
				$('#chatbox').append(`
					<i style="text-decoration: underline;">
						The start of a fresh chat! Make yourself at home :)
					</i>`
				)
			}
		});