from flask import Flask, render_template, jsonify, request, flash, session, url_for, redirect
from flask_socketio import SocketIO, send
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session
import os 
from werkzeug.utils import secure_filename
import uuid

app = Flask(__name__)
app.secret_key = "secretkey123"
socketio = SocketIO(app, cors_allowed_origins = "*")

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///parking.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class users(db.Model):
    role = db.Column(db.String(20), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.String(36), default=str(uuid.uuid4()), unique=True, primary_key=True)
    
# with app.app_context():
#     db.drop_all()
#     db.create_all()

@socketio.on("message")
def handle_message(message):
    print("Recieved message: " + message)
    if message != "User Connected":
        send(message, broadcast=True)

@app.route('/get_ngrok_url')
def get_ngrok_url():
    ngrok_url = os.environ.get('NGROK_URL', 'http://localhost:5000')
    return jsonify({"ngrok_url": ngrok_url})

@app.route('/')
def chat():
    return render_template("chat.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    
    if request.method == "POST":
        name = request.form["name"]
        role = request.form["role"]
        
        new_entry = users(role = role, name=name, user_id=user_id)
        db.session.add(new_entry)
        db.session.commit()
        
        return redirect(url_for('index'))
    
    return render_template("register.html")


if __name__ == "__main__":
    socketio.run(app, host="localhost")
