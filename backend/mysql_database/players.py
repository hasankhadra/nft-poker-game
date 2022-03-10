from connect import Connect
# from tournaments import Tournaments
# from rounds import Rounds

class Players:
    
    def __init__(self):
        self.db = 'nft_poker_game'
        self.config_file = 'db.ini'
        self.connect = Connect(self.config_file)
        # self.tournaments = Tournaments()
        # self.rounds = Rounds()
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
     
    def create_table(self):
        conn, crsr = self.init()
        
        crsr.execute("""
            CREATE TABLE IF NOT EXISTS players (
                id INT AUTO_INCREMENT PRIMARY KEY, 
                nft_id INT NOT NULL,
                public_address varchar(255) NOT NULL,
                username VARCHAR(255) NOT NULL, 
                round_id INT NOT NULL,
                is_rail BOOLEAN NOT NULL,
                bounty double NOT NULL,
                FOREIGN KEY (round_id) REFERENCES rounds(id));
            """)
        conn.commit()
        conn.close()
     
    def add_player(self, player_info: list):
        """
        :param player_info: list containing [nft_id, public_address, username]
        :return: id of the inserted player
        """
        
        # add round_id, is_rail, bounty info
        # tournament_id = get_current_tournament_id()
        round_id = 1 #, get_current_round_id(tournament_id)
        
        player_info += [round_id, False, 0.0] # TODO: add tournament_id
        
        conn, crsr = self.init()
        crsr.execute("""INSERT INTO players (nft_id, public_address, username, round_id, is_rail, bounty) 
                     VALUES (%s, %s, %s, %s, %s, %s)""", player_info)
        
        new_id = crsr.lastrowid
        
        conn.commit()
        conn.close()        

        return new_id
    
    def get_players(self, limit: int, winners=None):
        conn, crsr = self.init()
        query = "SELECT * FROM players"
        
        if winners:
            query += " WHERE is_rail == TRUE"
        
        query += " limit %s"
        crsr.execute(query, [limit])
        return crsr.fetchall()
    
    def update(self, to_update_info: dict):
        """
        to_update_info: dict 
        contains all columns to be updated in the format {column_name: new_value, ...}
        NOTE: The dict should contain the key-value pair {id: value} of the player
        """
        conn, crsr = self.init()
        
        id = to_update_info["id"]
        del to_update_info["id"]
        
        keys = list(to_update_info.keys())
        values = list(to_update_info.values())
        
        update_fields_expression = ""
        for item in keys:
            update_fields_expression += item + " = " + "%s, "
        update_fields_expression = update_fields_expression[:-2]
        
        values.append(id)
        crsr.execute(f"UPDATE players SET {update_fields_expression} WHERE id = %s", values)
        
        conn.commit()
        conn.close()

if __name__ == "__main__":
    players_instance = Players()
    players_instance.delete_table()
    # players_instance.create_table()
    # players_instance.create_index()
    
    # players_instance.add_player(["address_1", "first last"])
    # players_instance.update({"round_num": 3, "public_address": "address_1", "full_name": "fdsds last", "is_rail": True})

"""
"CREATE INDEX public_address_hash_index ON players (public_address);"
"""