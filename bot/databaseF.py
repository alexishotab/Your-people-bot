import sqlite3
import random
class Database:
    def __init__(self,database_file):
        self.connection=sqlite3.connect(database_file,check_same_thread = False)
        self.cursor =self.connection.cursor()
    def add_queue(self,chat_id):
        with self.connection:
            self.cursor.execute("INSERT INTO `queue` (`chat_id`) VALUES(?)",(chat_id,))
            self.connection.commit()
            users=self.cursor.execute("SELECT * FROM `queue`")

    def delete_queue(self,chat_id):
        with self.connection:
            self.cursor.execute("DELETE FROM `queue` WHERE `chat_id` = ?",(chat_id,))
            self.connection.commit()
            
    def get_chat(self):
        with self.connection:
            chat=self.cursor.execute("SELECT * FROM `queue`", ()).fetchmany(1)
            if (bool(len(chat))):
                for row in chat:
                    user_info=row[1]
                    return user_info
            else:
                return False#######################

    def create_chat(self,chat_one,chat_two):
        with self.connection:
            if chat_two!=0:
                self.cursor.execute("DELETE FROM `queue` WHERE `chat_id` = ?",(chat_two,))
                self.cursor.execute("INSERT INTO `chats` (`chat_one`,`chat_two`) VALUES(?,?)",(chat_one,chat_two,))
                self.connection.commit()
                return True            
            else:
                #go to queqe
                return False

    def get_active_chat(self,chat_id):
        with self.connection:
            chat=self.cursor.execute("SELECT * FROM `chats` WHERE `chat_one` = ?",(chat_id,))
            id_chat=0
            for row in chat:
                id_chat=row[0]
                chat_info=[row[0],row[2]]
            if id_chat==0:
                chat=self.cursor.execute("SELECT * FROM `chats` WHERE `chat_two` = ?",(chat_id,))
                for row in chat:
                    id_chat=row[0]
                    chat_info=[row[0],row[1]]
                if id_chat==0:
                    return False
                else:
                    return chat_info
            else:
                return chat_info

    def delete_chat(self,id_chat):
            self.cursor.execute("DELETE FROM `chats` WHERE `id` = ?",(id_chat,))
            self.connection.commit()



    def add_user(self,chat_id,Gender, Age,Name,Description,Photo):
        self.cursor.execute("INSERT INTO `users` (`chat_id`,`gender`,`age`,`name`,`description`,`photo`) VALUES(?,?,?,?,?,?)",(chat_id,Gender,Age,Name,Description,Photo))
        self.connection.commit()

    def create_self_anketa(self,chat_id):
        with self.connection:
            anket=self.cursor.execute("SELECT `name`,`age`,`gender`,`description`,`photo` from `users` WHERE `chat_id`=?",(chat_id,))
            if anket!=[]:
                for row in anket:
                    return row[0],row[1],row[2],row[3],row[4]
            else:
                return False

    def de(self):
        with self.connection:
            self.cursor.execute("DELETE FROM `users`")
            self.cursor.execute("DELETE FROM `queue`")
            self.cursor.execute("DELETE FROM `chats`")        














'''
    def set_gender(self,chat_id,gender):
        with self.connection:
            if bool(len(chat))==False:
                self.cursor.execute("INSERT INTO `users` (`chat_id`,`gender`) VALUES (?,?)",(chat_id,))
                self.connection.commit()
                return True
            else:
                return False

    def get_gender_(self,chat_id):
        with self.connection:
            user=self.cursor.execute("SELECT * FROM `users` WHERE `chat_id`=?",(chat_id,))
            if bool(len(user)):
                for row in user:
                    return row[2]
            else:
                return False

    def get_gender_chat (self,gender):
        with self.connection:
            chat=self.cursor.execute("SELECT * FROM `queue` WHERE `gender`= ?", (gender)).fetchmany(1)
            if (bool(len(chat))):
                for row in chat:
                    user_info=[row[1],row[2]]
                    return user_info
            else:
                return[0]
'''
