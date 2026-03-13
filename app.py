from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import os

app = Flask(__name__)
DB_FILE = "shop_todo.db"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS todos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            completed BOOLEAN NOT NULL CHECK (completed IN (0, 1))
        )
    ''')
    conn.commit()
    conn.close()

@app.route("/")
def index():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT id, title, completed FROM todos ORDER BY id DESC")
    todos = [{'id': row[0], 'title': row[1], 'completed': bool(row[2])} for row in c.fetchall()]
    conn.close()
    return render_template("index.html", todos=todos)

@app.route("/add", methods=["POST"])
def add():
    title = request.form.get("title")
    if title:
        conn = sqlite3.connect(DB_FILE)
        c = conn.cursor()
        c.execute("INSERT INTO todos (title, completed) VALUES (?, 0)", (title,))
        conn.commit()
        conn.close()
    return redirect(url_for("index"))

@app.route("/toggle/<int:todo_id>")
def toggle(todo_id):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT completed FROM todos WHERE id = ?", (todo_id,))
    row = c.fetchone()
    if row:
        new_status = 0 if row[0] else 1
        c.execute("UPDATE todos SET completed = ? WHERE id = ?", (new_status, todo_id))
        conn.commit()
    conn.close()
    return redirect(url_for("index"))

@app.route("/delete/<int:todo_id>")
def delete(todo_id):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("DELETE FROM todos WHERE id = ?", (todo_id,))
    conn.commit()
    conn.close()
    return redirect(url_for("index"))

if __name__ == "__main__":
    init_db()
    app.run(debug=True, port=8000)
