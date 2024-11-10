import sqlite3
#Db name
DATABASE_NAME='portfolio_database.db'

def add_db_table(table_name, columns):#columns is a tuple and all are strings
        try:
            dbcon=sqlite3.connect(DATABASE_NAME)
            dbcon.execute(f'CREATE TABLE {table_name} {columns}')
            dbcon.close()
            print( f'****db {table_name} tables created successfuly****')

        except sqlite3.OperationalError as err:
            print(f'****db table {table_name} could not be created ({err}) ****')

def save(table_name,values):
        dbcon=sqlite3.connect(DATABASE_NAME)
        cur=dbcon.cursor()
        if table_name=='Projects':
             cur.execute("INSERT INTO Projects (name,client,description,project_image_url,project_image_filename) VALUES (?,?,?,?,?)",values)
        elif table_name =='Messages':
             cur.execute("INSERT INTO Messages (visitor_name,visitor_email,subject,message) VALUES (?,?,?,?)",values)
        elif table_name =='Testimonials':
             cur.execute("INSERT INTO Testimonials (client_name,client_message) VALUES (?,?)",values)
        elif table_name =='Blogs':
             cur.execute("INSERT INTO Blogs (title,aurther,description) VALUES (?,?,?)",values)
        if table_name=='Art':
             cur.execute("INSERT INTO Art (name,category,description,price,art_image_url,art_image_filename) VALUES (?,?,?,?,?,?)",values)
        dbcon.commit()
        dbcon.close()

def delete(table_name,id):
        dbcon = sqlite3.connect(DATABASE_NAME)
        cur = dbcon.cursor()

        # Use parameterized query to safely delete the row
        query = f"DELETE FROM {table_name} WHERE id = ?"
        cur.execute(query, (id))

        dbcon.commit()
        dbcon.close()


def get( table_name):
        dbcon=sqlite3.connect(DATABASE_NAME)
        cur=dbcon.cursor()
        cur.execute(f"select * from {table_name}")
        rows = cur.fetchall()
        dbcon.close()
        return rows

class Message:
    def __init__(self, name, email,subject, message):
        self.visitor_name=name
        self.visitor_email=email
        self.message=message
        self.subject=subject
        self.db_table_name='Messages'


    def __str__(self) -> str:
        return f"{self.subject} -{self.visitor_name}"
    
    def create_db_table():
         add_db_table('Messages','(ID INTEGER PRIMARY KEY AUTOINCREMENT, visitor_name TEXT NOT NULL, visitor_email EMAIL NOT NULL, subject TEXT  NOT NULL, message TEXT NOT NULL , time_submitted TIMESTAMP DEFAULT CURRENT_TIMESTAMP)')

    def add_to_db(self):
         save(self.db_table_name,(self.visitor_name,self.visitor_email, self.subject, self.message))

    def get_from_db():
        return get('Messages')
    
    def delete_message(id):
         delete("messages", id)


class Blog:
    def __init__(self, title, aurther, description):
        self.title=title
        self.aurther=aurther
        self.description=description
        self.db_table_name='Blogs'

    def __str__(self) -> str:
        return self.title
        
    def create_db_table():
         add_db_table('Blogs','(ID INTEGER PRIMARY KEY AUTOINCREMENT,title TEXT , aurther TEXT, description TEXT, time_submitted TIMESTAMP DEFAULT CURRENT_TIMESTAMP)')
    
    def save_to_db(self):
        save(self.db_table_name, (self.title,self.aurther,self.description) )
        

    def remove_from_db(id):
        delete('Blogs', id)

    def get_from_db():
        return get('Blogs')


class Art:
    def __init__(self, name, category, description, price, art_image_url, art_image_filename):
        self.name=name
        self.category=category
        self.description=description
        self.price=price
        self.art_image_url=art_image_url
        self.art_image_filename=art_image_filename
        self.db_table_name='Art'
        db_table_name='Art'

    def __str__(self) -> str:
        return self.name
        
    def create_db_table():
         add_db_table('Art','(ID INTEGER PRIMARY KEY AUTOINCREMENT,name TEXT , category TEXT, description TEXT, price TEXT, art_image_url TEXT, art_image_filename TEXT)')
    
    def save_to_db(self):
        save(self.db_table_name, (self.name,self.category,self.description, self.price, self.art_image_url,self.art_image_filename) )
        

    def remove_from_db(id):
        delete('Art', id)

    def get_from_db():
        return get('Art')


'''dbcon=sqlite3.connect(DATABASE_NAME)
dbcon.execute("DROP TABLE Art") 
print('tbl deleted')
dbcon.close()
'''

Message.create_db_table()
Blog.create_db_table()
Art.create_db_table()

