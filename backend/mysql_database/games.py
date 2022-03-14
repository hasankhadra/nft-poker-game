from connect import Connect

class Games:
    
    def __init__(self):
        self.db = 'nft_poker_game'
        self.config_file = 'db.ini'
        self.connect = Connect(self.config_file)
        if not self.is_games_exist():
            self.create_table()
        
    def init(self):
        return self.connect.init(self.db)
        
    def is_games_exist(self):
        conn, crsr = self.init()
        crsr.execute("show tables;")
        tables = crsr.fetchall()
        tables = [item[0] for item in tables]
        conn.commit()
        conn.close()
        return 'games' in tables  
    
    def delete_table(self):
        conn, crsr = self.init()

        crsr.execute("DROP TABLE games;")
        
        conn.commit()
        conn.close()
    
    def clear_table(self):
        conn, crsr = self.init()
        
        crsr.execute("DELETE FROM games;")
        
        conn.commit()
        conn.close()
     
    def create_table(self):
        conn, crsr = self.init()
        
        crsr.execute("""
                     CREATE TABLE IF NOT EXISTS games (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        round_id INT NOT NULL,
                        player1_id INT NOT NULL,
                        player2_id INT NOT NULL,
                        winner_id INT,
                        FOREIGN KEY (round_id) REFERENCES rounds(id),
                        FOREIGN KEY (player1_id) REFERENCES players(id),
                        FOREIGN KEY (player2_id) REFERENCES players(id),
                        FOREIGN KEY (winner_id) REFERENCES players(id)
                        );
                     """)
        conn.commit()
        conn.close()
    
    def add_game(self, game_info: list):
        """
        :param game_info: list containing [round_id, player1_id, player2_id]
        """
        
        if len(game_info) != 3:
            return

        conn, crsr = self.init()
        crsr.execute("""INSERT INTO games (round_id, player1_id, player2_id) 
                     VALUES (%s, %s, %s)""", game_info)
        
        conn.commit()
        conn.close()        
    
    def retrieve_games(self, limit: int):
        conn, crsr = self.init()
        
        crsr.execute("SELECT * FROM games limit %s", [limit])
        retrieved = crsr.fetchall()
        conn.commit()
        conn.close()
        return retrieved

    def get_games_from_round(self, round_id: int):
        conn, crsr = self.init()
        
        crsr.execute("SELECT * FROM games WHERE round_id = %s", [round_id])
        retrieved = crsr.fetchall()
        conn.commit()
        conn.close()
        return retrieved
    
    def get_game(self, game_id):
        conn, crsr = self.init()

        crsr.execute(f"SELECT * FROM games WHERE id = %s;", [game_id])

        retrieved = None
        try:
            retrieved =  crsr.fetchall()[0]
        except:
            pass
        conn.commit()
        conn.close()
        return retrieved

    def update(self, to_update_info: dict):
        """
        A method to update the games table. It ensures that the winner should be one of the players in the game.
        :param to_update_info: a dictionary which only contains the keys winner_id and id.
        """
        
        winner_id = to_update_info['winner_id']
        game_id = to_update_info['id']
        values = [winner_id, game_id]

        this_game = self.get_game(game_id)

        assert this_game and (winner_id == game_id[1] or winner_id == game_id[2]) \
                and game_id[3] is None

        conn, crsr = self.init()

        crsr.execute(f"UPDATE games SET winner_id = %s WHERE id = %s", values)
        conn.commit()
        conn.close()
        
if __name__ == "__main__":
    games_instance = Games()
    games_instance.add_game([1, 3, 4])