from connect import Connect

from . import create_table_games

class Games:
    
    editable_fields = ['winner_id', 'player1_combo', 'player2_combo', 'bad_beat']

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
        
        crsr.execute(create_table_games)
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
        game_id = to_update_info['id']
        del to_update_info['id']

        for key in to_update_info:
            assert key in Games.editable_fields

        this_game = self.get_game(game_id)

        if 'winner_id' in to_update_info:
            assert this_game and (to_update_info['winner_id'] == this_game[1] \
                             or to_update_info['winner_id'] == this_game[2]) is None
        
        
        values = list(to_update_info.values()) + [game_id]
        
        update_fields_expression = ""
        for item in to_update_info:
            update_fields_expression += item + " = %s, "
        update_fields_expression = update_fields_expression[:-2]
        

        conn, crsr = self.init()

        crsr.execute(f"UPDATE players SET {update_fields_expression} WHERE id = %s", values)
        conn.commit()
        conn.close()
        
if __name__ == "__main__":
    games_instance = Games()
    games_instance.add_game([1, 3, 4])