from typing import List, Tuple
from mysql_database.connect import Connect
import json 

class GamesDraws:

    def __init__(self, config_file):
        self.db = 'nft_poker_game'
        self.config_file = config_file
        self.connect = Connect(self.config_file)

    def add_game(self, game_info: list):
        """
        :param game_info: list containing [game_id, player1_combo, player2_combo, flops]
        """
        
        if len(game_info) != 4:
            return

        conn, crsr = self.init()
        crsr.execute("""INSERT INTO games_draws (game_id, player1_combo, player2_combo, flops) 
                     VALUES (%s, %s, %s, %s)""", game_info)
        
        conn.commit()
        conn.close()        
    
    def get_games_logs(self, games_ids: list, get_json_format=None):
        """returns all game draws given a list of (game_id)s

        Args:
            games_ids (list): a list of games ids
            get_json_format : True or False

        Returns:
            [list]: list of (dictionaries/lists) 
        """
        
        assert len(games_ids) > 0, "No games ids given"
        
        conn, crsr = self.init()
        
        query = "SELECT * FROM games WHERE " + "game_id = %s AND " * len(games_ids)
        query = query[:-4]
        
        crsr.execute(query, games_ids)
        
        results = crsr.fetchall()
        
        if get_json_format:
            results = self._get_json_format(crsr, results)
        
        conn.commit()
        conn.close()
        
        return results
    
    def _get_json_format(self, crsr, results):
        row_headers=[item[0] for item in crsr.description]
        json_data = []
        for row in results:
            json_data.append(dict(zip(row_headers, row)))
        return json_data
