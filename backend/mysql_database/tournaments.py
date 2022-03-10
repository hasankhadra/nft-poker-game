from connect import Connect

class Tournaments:
    
    def __init__(self, file):
        self.db = 'nft_poker_game'
        self.config_file = file
        self.connect = Connect(self.config_file)
        if not self.is_tournaments_exist():
            self.create_table()
        
    def init(self):
        return self.connect.init(self.db)
        
    def is_tournaments_exist(self):
        conn, crsr = self.init()
        crsr.execute("show tables;")
        tables = crsr.fetchall()
        tables = [item[0] for item in tables]
        return 'tournaments' in tables  
    
    def delete_table(self):
        conn, crsr = self.init()

        crsr.execute("DROP TABLE tournaments;")
        
        conn.commit()
        conn.close()
    
    def clear_table(self):
        conn, crsr = self.init()
        
        crsr.execute("DELETE FROM tournaments;")
        
        conn.commit()
        conn.close()
     
    def create_table(self):
        conn, crsr = self.init()
        
        crsr.execute("""
                     CREATE TABLE IF NOT EXISTS tournaments (
                        id INT AUTO_INCREMENT PRIMARY KEY, 
                        num_rounds INT NOT NULL,
                        is_over BOOLEAN NOT NULL);
                     """)
        conn.commit()
        conn.close()
     
    def add_tournament(self, tournament_info: list):
        """
        :param tournament_info: list containing [public_address, full_name]
        """
        
        # add round_num and is_rail
        tournament_info.append(0)
        tournament_info.append(False)
        
        conn, crsr = self.init()
        crsr.execute("""INSERT INTO tournaments (public_address, full_name, round_num, is_rail) 
                     VALUES (%s, %s, %s, %s)""", tournament_info)
        
        conn.commit()
        conn.close()        
    
    def retrieve_tournaments(self, limit: int):
        conn, crsr = self.init()
        
        crsr.execute("SELECT * FROM tournaments limit %s", [limit])
        return crsr.fetchall()
    
    def create_index(self):
        conn, crsr = self.init()

        crsr.execute("CREATE INDEX public_address_hash_index ON tournaments (public_address);")
        
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
        crsr.execute(f"UPDATE tournaments SET {update_fields_expression} WHERE public_address = %s", values)
        
        conn.commit()
        conn.close()


if __name__ == "__main__":
    tournaments_instance = Tournaments('db.ini')
    # tournaments_instance.delete_table()
    tournaments_instance.create_table()
    # tournaments_instance.create_index()
    
    tournaments_instance.add_tournament(["address_1", "first last"])
    tournaments_instance.update({"round_num": 3, "public_address": "address_1", "full_name": "fdsds last", "is_rail": True})

    