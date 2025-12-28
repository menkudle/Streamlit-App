import sqlite3
import pandas as pd

DB_PATH = "data/todo.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS tasks (task TEXT, status TEXT)')
    conn.commit()
    conn.close()

def add_task(task):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('INSERT INTO tasks (task, status) VALUES (?, ?)', (task, 'Pending'))
    conn.commit()
    conn.close()

def get_tasks():
    conn = sqlite3.connect(DB_PATH)
    return pd.read_sql('SELECT rowid, * FROM tasks', conn)

def delete_task(rowid):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('DELETE FROM tasks WHERE rowid = ?', (rowid,))
    conn.commit()
    conn.close()