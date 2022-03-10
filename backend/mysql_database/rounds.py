from connect import Connect
from datetime import datetime
from tournaments import Tournaments

class Rounds:
    
    def __init__(self):
        self.db = 'nft_poker_game'
        self.config_file = 'db.ini'
        self.connect = Connect(self.config_file)
        self.tournaments = Tournaments()
        
    def init(self):
        return self.connect.init(self.db)
        
    def is_rounds_exist(self):
        conn, crsr = self.init()
        crsr.execute("show tables;")
        tables = crsr.fetchall()
        tables = [item[0] for item in tables]
        
        conn.close()
        return 'rounds' in tables  
    
    def delete_table(self):
        conn, crsr = self.init()

        crsr.execute("DROP TABLE rounds")
        
        conn.commit()
        conn.close()
    
    def clear_table(self):
        conn, crsr = self.init()
        
        crsr.execute("DELETE FROM rounds")
        
        conn.commit()
        conn.close()
     
    def create_table(self):
        conn, crsr = self.init()
        
        crsr.execute("""
            CREATE TABLE IF NOT EXISTS rounds (
                id INT AUTO_INCREMENT PRIMARY KEY, 
                tournament_id INT NOT NULL,
                round_num INT NOT NULL,
                start_time DATE NOT NULL,
                end_time DATE NOT NULL);
            """)
        conn.commit()
        conn.close()
     
    def add_round(self, round_info: list):
        """
        :param round_info: list containing [round_num, start_time, end_time]
        :return: id of the inserted round
        """
        
        # add tournament_id 
        tournament_id = get_current_tournament_id()
        
        round_info += [tournament_id] # TODO: add tournament_id
        
        conn, crsr = self.init()
        crsr.execute("""INSERT INTO rounds (round_num, start_time, end_time, tournament_id) 
                     VALUES (%s, %s, %s, %s)""", round_info)
        
        new_id = crsr.lastrowid
        
        conn.commit()
        conn.close()        

        return new_id
    
    def get_rounds_by_tournament_id(self, round_info: list):
        """
        :param round_info: list containing [tournament_id]
        :return: tuple of tuples containing all the rounds inside a specific tournament
        """
        conn, crsr = self.init()
        res = crsr.execute("SELECT * from rounds WHERE tournament_id = %s", round_info)
        
        conn.close()
        return res
    
    def get_next_round_id(self, round_info: list):
        """
        :param round_info: list 
        containing [tournament_id, round_num]
        """
        conn, crsr = self.init()
        
        crsr.execute("SELECT id from rounds WHERE tournament_id = %s AND round_num = %s", round_info)
        try:
            id = crsr.fetchall()[0][0]
            conn.close()

            return id
        except Exception as e:
            print(e)
        return None
        
    def get_rounds(self, limit: int):
        conn, crsr = self.init()
        query = "SELECT * FROM rounds"
        
        query += " limit %s"
        crsr.execute(query, [limit])
        
        conn.close()
        return crsr.fetchall()
    
    def update(self, to_update_info: dict):
        """
        to_update_info: dict 
        contains all columns to be updated in the format {column_name: new_value, ...}
        NOTE: The dict should contain the key-value pair {id: value} of the round
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
        crsr.execute(f"UPDATE rounds SET {update_fields_expression} WHERE id = %s", values)
        
        conn.commit()
        conn.close()

if __name__ == "__main__":
    rounds_instance = Rounds()
    rounds_instance.delete_table()
    # rounds_instance.create_table()
    # rounds_instance.create_index()
    
    # rounds_instance.add_round(["address_1", "first last"])
    # rounds_instance.update({"round_num": 3, "public_address": "address_1", "full_name": "fdsds last", "is_rail": True})

"""
"CREATE INDEX public_address_hash_index ON rounds (public_address);"
"""