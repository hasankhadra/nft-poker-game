from mysql_database.connect import Connect


connection = Connect('mysql_database/db.ini')
conn, crsr = connection.init('nft_poker_game')

def delete_table(table_name):
    crsr.execute(f"DROP TABLE IF EXISTS {table_name}")
    conn.commit()

delete_table('games')
delete_table('num_players')
delete_table('players')
delete_table('rounds')
delete_table('tournaments')
