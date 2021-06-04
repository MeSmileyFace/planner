CREATE TABLE tasks (
id INTEGER PRIMARY KEY,
name TEXT NOT NULL,
description TEXT,
selected_date TEXT NOT NULL,
due_date TEXT NOT NULL,
finished INTEGER NOT NULL,
date_finished TEXT,
user_id INTEGER NOT NULL,
FOREIGN KEY(user_id) REFERENCES users(id)
);