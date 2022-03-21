from mysql_database.connect import Connect
from mysql_database.tournaments import Tournaments

class Num_players:
    
    def __init__(self, config_file):
        self.db = 'nft_poker_game'
        self.config_file = config_file
        self.connect = Connect(self.config_file)
        self.tournaments = Tournaments(config_file)
        
    def init(self):
        return self.connect.init(self.db)
        
    def is_players_exist(self):
        conn, crsr = self.init()
        crsr.execute("show tables;")
        tables = crsr.fetchall()
        tables = [item[0] for item in tables]
        return 'num_players' in tables  
    
    def delete_table(self):
        conn, crsr = self.init()

        crsr.execute("DROP TABLE num_players")
        
        conn.commit()
        conn.close()
    
    def clear_table(self):
        conn, crsr = self.init()
        
        crsr.execute("DELETE FROM num_players")
        
        conn.commit()
        conn.close()

    def add_row(self, info: list):
        """
        :param info: list containing [tournament_id]
        """
        conn, crsr = self.init()

        crsr.execute("INSERT INTO num_players (tournament_id, count) VALUES (%s, 0)", info)

        conn.commit()
        conn.close()

    
    def get_cur_count(self):
        """
        returns the number of already registered players in the current tournament
        """
        conn, crsr = self.init()
        
        values = [self.tournaments.get_current_tournament_id()]
        
        query = "SELECT count FROM num_players WHERE tournament_id = %s"

        crsr.execute(query, values)
        result = crsr.fetchall()
        
        conn.close()
        return result[0][0]
  
    def increase_players_num(self):
        cur_count = self.get_cur_count()
        self.update({"tournament_id": self.tournaments.get_current_tournament_id(), "count": cur_count + 1})

    def update(self, to_update_info: dict):
        """
        to_update_info: dict 
        contains all columns to be updated in the format {column_name: new_value, ...}
        NOTE: The dict should contain the key-value pair {tournament_id: value} of the player
        """
        conn, crsr = self.init()
        
        id = to_update_info["tournament_id"]
        del to_update_info["tournament_id"]
        
        keys = list(to_update_info.keys())
        values = list(to_update_info.values())
        
        update_fields_expression = ""
        for item in keys:
            update_fields_expression += item + " = %s, "
        update_fields_expression = update_fields_expression[:-2]
        
        values.append(id)
        crsr.execute(f"UPDATE num_players SET {update_fields_expression} WHERE tournament_id = %s", values)
        
        conn.commit()
        conn.close()

    
if __name__ == '__main__':
    num_players_instance = Num_players("db.ini")
    print(num_players_instance.get_cur_count())