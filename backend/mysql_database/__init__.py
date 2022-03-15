from mysql_database.connect import Connect
from MySQLdb import OperationalError

create_table_tournaments = """
CREATE TABLE IF NOT EXISTS tournaments (
    id INT AUTO_INCREMENT PRIMARY KEY, 
    num_rounds INT NOT NULL,
    is_over BOOLEAN NOT NULL);
"""

create_table_rounds = """
CREATE TABLE IF NOT EXISTS rounds (
    id INT AUTO_INCREMENT PRIMARY KEY, 
    tournament_id INT NOT NULL,
    round_num INT NOT NULL,
    start_time DATE NOT NULL,
    end_time DATE NOT NULL,
    FOREIGN KEY (tournament_id) REFERENCES tournaments(id));
"""

create_table_games = """
CREATE TABLE IF NOT EXISTS games (
    id INT AUTO_INCREMENT PRIMARY KEY,
    round_id INT NOT NULL,
    player1_id INT NOT NULL,
    player2_id INT NOT NULL,
    player1_combo VARCHAR(20),
    player2_combo VARCHAR(20),
    winner_id INT,
    bad_beat BOOLEAN,
    FOREIGN KEY (round_id) REFERENCES rounds(id),
    FOREIGN KEY (player1_id) REFERENCES players(id),
    FOREIGN KEY (player2_id) REFERENCES players(id),
    FOREIGN KEY (winner_id) REFERENCES players(id)
    );
"""

create_table_players = """
CREATE TABLE IF NOT EXISTS players (
    id INT AUTO_INCREMENT PRIMARY KEY, 
    nft_id VARCHAR(255) NOT NULL,
    public_address varchar(255) NOT NULL,
    username VARCHAR(255) NOT NULL, 
    round_id INT NOT NULL,
    nft_tier VARCHAR(40),
    is_rail BOOLEAN NOT NULL,
    bounty double NOT NULL,
    FOREIGN KEY (round_id) REFERENCES rounds(id));
"""

create_table_total_players = """
CREATE TABLE IF NOT EXISTS num_players (
    tournament_id INT NOT NULL,
    count INT NOT NULL,
    FOREIGN KEY (tournament_id) REFERENCES tournaments(id));
"""


table_players_columns = ['id', 'nft_id', 'public_address', 'username', 'round_id', 
                         'nft_tier', 'is_rail', 'bounty']


connection = Connect('mysql_database/db.ini')
conn, crsr = connection.init('nft_poker_game')

crsr.execute(create_table_tournaments)
crsr.execute(create_table_rounds)
crsr.execute(create_table_players)
crsr.execute(create_table_games)
crsr.execute(create_table_total_players)


# creating indexes
players_public_address_index = "CREATE INDEX public_address_index ON players (public_address);"
tournaments_is_over_index = "CREATE INDEX is_over_index ON tournaments (is_over);"
games_round_id_index = "CREATE INDEX round_id_index ON games (round_id);"
rounds_tournament_id_index = "CREATE INDEX tournament_id_index ON rounds (tournament_id);"
rounds_round_num_index = "CREATE INDEX round_num_index ON rounds (round_num);"

try:
    crsr.execute(players_public_address_index)
    crsr.execute(tournaments_is_over_index)
    crsr.execute(games_round_id_index)
    crsr.execute(rounds_tournament_id_index)
    crsr.execute(rounds_round_num_index)
except OperationalError as e:
    print(e)
    
conn.commit()
conn.close()