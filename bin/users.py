from app import db
from os import getenv
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy.sql import text
from flask import session
from datetime import datetime



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
    is_teacher = userType.lower() == "true"

    try:
        if is_teacher:
            if not teachercode or teachercode != "TEACHER":
                raise ValueError("Invalid or missing teacher code")
                
        sql = text("INSERT INTO users (username, password, teacher) VALUES (:username, :password, :teacher)")
        db.session.execute(sql, {"username": username, "password": hash_value, "teacher": is_teacher})
        db.session.commit()
        if is_teacher:
            sql = text("UPDATE users SET teacher = true WHERE username = :username")
            db.session.execute(sql, {"username": username})
            db.session.commit()

        login(username, password)
        return True

    except Exception as e:
        print(f"Error: {e}")
        db.session.rollback()
        return False

		
def get_classes():
    try:
        sql = text("SELECT id, name FROM classes")
        result = db.session.execute(sql)
        classes = result.fetchall()
        return classes
    except Exception as e:
        print(f"Error: {e}")
        return []


def get_class_info(class_id):
    sql = text("SELECT id FROM classes WHERE id = :class_id")
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
        except Exception as e:
            print(f"Error: {e}")
            db.session.rollback()
            return False
    else:
        return False


def delete_class(class_id):
    teacher = session.get("teacher", False)
    if teacher:
        try:
            sql = text("DELETE FROM messages WHERE class_id = :class_id")
            db.session.execute(sql, {"class_id": class_id})
            sql = text("DELETE FROM classes WHERE id = :class_id")
            db.session.execute(sql, {"class_id": class_id})
            db.session.commit()            
            return True
        except:
            db.session.rollback()
            return False
    else:
        return False
    
def send_message(user_id, class_id, content):
    sent_at = datetime.now()
    sql = text("INSERT INTO messages (user_id, class_id, content, sent_at) VALUES (:user_id, :class_id, :content, :sent_at) RETURNING id")
    result = db.session.execute(sql, {"user_id": user_id, "class_id": class_id, "content": content, "sent_at": sent_at})
    message_id = result.fetchone()[0]
    db.session.commit()
    return message_id

def get_messages(class_id):
    sql = text("SELECT m.id, m.user_id, m.content, u.username, m.sent_at FROM messages m JOIN users u ON m.user_id = u.id WHERE m.class_id = :class_id ORDER BY m.sent_at")
    result = db.session.execute(sql, {"class_id": class_id})
    messages = result.fetchall()
    return messages

def edit_message(message_id, edited):
    sql = text("UPDATE messages SET content = :edited WHERE id = :message_id")
    db.session.execute(sql, {"message_id": message_id, "edited": edited})
    db.session.commit()

def delete_message(message_id, user_id):
    sql = text("SELECT user_id FROM messages WHERE id = :message_id")
    result = db.session.execute(sql, {"message_id": message_id})
    message = result.fetchone()
    teacher = session.get("teacher", False)
    if teacher or message.user_id == user_id:
        try:
            sql = text("DELETE FROM messages WHERE id = :message_id")
            db.session.execute(sql, {"message_id": message_id})
            db.session.commit()
            return True
        except:
            db.session.rollback()
            return False
    else:
        return False
        
def get_total_classes():
    sql = text("SELECT COUNT(*) FROM classes")
    result = db.session.execute(sql)
    total_classes = result.fetchone()[0]
    return total_classes

def get_total_messages():
    sql = text("SELECT COUNT(*), MAX(sent_at) FROM messages")
    result = db.session.execute(sql)
    row = result.fetchone()
    total_messages = row[0]
    return total_messages
        
def like_message(user_id, message_id):
    sql = text("SELECT * FROM likes WHERE user_id = :user_id AND message_id = :message_id")
    like = db.session.execute(sql, {"user_id": user_id, "message_id": message_id}).first()
    if not like:
        sql = text("INSERT INTO likes (user_id, message_id) VALUES (:user_id, :message_id)")
        db.session.execute(sql, {"user_id": user_id, "message_id": message_id})
        db.session.commit()

def get_likes_count(message_id):
    sql = text("SELECT COUNT(*) FROM likes WHERE message_id = :message_id")
    result = db.session.execute(sql, {"message_id": message_id}).scalar()
    return result
    
def search(keyword):
    sql = text("SELECT m.id, m.content, m.sent_at, u.username FROM messages m JOIN users u ON m.user_id = u.id WHERE m.content LIKE :keyword")
    result = db.session.execute(sql, {"keyword": f"%{keyword}%"})
    search_results = result.fetchall()
    return search_results
        
def add_favorite(message_id, user_id, class_id):
    sql = text("INSERT INTO favorites (message_id, user_id, class_id) VALUES (:message_id, :user_id, :class_id)")
    db.session.execute(sql, {"message_id": message_id, "user_id": user_id, "class_id": class_id})
    db.session.commit()


def get_favorite_messages(user_id):
    sql = text("SELECT m.id, m.user_id, m.content, u.username, m.sent_at, c.id FROM messages m JOIN favorites f ON m.id = f.message_id JOIN users u ON m.user_id = u.id JOIN classes c ON m.class_id = c.id WHERE f.user_id = :user_id ORDER BY m.sent_at")
    result = db.session.execute(sql, {"user_id": user_id})
    favorite_messages = result.fetchall()
    return favorite_messages

def logout():
	del session["user_id"]

	
