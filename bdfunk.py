import sqlite3 as sq


class Data_base_user():

    def __init__(self, database_file):
        self.connection = sq.connect(database_file)
        self.cur = self.connection.cursor()

    def check_for_presence_in_the_list(self, id):
        self.cur.execute(f"SELECT user_name FROM user WHERE id_telegram = {id}")
        result = self.cur.fetchall()

        if len(result) == 0:
            return False
        else:
            return True

    def get_username(self, id):
        self.cur.execute(f"SELECT user_name FROM user WHERE id_telegram = {id}")
        result = self.cur.fetchall()
        return result[0][0]

    def add_guests(self, id, name):
        self.cur.execute(f'INSERT INTO user(id_telegram,user_name,subscription_activation) VALUES({id},"{name}","False")')
        self.connection.commit()

    def clouse(self):
        self.connection.close()


class Data_base_emoje_token():

    def __init__(self, database_file):
        self.connection = sq.connect(database_file)
        self.cur = self.connection.cursor()

    def get_token(self, name):
        self.cur.execute(f'SELECT token_emoji FROM emoji WHERE name_emoji = "{name}" ')
        result = self.cur.fetchall()
        return result[0][0]
        
    def clouse(self):
        self.connection.close()



