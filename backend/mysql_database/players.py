from connect import Connect
from tournaments import Tournaments
from rounds import Rounds

class Players:
    
    def __init__(self):
        self.db = 'nft_poker_game'
        self.config_file = 'db.ini'
        self.connect = Connect(self.config_file)
        self.tournaments = Tournaments()
        self.rounds = Rounds()
        if not self.is_players_exist():
            self.create_table()
        
    def init(self):
        return self.connect.init(self.db)
        
    def is_players_exist(self):
        conn, crsr = self.init()
        crsr.execute("show tables;")
        tables = crsr.fetchall()
        tables = [item[0] for item in tables]
        return 'players' in tables  
    
    def delete_table(self):
        conn, crsr = self.init()

        crsr.execute("DROP TABLE players")
        
        conn.commit()
        conn.close()
    
    def clear_table(self):
        conn, crsr = self.init()
        
        crsr.execute("DELETE FROM players")
        
        conn.commit()
        conn.close()

    def add_player(self, player_info: list):
        """
        :param player_info: list containing [nft_id, public_address, username]
        :return: id of the inserted player
        """
        
        # TODO
        tournament_id = self.tournaments.get_current_tournament_id()
        round_id = self.rounds.get_round_id_by_round_num([tournament_id, 3])
        
        player_info += [round_id, False, 0.0]
        
        conn, crsr = self.init()
        crsr.execute("""INSERT INTO players (nft_id, public_address, username, round_id, is_rail, bounty) 
                     VALUES (%s, %s, %s, %s, %s, %s)""", player_info)
        
        new_id = crsr.lastrowid
        
        conn.commit()
        conn.close()        

        return new_id
    
    def get_players(self, limit : int =10, winners=None):
        conn, crsr = self.init()
        query = "SELECT * FROM players"
        
        if winners:
            query += f" WHERE is_rail = false"
        
        query += " limit %s"
        result = crsr.execute(query, [limit])
        
        conn.close()
        return result
    
    def get_player_by_id(self, player_info: list):
        """
        :param player_info: list containing [id]
        """
        conn, crsr = self.init()
        
        crsr.execute("SELECT * FROM players WHERE id = %s", player_info)
        result = crsr.fetchall()
        
        conn.close()
        return result
    
    def transfer_nft_ownership(self, from_public_address: str, to_public_address: str, nft_id: str):
        conn, crsr = self.init()
        
        crsr.execute("UPDATE players SET public_address = %s WHERE STRCMP(public_address, %s) = 0 AND STRCMP(nft_id, %s) = 0", 
                     [to_public_address, from_public_address, nft_id])
        
        conn.commit()
        conn.close()
               
    def update(self, to_update_info: dict):
        """
        to_update_info: dict 
        contains all columns to be updated in the format {column_name: new_value, ...}
        NOTE: The dict should contain the key-value pair {id: value} of the player
        """
        # TODO if we will update nft_id, check with web3 if the user
        # owns this nft
        conn, crsr = self.init()
        
        id = to_update_info["id"]
        del to_update_info["id"]
        
        if to_update_info.get("is_rail", None):
            assert to_update_info["is_rail"] == True
        
        assert to_update_info.get("username", -1) == -1
        assert to_update_info.get("public_address", -1) == -1
        
        keys = list(to_update_info.keys())
        values = list(to_update_info.values())
        
        update_fields_expression = ""
        for item in keys:
            update_fields_expression += item + " = %s, "
        update_fields_expression = update_fields_expression[:-2]
        
        values.append(id)
        crsr.execute(f"UPDATE players SET {update_fields_expression} WHERE id = %s", values)
        
        conn.commit()
        conn.close()

if __name__ == "__main__":
    players_instance = Players()
    
