from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import gen_adventure.prompt_manager as prompt_manager

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)
game_prompt_manager = prompt_manager.PromptManager()
game_user_name = "GM"

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('connect')
def test_connect():
    print('Client connected')
    emit('message', {'username': game_user_name, 'message': 'Welcome!'}, broadcast=True)
    gm_message = game_prompt_manager.handle_prompt("")
    emit('message', {'username': game_user_name, 'message': gm_message}, broadcast=True)


@socketio.on('message')
def handle_message(data):
    print('received message:', data)
    emit('message', {'username': 'Player 1', 'message': data['message']}, broadcast=True)
    gm_message = game_prompt_manager.handle_prompt(data['message'])
    print('sent message:', gm_message)
    emit('message', {'username': game_user_name, 'message': gm_message}, broadcast=True)

if __name__ == '__main__':
    socketio.run(app)