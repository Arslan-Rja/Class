CREATE TABLE users (id SERIAL PRIMARY KEY, username TEXT, password TEXT);
CREATE TABLE classes (id SERIAL PRIMARY KEY, class_id INTEGER);
CREATE TABLE messages (id SERIAL PRIMARY KEY,content TEXT,user_id INTEGER, class_id INTEGER, sent_at TIMESTAMP);

