from connect import Connect

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
    winner_id INT NOT NULL,
    FOREIGN KEY (round_id) REFERENCES rounds(id),
    FOREIGN KEY (player1_id) REFERENCES players(id),
    FOREIGN KEY (player2_id) REFERENCES players(id),
    FOREIGN KEY (winner_id) REFERENCES players(id)
    );
"""

create_table_players = """
CREATE TABLE IF NOT EXISTS players (
    id INT AUTO_INCREMENT PRIMARY KEY, 
    nft_id INT NOT NULL,
    public_address varchar(255) NOT NULL,
    username VARCHAR(255) NOT NULL, 
    round_id INT NOT NULL,
    is_rail BOOLEAN NOT NULL,
    bounty double NOT NULL,
    FOREIGN KEY (round_id) REFERENCES rounds(id));
"""

connection = Connect('db.ini')
conn, crsr = connection.init('nft_poker_game')

crsr.execute(create_table_tournaments)
crsr.execute(create_table_rounds)
crsr.execute(create_table_players)
crsr.execute(create_table_games)

conn.commit()
conn.close()