from app import app, db
from os import getenv
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy.sql import text
from flask import session



def login(username, password):
    sql = text("SELECT id, password FROM users WHERE username=:username")
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()
    if not user:
        return False
    else:
        if check_password_hash(user.password, password):
            session["user_id"] = user.id
            session["username"] = username

            return True
        else:
            return False


def register(username, password):
    hash_value = generate_password_hash(password)
    try:
        sql = text("INSERT INTO users (username, password) VALUES (:username, :password)")
        db.session.execute(sql, {"username":username, "password":hash_value})
        db.session.commit()
    except:
        return False
    return login(username, password)
    
	
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

    sql = text("INSERT INTO classes (name) VALUES (:class_name)")
    db.session.execute(sql, {"class_name": class_name})
    db.session.commit()
    
def send_message(user_id, class_id, content):
        sql = text("INSERT INTO messages (user_id, class_id, content) VALUES (:user_id, :class_id, :content)")
        db.session.execute(sql, {"user_id": user_id, "class_id": class_id, "content": content})
        db.session.commit()

def get_messages(class_id):
    sql = text("SELECT m.content, u.username, m.sent_at FROM messages m JOIN users u ON m.user_id = u.id WHERE m.class_id = :class_id ORDER BY m.sent_at")
    result = db.session.execute(sql, {"class_id": class_id})
    messages = result.fetchall()
    return messages
    
    
def logout():
	del session["user_id"]
  
    
