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


tournaments_instance.add_tournament([3])

rounds_instance.add_round([1, '2022-5-6 06:00:00', '2022-5-6 09:00:00'])

num_players_instance.add_row([1])

players_instance.add_player(["nft1", "add1", "user1", "tier_1"])
players_instance.add_player(["nft2", "add2", "user2", "tier_2"])
players_instance.add_player(["nft3", "add3", "user3", "tier_3"])
players_instance.add_player(["nft4", "add4", "user4", "tier_4"])
players_instance.add_player(["nft5", "add5", "user5", "tier_5"])
players_instance.add_player(["nft6", "add6", "user6", "tier_6"])

