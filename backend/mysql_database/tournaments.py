from connect import Connect

class Tournaments:
    
    def __init__(self):
        self.db = 'nft_poker_game'
        self.config_file = 'db.ini'
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
        conn.commit()
        conn.close()
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
        
        try:
            assert len(tournament_info) == 1 and isinstance(tournament_info[0], int) \
                   and tournament_info[0] > 0
        except:
            return

        # Setting the is_over in the tables to False.
        tournament_info.append(False)

        conn, crsr = self.init()
        crsr.execute("""INSERT INTO tournaments (num_rounds, is_over) 
                     VALUES (%s, %s)""", tournament_info)
        
        conn.commit()
        conn.close()        
    
    def retrieve_tournaments(self, limit: int):
        conn, crsr = self.init()
        
        crsr.execute("SELECT * FROM tournaments limit %s", [limit])
        retrieved = crsr.fetchall()
        conn.commit()
        conn.close()
        return retrieved
    
    def update(self, to_update_info: dict):
        """
        :param to_update_info: a dictionary which only contains the keys is_over and id.
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
        conn, crsr = self.init()
        
        crsr.execute("SELECT id FROM tournaments WHERE is_over = False", [])
        
        retrieved_id = None
        try:
            retrieved_id =  crsr.fetchall()[0][0]
        except:
            pass
        conn.commit()
        conn.close()
        return retrieved_id
