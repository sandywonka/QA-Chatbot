from flask import Flask, render_template, request
from chatterbot import ChatBot, response_selection, comparisons
from chatterbot.trainers import ChatterBotCorpusTrainer
from chatterbot.trainers import ListTrainer
from flask_socketio import SocketIO, emit, send

app = Flask(__name__)
socket = SocketIO(app)


botz = ChatBot(
    'botz',
    storage_adapter='chatterbot.storage.SQLStorageAdapter',
    database_uri='sqlite:///database.sqlite3',
    logic_adapters = [
    {
    'import_path': 'chatterbot.logic.BestMatch',
    'statement_comparison_function': comparisons.levenshtein_distance,
    'response_selection_method': response_selection.get_most_frequent_response
    },
    {
    'import_path': 'chatterbot.logic.BestMatch',
    'threshold': 0.80,
    'default_response': 'I am sorry, I do not understand.'
    }
]
)

trainer = ListTrainer(botz)

trainer.train([
    'Hi',
    'Hello',
    'How are you today?',
    'I am good, thanks',
    'What are you?',
    'I am QA chatbot',
    'What are you doing?',
    'I am trying to be any help for you',
    'Okay, thanks',
    'No problem!'
    ])


@app.route("/")
def index():
    return render_template("index.html")

@socket.on('connect')
def connect():
    print('CLIENT CONNECTED', request.sid)


@socket.on('data')
def emitback(data):
    emit('returndata', data, broadcast = True)
    response = str(botz.get_response(data))
    emit('returndata', response, broadcast = True)





if __name__ == "__main__":
    socket.run(app, host='0.0.0.0', port=5000)