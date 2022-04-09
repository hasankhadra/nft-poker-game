import json
from ntpath import join
from flask import Flask, request
from flask_socketio import SocketIO, join_room, leave_room, rooms, ConnectionRefusedError
from apscheduler.schedulers.background import BackgroundScheduler
from flask_cors import CORS
from __init__ import TOTAL_PLAYERS, get_tiers_distribution, DB_CONFIG_FILE

from mysql_database.tournaments import Tournaments
from mysql_database.rounds import Rounds
from mysql_database.games import Games
from mysql_database.games_draws import GamesDraws
from mysql_database.players import Players
from mysql_database.num_players import Num_players
from datetime import datetime, timedelta

from poker_logic.dealer import draw_combo, draw_the_flops
from poker_logic import dealer

from poker_logic.round_matching import get_round_matching
from poker_logic.game import play

import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)
app.config["SECRET_KEY"] = os.environ["SECRET_KEY"]
ADMIN_ADDRESS = os.environ["ADMIN_ADDRESS"]
socketio = SocketIO(app, cors_allowed_origins="*")

tournaments_instance = Tournaments(DB_CONFIG_FILE)
rounds_instance = Rounds(DB_CONFIG_FILE)
games_instance = Games(DB_CONFIG_FILE)
games_draws_instance = GamesDraws(DB_CONFIG_FILE)
players_instance = Players(DB_CONFIG_FILE)
num_players_instance = Num_players(DB_CONFIG_FILE)

tiers_distribution = get_tiers_distribution()
scheduler = BackgroundScheduler()

def schedule_round():
    print("Running the scheduler")
    tournaments_id = tournaments_instance.get_current_tournament_id()
    round_players = players_instance.get_players(tournament_id=tournaments_id)

    round_id = rounds_instance.get_cur_round()["id"]
    games = get_round_matching(round_players)
    games_instance.add_round_games(round_id, games)

# if os.environ.get("WERKZEUG_RUN_MAIN") == "true":
#     pass
#     # TODO set all the rounds
#     scheduler.start()

@socketio.on("add_round")
def add_round(data: dict):
    """
    :param data: dict containing 
    {
        start_time: str,
        end_time: str,
        public_address: str
    }
    """
    start_time = data["start_time"]
    end_time = data["end_time"]
    public_address = data["public_address"]
    
    assert public_address == ADMIN_ADDRESS, "You have no access to add a round"
    
    # TODO check the public_address
    cur_round = rounds_instance.get_cur_round()
    if cur_round:
        rounds_instance.add_round([cur_round["round_num"] + 1, start_time, end_time])
    else:
        rounds_instance.add_round([1, start_time, end_time])
    
    start_time = datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S')# - timedelta(days=0, hours=0, minutes=5)
    scheduler.add_job(func=schedule_round, trigger="date", run_date=start_time)
    scheduler.start()

@socketio.on('round_info')
def round_info():
    cur_round = rounds_instance.get_cur_round()
    socketio.emit("round_info", {"start_time": cur_round["start_time"], 
                                 "end_time": cur_round["end_time"],
                                 "round_num": cur_round["round_num"]})
    
@socketio.on("register")
def register(data: dict):
    """
    :param data: dict containing 
    {
        MAYBE NFT ID: str,
        public_address: str,
        username: str
    }
    """
    
    if num_players_instance.get_cur_count() == TOTAL_PLAYERS:
        socketio.emit("register", {"response": "There is no room left for new players!"})
        raise ConnectionRefusedError('There is no room left for new players!')
    
    if players_instance.exists_username([data["username"]]):
        socketio.emit("register", {"response": """Nickname already exists!\nTry a different Nickname!"""})
        raise ConnectionRefusedError("Username already exists")
    
    players_instance.add_player(["TODO_get_nft_id", data["public_address"], data["username"], tiers_distribution[num_players_instance.get_cur_count()]])
    num_players_instance.increase_players_num()
    
    socketio.emit("register", {"response": "OK"})
        
@socketio.on("get_nfts_info")
def nfts_info(data: dict):
    """
    return a list of nfts (if any) with their metadata
    :param data: dict containing
    {
        public_address: str
    }
    :return: a dict 
    {
        "ntfs": list
    }
    where each element in the list is a dictionary
    """
    
    public_address = data["public_address"]
    tournament_id = tournaments_instance.get_current_tournament_id()
    
    nfts_json_format = players_instance.get_player_by(by={"public_address": public_address, "tournament_id": tournament_id}, get_json_format=True)

    socketio.emit("get_nfts_info", {"nfts": nfts_json_format})
    
@socketio.on("get_players")
def get_players():
    """
    return all the players in the curernt tournament
    :return: a dict 
    {
        "players": list
    }
    where each element in the list is a dictionary
    """
    
    tournament_id = tournaments_instance.get_current_tournament_id()
    
    players_json_format = players_instance.get_players(tournament_id=tournament_id, get_json_format=True)
    
    print(players_json_format)

    socketio.emit("get_players", {"players": players_json_format})
    
@socketio.on('log_in_round')
def log_in_round(data: dict):
    
    # TODO check if all nfts are still owned by this user. BLOCKCHAIN
    pass
    
@socketio.on('join_room')
def on_join(data):
    """
    data: dict
    {
        room: room to be assigned to (str)
        game_id: int,
        public_address: str
    }
    """
    print(data)
    game_id = data["game_id"]
    public_address = data["public_address"]
    room = data["room"]
    
    players = players_instance.get_player_by({"public_address": public_address}, get_json_format=True)
    games = games_instance.get_games_by(by={"id": game_id}, get_json_format=True)
    player_id = ""
    username = ""
    opponent_id = ""
    
    for player in players:
        if player["id"] == games[0]["player1_id"]:
            player_id = player["id"]
            username = player["username"]
        if player["id"] == games[0]["player2_id"]:
            player_id = player["id"]
            username = player["username"]


    
    if player_id != "":
        join_room(room)
        
        if player_id == games[0]["player1_id"]:
            opponent_id = games[0]["player2_id"]
        else:
            opponent_id = games[0]["player1_id"]
        
        opponent = players_instance.get_player_by({"id": opponent_id}, get_json_format=True)[0]
        
        socketio.emit("join_room", {"opponent_id": opponent["id"], "username": username, "player_id": player_id, "opponent_username": opponent["username"]})
    else:
        socketio.emit("join_room", {"response": "You are not allowed to access this game"})

@socketio.on('leave_room')
def on_leave(data):
    """
    :param data: dict
    {
        'room': room to leave (str)
    }
    """
    leave_room(data['room'])

@socketio.on("get_next_room")
def get_next_room(data: dict):
    """
    :param data: dict
    {
        player_id: int
    }
    """
    
    player_id = data["player_id"]
    
    cur_round_id = rounds_instance.get_cur_round()["id"]
    all_games = games_instance.get_games_from_round([cur_round_id])
    
    player_rooms = [f"room_{game['id']}" for game in all_games if ((game["player1_id"] == player_id or game["player2_id"] == player_id) and (not game["winner_id"]))]

    if len(player_rooms):
        join(player_rooms[0])
    else:
        socketio.emit("get_next_room", {"room": "ERROR"})
    socketio.emit("get_next_room", {"room": player_rooms[0]})

@socketio.on("stake_nft")
def stake_nft(data: dict):
    """
    transfer nft ownership to smart contract
    data: dict
    {
        public_address: str, 
        nft_id: str,
        player_id: int
    }
    """
    
    public_address = data["public_address"]
    nft_id = data["nft_id"]
    player_id = data["player_id"]
    
    player_json = players_instance.get_player_by(by={"public_address": public_address,
                                                     "nft_id": nft_id,
                                                     "player_id": player_id}, 
                                                 get_json_format=True)

    player_json = player_json
    
    if len(player_json) == 0:
        socketio.emit("stake_nft", {"response": "No such player with nft"})
        raise ConnectionRefusedError("No such player with nft")
    
    # TODO blockchain - transfer ownership of nft to smart contract
    try:
        players_instance.update({"id": player_id, "staked": True})
    except Exception as e:
        socketio.emit("stake_nft", {"response": e})

    
    socketio.emit("stake_nft", {"response": "OK"}) 

@socketio.on("unstake_nft")
def unstake_nft(data: dict):
    """
    transfer nft ownership to player
    data: dict
    {
        public_address: str, 
        nft_id: str,
        player_id: int
    }
    """
    
    public_address = data["public_address"]
    nft_id = data["nft_id"]
    player_id = data["player_id"]
    
    player_json = players_instance.get_player_by(by={"public_address": public_address,
                                                     "nft_id": nft_id,
                                                     "player_id": player_id}, 
                                                 get_json_format=True)

    player_json = player_json
    
    if len(player_json) == 0:
        socketio.emit("unstake_nft", {"response": "No such player with nft"})
        raise ConnectionRefusedError("No such player with nft")
    
    # TODO blockchain - transfer ownership of nft to player
    try:
        players_instance.update({"id": player_id, "staked": False})
    except Exception as e:
        socketio.emit("unstake_nft", {"response": e})

    
    socketio.emit("unstake_nft", {"response": "OK"})

@socketio.on("draw_combo")
def draw_combo(data):
    """
    return a combo of a player in a game
    data: dict
    {
        public_address: str,
        game_id: int
    }
    """
    
    game_id = data["game_id"]
    public_address = data["public_address"]
    
    players = players_instance.get_player_by({"public_address": public_address}, get_json_format=True)
    games = games_instance.get_games_by(by={"id": game_id}, get_json_format=True)
    player_id = ""
    
    for game in games:
        for player in players:
            if player["id"] == game["player1_id"]:
                player_id = player["id"]
            if player["id"] == game["player2_id"]:
                player_id = player["id"]
    
    
    # get player nft tier
    nft_tier = players_instance.get_player_by({"id": player_id}, get_json_format=True)[0]["nft_tier"]

    
    
    # get opponent combo if any
    cur_game = games_instance.get_game([game_id])[0]


    if player_id == cur_game[2]:
        opp_id = cur_game[3]
    else:
        opp_id = cur_game[2]
    
    if cur_game[2] == player_id and cur_game[4]:
        player_combo = cur_game[4].upper()
        opp_combo = cur_game[5].upper()
        
    
    elif cur_game[3] == player_id and cur_game[5]:
        player_combo = cur_game[5].upper()
        opp_combo = cur_game[4].upper()
    
    else:
        opp_combo = cur_game[5] if player_id == cur_game[2] else cur_game[4]
        
        player_combo = dealer.draw_combo(nft_tier, opp_combo)
        
        # update player hand
        player_num = "player1" if player_id == cur_game[2] else "player2"
        games_instance.update({"id": game_id, f"{player_num}_combo": player_combo.upper()})
        player_combo = player_combo.upper()
    
    socketio.emit('draw_combo', {"player_combo": [player_combo[:2], player_combo[2:]]})
    cur_game = games_instance.get_game([game_id])[0]
    
    print(cur_game[4], cur_game[5])
    if cur_game[4] and cur_game[5]:
        print("inside if")
        results = play_game({"game_id": game_id})
        results['player_id'] = player_id
        results['opponent_id'] = opp_id
        results['opponent_combo'] = [opp_combo[:2], opp_combo[2:]]
        socketio.emit("play_game", {"results": results})

        results_copy = results.copy()
        results_copy['player_id'] = opp_id
        results_copy['opponent_id'] = player_id
        results['opponent_combo'] = [player_combo[:2], player_combo[2:]]
        
        socketio.emit("play_game", {"results": results_copy}, to="room_"+str(cur_game[0]), include_self=False)
        # to="room_"+str(cur_game[0])

def play_game(data: dict):  
    """
    return the result of the game between two players
    :param data: dict
    {
        game_id: int
    }
    :return: dict
    {
        winner: int (1 for first_player, 2 for second player, -1 for draw),
        player1_id: {
            best_hand: list,
            best_hand_name: str,   
            winner: bool
        },
        player2_id: {
            best_hand: list,
            best_hand_name: str,    
            winner: bool
        },
        flops: list
        bad_beat: bool (True if the loser has a hand better than "AAAKK"),
        tie_with_hands: bool
    }
    """  
    game_id = data["game_id"]
    
    game = games_instance.get_game([game_id], get_json_format=True)[0]
    
    player1_combo = game["player1_combo"]
    player2_combo = game["player2_combo"]
    if not game['flops']:
        the_flops = dealer.draw_the_flops(player1_combo, player2_combo)
        games_instance.update({"id": game_id, "flops": the_flops})
    else:
        the_flops = game['flops']
    
    game_result: dict = play(player1_combo, player2_combo, the_flops)
    if game_result["winner"] != -1:
        games_instance.update({
            "id": game["id"], 
            "winner_id": game["player1_id"] if game_result["winner"] == 1 else game["player2_id"], 
            "bad_beat": True if game_result.get("bad_beat") else False
        })
    
    player1_dict = {
        game["player1_id"]: {
            "best_hand": game_result["best_hand_1"],
            "best_hand_name": game_result["best_hand_1_name"],
            "winner": True if game_result["winner"] == 1 else False
        }
    }
    
    game_result.update(player1_dict)
    
    player2_dict = {
        game["player2_id"]: {
            "best_hand": game_result["best_hand_2"],
            "best_hand_name": game_result["best_hand_2_name"],
            "winner": True if game_result["winner"] == 2 else False
        }
    }
    
    game_result.update(player2_dict)

    del game_result["best_hand_1"]
    del game_result["best_hand_2"]
    del game_result["best_hand_1_name"]
    del game_result["best_hand_2_name"]
    
    if game_result["winner"] == -1:
        games_draws_instance.add_game([game_id, player1_combo, player2_combo, the_flops])
    else:
        games_instance.update({"id": game_id, 
                               "winner_id": game["player1_id"] if game_result["winner"] == 1 else game["player2_id"]})
    
    game_result["flops"] = the_flops.upper().split(",")
    return game_result

@socketio.on("draw_the_flops")
def draw_the_flops(data: dict):
    """
    return the 5 cards that will be showed on the table
    data: dict
    {
        game_id: int
    }
    """
    game_id = data["game_id"]
    
    game_row = games_instance.get_game([game_id])[0]
    
    player1_combo = game_row[4]
    player2_combo = game_row[5]
    player1_combo ="QhTd"
    print(player1_combo, player2_combo)
    
    if game_row[6] != "":
        the_flops = game_row[6]
    else:    
        the_flops = dealer.draw_the_flops(player1_combo, player2_combo)
        
        games_instance.update({"id": game_id, "flops": the_flops})
        
    the_flops = the_flops.upper().split(",")
        
    socketio.emit("draw_the_flops", {"the_flops": the_flops})
    

if __name__ == "__main__":
    socketio.run(app, debug=True, host="0.0.0.0")
