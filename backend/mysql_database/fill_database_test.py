from mysql_database.connect import Connect

from mysql_database.tournaments import Tournaments
from mysql_database.rounds import Rounds
from mysql_database.games import Games
from mysql_database.players import Players
from mysql_database.num_players import Num_players

DB_CONFIG_FILE = "mysql_database/db.ini"

tournaments_instance = Tournaments(DB_CONFIG_FILE)
rounds_instance = Rounds(DB_CONFIG_FILE)
games_instance = Games(DB_CONFIG_FILE)
players_instance = Players(DB_CONFIG_FILE)
num_players_instance = Num_players(DB_CONFIG_FILE)
import random

# tournaments_instance.add_tournament([3])

rounds_instance.add_round([1, '2022-03-08 06:00:00', '2022-03-09 09:00:00'])

for i in range(4):
    id = players_instance.add_player([f"nft{i + 1}", f"address_{i + 1}", f"user_{i + 1}", f"tier_{i + 1}"])
    players_instance.update({"id": id, "bounty": random.random() * 200.0})
