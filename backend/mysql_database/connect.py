import MySQLdb
import configparser

class Init:
    
    def __init__(self, file, db=None):
        config = configparser.ConfigParser()
        
        config.read(file)
        
        self.host=config['mysql']['host']
        self.port=int(config['mysql']['port'])
        self.user=config['mysql']['user']
        self.passwd=config['mysql']['password']
        self.db = db if db else None
        
    def init(self):
        if self.db:
            connection = MySQLdb.connect(
                host=self.host,
                port=self.port,
                db=self.db,
                user=self.user,
                passwd=self.passwd)
        else:
            connection = MySQLdb.connect(
                host=self.host,
                port=self.port,
                user=self.user,
                passwd=self.passwd)
        return connection, connection.cursor()


class Connect:
    
    def __init__(self, file):
        self.config_file = file
        self.connect = Init(self.config_file)
        self.connection = None
    
    def init(self, db_name):
        if not self.is_db_exist(db_name):
            self.create_db(db_name)
            
        if self.connection == None:
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
    x = Connect("db.ini")
    conn, crsr = x.init("nft_poker_game")
    
    