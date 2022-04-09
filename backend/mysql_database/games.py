from typing import List, Tuple
from mysql_database.connect import Connect
import json 


class Games:
    
    editable_fields = ['winner_id', 'player1_combo', 'player2_combo', 'bad_beat', 'flops']

    def __init__(self, config_file):
        self.db = 'nft_poker_game'
        self.config_file = config_file
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

    def add_round_games(self, round_id, games_info: List[Tuple]):
        """
        :param games_info: a list of tuples representing the games. Each game must 
        be of the format (player1_id, player2_id).
        """

        for element in games_info:
            assert len(element) == 2

        one_row = """ (%s, %s, %s),"""

        query = "INSERT INTO games (round_id, player1_id, player2_id) VALUES"
        query += one_row * len(games_info)
        query = query[:-1] + ';'

        game_info = [(round_id, *element) for element in games_info]
        values = list(sum(game_info, ()))
        conn, crsr = self.init()
        crsr.execute(query, values)
        
        conn.commit()
        conn.close()  

    def get_games_by(self, by: dict, get_json_format=None):
        """
        :param by: dict containing the conditions for the select statement
        where the key is the name of the column and the value is the desired value in
        the rows
        """
        
        assert len(by.keys()) > 0
        
        conn, crsr = self.init()
        
        query = "SELECT * FROM games WHERE"
        conditions = []
        
        for item, value in by.items():
            query += f" {item} = %s AND"
            conditions.append(value)
        
        query = query[:-3]
        
        crsr.execute(query, conditions)
        results = crsr.fetchall()
        
        if get_json_format:
            results = self._get_json_format(crsr, results)
        
        conn.close()
        return results

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
    
    def _get_json_format(self, crsr, results):
        row_headers=[item[0] for item in crsr.description]
        json_data = []
        for row in results:
            json_data.append(dict(zip(row_headers, row)))
        return json_data
   
    def get_games_from_round(self, game_info: list):
        """
        :param game_info: list containing [round_id]
        """
        conn, crsr = self.init()
        
        crsr.execute("SELECT * FROM games WHERE round_id = %s", game_info)
        retrieved = crsr.fetchall()
        conn.commit()
        conn.close()
        return retrieved
    
    def get_game(self, game_info: list, get_json_format=None):
        """
        :param game_info: list containing [game_id]
        """
        conn, crsr = self.init()

        crsr.execute(f"SELECT * FROM games WHERE id = %s;", game_info)
        
        results = crsr.fetchall()
        
        if get_json_format:
            results = self._get_json_format(crsr, results)
        
        conn.close()
        return results

    def update(self, to_update_info: dict):
        """
        A method to update the games table. It ensures that the winner should be one of the players in the game.
        :param to_update_info: a dictionary which only contains the keys winner_id and id.
        """
        game_id = to_update_info['id']
        del to_update_info['id']

        for key in to_update_info:
            assert key in Games.editable_fields

        this_game = self.get_game([game_id])[0]
        print(this_game)

        if 'winner_id' in to_update_info:
            assert this_game and (to_update_info['winner_id'] == this_game[3] or to_update_info['winner_id'] == this_game[2])
        
        
        values = list(to_update_info.values()) + [game_id]
        
        update_fields_expression = ""
        for item in to_update_info:
            update_fields_expression += item + " = %s, "
        update_fields_expression = update_fields_expression[:-2]
        

        conn, crsr = self.init()
        
        crsr.execute(f"UPDATE games SET {update_fields_expression} WHERE id = %s", values)
        conn.commit()
        conn.close()
