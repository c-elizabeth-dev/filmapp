import sqlite3

def delete_users_table():
    conn = sqlite3.connect('filmflix.db') 
    dbCursor = conn.cursor()
    
    dbCursor.execute("DELETE FROM users")
    dbCursor.execute("DROP TABLE users")

    conn.commit()
    conn.close()

if __name__ == '__main__':
    delete_users_table()