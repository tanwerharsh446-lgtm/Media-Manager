import sqlite3
class data:
    def __init__(self):
        self.con = sqlite3.connect("users_data.db")
        self.cur = self.con.cursor()
    def create_table(self):
        self.cur.execute("""CREATE TABLE IF NOT EXISTS users(
                         id INTEGER PRIMARY KEY AUTOINCREMENT,
                         email TEXT,
                         name TEXT,
                         password TEXT)""")
        
    

        
        self.con.commit()

    def insert(self,value,value2,value3):
        self.create_table()

        self.cur.execute("INSERT INTO users(name,email,password) VALUES(?,?,?)",
                         (value,value2,value3))
        
        self.con.commit()
    def in_name(self,value):
        self.create_table()

        self.cur.execute("INSERT INTO users(name)VALUES(?)",
                         (value,))
        
        self.con.commit()

    def in_email(self,value):
        self.create_table()

        self.cur.execute("INSERT INTO users(email)VALUES(?)",
                         (value,))
        
        self.con.commit()

    def in_password(self,value):
        self.create_table()

        self.cur.execute("INSERT INTO users(password)VALUES(?)",
                         (value,))
        
        self.con.commit()

    def show_name(self,value):

        self.cur.execute("SELECT name FROM users WHERE email=?",(value,))
        name = self.cur.fetchone()
        return name
    
    def show_password(self,value):

        self.cur.execute("SELECT password FROM users WHERE email=?",(value,))
        password = self.cur.fetchone()
        return password
    
    def show_id(self,value):

        self.cur.execute("SELECT id FROM users WHERE email=?",(value,))
        id = self.cur.fetchone()
        return id
        
    def update_password(self,value2,value):
        self.cur.execute("UPDATE users SET password=? WHERE email=?",
                         (value,value2))
        self.con.commit()

    def delete(self,value):
        self.cur.execute("DELETE FROM users WHERE email=?",
                         (value,))
        self.con.commit()

    def show_all(self):
        self.cur.execute("SELECT * FROM users")
        rows = self.cur.fetchall()
        return rows
    
    def z(self):
        self.cur.execute("DELETE FROM users")
        self.con.commit()

    def create_table_notes(self):
        self.cur.execute("""CREATE TABLE IF NOT EXISTS notes(
                         id INTEGER PRIMARY KEY AUTOINCREMENT,
                         email TEXT,
                         note TEXT
                         )""")
        self.con.commit()

    def insert_notes(self,email,note):
        self.create_table_notes()
        self.cur.execute("INSERT INTO notes(email,note) VALUES(?,?)",(email,note))
        self.con.commit()

    def get_notes(self,email):
        self.cur.execute("SELECT note FROM notes WHERE email=?",(email,))
        rows = self.cur.fetchall()
        if rows:
            return rows
        return False
    def get_id(self,email):
        self.cur.execute("SELECT id FROM notes WHERE email=?",(email,))
        rows = self.cur.fetchall()
        if rows:
            return rows
        return False
    def delete_note(self,id,email):
        self.cur.execute("DELETE FROM notes WHERE email=? AND id=?",(email,id))
        self.con.commit()
        

