CREATE TABLE classes (id SERIAL PRIMARY KEY, name TEXT );
CREATE TABLE users (id SERIAL PRIMARY KEY, username TEXT, password TEXT, teacher BOOLEAN DEFAULT false, class_id INTEGER REFERENCES classes(id));
CREATE TABLE messages (id SERIAL PRIMARY KEY, content TEXT, user_id INTEGER, class_id INTEGER, sent_at TIMESTAMP, likes_count INTEGER DEFAULT 0);
CREATE TABLE likes (id SERIAL PRIMARY KEY, message_id INTEGER, user_id INTEGER, FOREIGN KEY (message_id) REFERENCES messages (id), FOREIGN KEY (user_id) REFERENCES users (id));
CREATE TABLE favorites (id SERIAL PRIMARY KEY, user_id INTEGER REFERENCES users(id), message_id INTEGER REFERENCES messages(id), marked_at TIMESTAMP, class_id INTEGER);

