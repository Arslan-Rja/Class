from app import db
from os import getenv
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy.sql import text
from flask import session


def login(username, password):
    sql = text("SELECT id, password, teacher FROM users WHERE username=:username")
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()
    if not user:
        return False
    else:
        if check_password_hash(user.password, password):
            session["user_id"] = user.id
            session["username"] = username
            session["teacher"] = user.teacher
            return True
        else:
            return False


def register(username, password, userType, teachercode):
    hash_value = generate_password_hash(password)
    
    sql = text("INSERT INTO users (username, password, teacher) VALUES (:username, :password, :teacher)")
    db.session.execute(sql, {"username": username, "password": hash_value, "teacher": userType == "true"})
    db.session.commit()


    if userType == "true":
        if teachercode != "TEACHER":
            return False
        else:
            sql_update_teacher = text("UPDATE users SET teacher = true WHERE username = :username")
            db.session.execute(sql_update_teacher, {"username": username})
            db.session.commit()
        
    login(username, password)
   
    return True
	
	
def get_classes():

    sql = text("SELECT id, name FROM classes")
    result = db.session.execute(sql)
    classes = result.fetchall()
    return classes

def get_class_info(class_id):

    sql = text("SELECT id, name FROM classes WHERE id = :class_id")
    result = db.session.execute(sql, {"class_id": class_id})
    class_info = result.fetchone()
    return class_info

def add_class(class_name):
    teacher = session.get("teacher", False)
    
    if teacher:
        try:
            sql = text("INSERT INTO classes (name) VALUES (:class_name)")
            db.session.execute(sql, {"class_name": class_name})
            db.session.commit()
            return True
        except:
            db.session.rollback()
            return False
    else:
        return False

        
    
def send_message(user_id, class_id, content):
        sql = text("INSERT INTO messages (user_id, class_id, content) VALUES (:user_id, :class_id, :content)")
        db.session.execute(sql, {"user_id": user_id, "class_id": class_id, "content": content})
        db.session.commit()

def get_messages(class_id):
    sql = text("SELECT m.id, m.user_id, m.content, u.username, m.sent_at FROM messages m JOIN users u ON m.user_id = u.id WHERE m.class_id = :class_id ORDER BY m.sent_at")
    result = db.session.execute(sql, {"class_id": class_id})
    messages = result.fetchall()
    return messages


    
def edit_message(message_id, editted):
    sql = text("UPDATE messages SET content = :editted WHERE id = :message_id")
    db.session.execute(sql, {"message_id": message_id, "editted": editted})
    db.session.commit()

def delete_message(message_id):
    sql = text("DELETE FROM messages WHERE id = :message_id")
    db.session.execute(sql, {"message_id": message_id})
    db.session.commit()



def logout():
	del session["user_id"]
  
    
