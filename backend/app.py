from flask import Flask, render_template_string, redirect, request, session, url_for
from flask_session import Session
from flask_socketio import SocketIO, join_room, leave_room, send, emit, rooms
import json
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ["SECRET_KEY"]
socketio = SocketIO(app, cors_allowed_origins="*")
messages = {}
counter = 1
users = {}


@socketio.on('message')
def handle_message(msg):
    global counter, messages
    print("Sent message is ", msg)
    to_send_msg = {"id": counter,
           "user" : msg["name"],
           "value": msg["message"],
           "time": "Now",
           "room": msg["room"]
           }
    counter += 1
    messages[msg["room"]].append(to_send_msg)
    print(messages)
    send(to_send_msg, to=msg["room"])
    #threading.Timer(10, delete_message, (counter - 1, msg["room"])).start()

@socketio.on('getMessages')
def get_messages(data):
    global messages
    socketio.emit("getMessages", json.dumps(messages[data["room"]]), to=data["room"])

@socketio.on('join_room')
def on_join(data):
    """
    data: dict
    {'user': player username,
    'room': room to be assigned to}
    """
    user = data['user']
    room = data['room']
    if not messages.get(room):
        messages[room] = []
    join_room(room)
    send(user + ' has entered the room.', to=room)

@socketio.on('leave')
def on_leave(data):
    name = data['name']
    room = data['room']
    leave_room(room)
    send(name + ' has left the room.', to=room)

@socketio.on("test")
def test():
    print("Current rooms for this user:", rooms(sid=request.sid))
if __name__ == "__main__":
    socketio.run(app)
