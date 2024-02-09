from flask import Flask, render_template
from flask_socketio import SocketIO, send


app = Flask(__name__)
app.secret_key = "secretkey123"
socketio = SocketIO(app, cors_allowed_origins = "*")

@socketio.on("message")
def handle_message(message):
    print("Recieved message: " + message)
    if message != "User Connected":
        send(message, broadcast=True)

@app.route('/')
def chat():
    return render_template("chat.html")

if __name__ == "__main__":
    socketio.run(app, host="localhost")
