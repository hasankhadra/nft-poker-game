from connect import Connect

create_table_tournament = """

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

crsr.execute(create_table_tournament)
crsr.execute(create_table_rounds)
crsr.execute(create_table_games)
crsr.execute(create_table_players)

conn.commit()
conn.close()