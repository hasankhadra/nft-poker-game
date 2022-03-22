from mysql_database.connect import Connect
from mysql_database.tournaments import Tournaments
import json 
from datetime import datetime

class Rounds:
    
    def __init__(self, config_file):
        self.db = 'nft_poker_game'
        self.config_file = config_file
        self.connect = Connect(self.config_file)
        self.tournaments = Tournaments(config_file)
        
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
     
    def add_round(self, round_info: list):
        """
        :param round_info: list containing [round_num, start_time, end_time]
        :return: id of the inserted round
        """
        
        # add tournament_id 
        tournament_id = self.tournaments.get_current_tournament_id()
        
        round_info += [tournament_id]
        
        conn, crsr = self.init()
        crsr.execute("""INSERT INTO rounds (round_num, start_time, end_time, tournament_id) 
                     VALUES (%s, %s, %s, %s)""", round_info)
        
        new_id = crsr.lastrowid
        
        conn.commit()
        conn.close()        

        return new_id
    
    def get_cur_round(self):
        """
        returns the current active round. In case no round is active now,
        it returns the next upcoming round.
        """
        conn, crsr = self.init()
        
        tournament_id = self.tournaments.get_current_tournament_id()
        
        crsr.execute("SELECT * FROM rounds WHERE tournament_id = %s", [tournament_id])
        
        results = crsr.fetchall()
        
        results = json.loads(self._get_json_format(crsr, results))
        
        conn.close()
        
        cur_round_index = -1
        
        for index in range(len(results)):
            result = results[index]
            end_time = datetime.strptime(result["end_time"], '%Y-%m-%d %H:%M:%S')
            start_time = datetime.strptime(result["start_time"], '%Y-%m-%d %H:%M:%S')
            
            cur_time = datetime.now()
            
            if end_time < cur_time:
                continue
            
            if cur_round_index == -1:
                cur_round_index = index
                continue
            
            if end_time < datetime.strptime(results[cur_round_index]["start_time"], '%Y-%m-%d %H:%M:%S'):
                cur_round_index = index
            
        return results[cur_round_index]
    
    def _get_json_format(self, crsr, results):
        row_headers=[item[0] for item in crsr.description]
        json_data = []
        for row in results:
            json_data.append(dict(zip(row_headers, row)))
        return json_data
    
    def get_rounds_by(self, by: dict, get_json_format=None):
        """
        :param by: dict containing the conditions for the select statement
        where the key is the name of the column and the value is the desired value in
        the rows
        """
        
        assert len(by.keys()) > 0
        
        conn, crsr = self.init()
        
        query = "SELECT * FROM rounds WHERE"
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
  
    def get_round_id_by_round_num(self, round_info: list):
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
        assert False, "cannot edit any column"
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
