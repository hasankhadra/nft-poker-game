import json
from flask import Flask, request
from flask_socketio import SocketIO, join_room, leave_room, send, emit, rooms, ConnectionRefusedError
import os
from __init__ import TOTAL_PLAYERS, get_tiers_distribution
from mysql_database.players import Players
from mysql_database.games import Games
from mysql_database.num_players import Num_players
from dotenv import load_dotenv
from poker_logic.dealer import draw_combo
load_dotenv()

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ["SECRET_KEY"]
socketio = SocketIO(app, cors_allowed_origins="*")

players_instance = Players("mysql_database/db.ini")
games_instance = Games("mysql_database/db.ini")
num_players_instance = Num_players("mysql_database/db.ini")

tiers_distribution = get_tiers_distribution()

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
    cur_players_count = num_players_instance.get_cur_count()
    if cur_players_count == TOTAL_PLAYERS:
        raise ConnectionRefusedError('There is no room left for new players!')
    
    if players_instance.exists_username([data["username"]]):
        raise ConnectionRefusedError("Username already exists")
    
    players_instance.add_player(["TODO_get_nft_id", data["public_address"], data["username"], tiers_distribution[cur_players_count]])
    num_players_instance.increase_players_num()
    
    if num_players_instance.get_cur_count() == TOTAL_PLAYERS:
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

@socketio.on("draw_combo")
def draw_combo(data):
    """
    data: dict
    {
        player_id: ..,
        game_id: ..
    }
    """
    
    game_id = data["game_id"]
    player_id = data["player_id"]
    
    # get player nft tier
    nft_tier = players_instance.get_player_by_id([player_id])[5]
    
    # get opponent combo if any
    cur_game = games_instance.get_game([game_id])
    opp_combo = cur_game[5] if player_id == cur_game[2] else cur_game[4]
    
    player_combo = draw_combo(nft_tier, opp_combo)
    
    send('draw_combo', json.dumps({"player_combo": player_combo}))
    
    

if __name__ == "__main__":
    socketio.run(app, debug=True)
