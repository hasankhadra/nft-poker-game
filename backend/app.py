from flask import Flask, request
from flask_socketio import SocketIO, join_room, leave_room, send, emit, rooms, ConnectionRefusedError
import os
from backend import TOTAL_PLAYERS
from mysql_database.players import Players
from dotenv import load_dotenv
from typing import Union
load_dotenv()

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ["SECRET_KEY"]
socketio = SocketIO(app, cors_allowed_origins="*")

players_instance = Players()

@socketio.on("register")
def register_player(data: dict):
    """
    :param data: dict containing 
    {
        MAYBE NFT ID: ,
        public_address: player public address,
        username: player username
    }
    """
    
    if players_instance.get_num_players() == TOTAL_PLAYERS:
        raise ConnectionRefusedError('There is no room left for new players!')
    
    players_instance.add_player(["TODO_get_nft_id", data["public_address"], data["username"]])
    
    if players_instance.get_num_players() == TOTAL_PLAYERS:
        # TODO start initiating graph for games and storing rooms
        # for each game
        pass
    
@socketio.on('log_in_round')
def log_in_round(data: dict):
    # TODO check if all nfts are still owned by this user.
    pass
    
@socketio.on('join_room')
def on_join(data):
    """
    data: dict
    {
        'id': player id,
        'room': room to be assigned to
    }
    """
    user = data['id']
    room = data['room']
    join_room(room)
    send(user + ' has entered the room.', to=room)

@socketio.on('leave')
def on_leave(data):
    """
    :param data: dict
    {
        'room': room to leave
    }
    """
    leave_room(data['room'])

@socketio.on("get_rooms")
def get_rooms():
    # TODO return all games' rooms this player will join
    pass


if __name__ == "__main__":
    socketio.run(app, debug=True)
