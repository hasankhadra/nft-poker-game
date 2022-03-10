from connect import Connect

class Players:
    
    def __init__(self, file):
        self.db = 'nft_poker_game'
        self.config_file = file
        self.connect = Connect(self.config_file)
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
                         public_address varchar(255),
                         full_name VARCHAR(255), 
                         round_num INT,
                         is_rail BOOLEAN);
                     """)
        conn.commit()
        conn.close()
     
    def add_player(self, player_info: list):
        """
        :param player_info: list containing [public_address, full_name]
        """
        
        # add round_num and is_rail
        player_info.append(0)
        player_info.append(False)
        
        conn, crsr = self.init()
        crsr.execute("""INSERT INTO players (public_address, full_name, round_num, is_rail) 
                     VALUES (%s, %s, %s, %s)""", player_info)
        
        conn.commit()
        conn.close()        
    
    def retrieve_players(self, limit: int):
        conn, crsr = self.init()
        
        crsr.execute("SELECT * FROM players limit %s", [limit])
        return crsr.fetchall()
    
    def create_index(self):
        conn, crsr = self.init()

        crsr.execute("CREATE INDEX public_address_hash_index ON players (public_address);")
        
        conn.commit()
        conn.close()
    
    def update(self, to_update_info: dict):
        conn, crsr = self.init()
        
        public_address = to_update_info["public_address"]
        del to_update_info["public_address"]
        
        keys = list(to_update_info.keys())
        values = list(to_update_info.values())
        
        update_fields_expression = ""
        for item in keys:
            update_fields_expression += item + " = " + "%s, "
        update_fields_expression = update_fields_expression[:-2]
        
        values.append(public_address)
        crsr.execute(f"UPDATE players SET {update_fields_expression} WHERE public_address = %s", values)
        
        conn.commit()
        conn.close()

# TODO
"""
- Add max_rounds to table
- user_name instead of full_name

- Edit retrieve players (add round=None parameter)
"""
if __name__ == "__main__":
    players_instance = Players('db.ini')
    # players_instance.delete_table()
    players_instance.create_table()
    # players_instance.create_index()
    
    players_instance.add_player(["address_1", "first last"])
    players_instance.update({"round_num": 3, "public_address": "address_1", "full_name": "fdsds last", "is_rail": True})

    