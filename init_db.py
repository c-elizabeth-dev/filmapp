import sqlite3

def create_users_table():
    conn = sqlite3.connect('filmflix.db') 
    dbCursor = conn.cursor()
    
    dbCursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            
            username TEXT NOT NULL PRIMARY KEY,
            password TEXT NOT NULL,
            is_admin BOOLEAN
        )
    ''')

    conn.commit()
    conn.close()

if __name__ == '__main__':
    create_users_table()
