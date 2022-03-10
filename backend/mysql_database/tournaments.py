from operator import is_
import re
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
        _, crsr = self.init()
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
        :param tournament_info: list containing [num_rounds]
        """
        
        # Setting the is_over in the tables to False.
        tournament_info.append(False)

        conn, crsr = self.init()
        crsr.execute("""INSERT INTO tournaments (num_rounds, is_over) 
                     VALUES (%s, %s)""", tournament_info)
        
        conn.commit()
        conn.close()        
    
    def retrieve_tournaments(self, limit: int):
        _, crsr = self.init()
        
        crsr.execute("SELECT * FROM tournaments limit %s", [limit])
        return crsr.fetchall()
    
    def update(self, to_update_info: dict):
        """
        :param tournament_info: a dictionary which only contains the keys is_over and id.
        """
        conn, crsr = self.init()
        
        is_over = to_update_info['is_over']
        tournament_id = to_update_info['id']
        values = [is_over, tournament_id]

        # Can't turn finished tournaments to unfinished.
        if not is_over:
            return

        crsr.execute(f"UPDATE tournaments SET is_over = %s WHERE id = %s", values)
        conn.commit()
        conn.close()

    def get_current_tournament_id(self):
        _, crsr = self.init()
        
        crsr.execute("SELECT id FROM tournaments WHERE is_over = False", [])
        retrieved =  crsr.fetchall()
        return retrieved[0][0]


if __name__ == "__main__":
    tournaments_instance = Tournaments('db.ini')
    tournaments_instance.clear_table()
    tournaments_instance.add_tournament([4])
    tournaments_instance.update({'id': 25, 'is_over': True})
    tournaments_instance.add_tournament([2])
    tournaments_instance.add_tournament([10])
    print(tournaments_instance.get_current_tournament_id())
    print(tournaments_instance.retrieve_tournaments(10))

    