import MySQLdb
import configparser

class Init:
    
    def __init__(self, file, db=None):
        config = configparser.ConfigParser()
        
        config.read(file)
        if db is None:
            self.conn = MySQLdb.connect(
                host=config['mysql']['host'],
                port=int(config['mysql']['port']),
                user=config['mysql']['user'],
                passwd=config['mysql']['password'])
        else:
            self.conn = MySQLdb.connect(
                host=config['mysql']['host'],
                port=int(config['mysql']['port']),
                db=db,
                user=config['mysql']['user'],
                passwd=config['mysql']['password'])
        
    def init(self):
        crsr = self.conn.cursor()
        return self.conn, crsr


class Connect:
    
    def __init__(self, file):
        self.config_file = file
        self.connect = Init(self.config_file)
        self.connection = None
    
    def init(self, db_name):
        if not self.is_db_exist(db_name):
            self.create_db(db_name)
            
        if not self.connection:
            self.connection = Init(self.config_file, db_name)
        return self.connection.init()
        
    def is_db_exist(self, db_name):
        conn, crsr = self.connect.init()
        crsr.execute("SHOW DATABASES;")
        databases = crsr.fetchall()
        databases = [item[0] for item in databases]
        return db_name in databases
        
    def create_db(self, db_name):
        conn, crsr = self.connect.init()
        crsr.execute(f"CREATE DATABASE {db_name}")
        conn.commit()
        conn.close()
        


if __name__ == "__main__":
    x = Init("db.ini")
    conn, crsr = x.init("nft_poker_game")
    
    