from flask import Flask, render_template, request, redirect
import psycopg2
import os

app = Flask(__name__)

# Database URL
DATABASE_URL = "postgresql://postgres:xgZMYbLgKSFiWbyqRZLukdHEDmCtInnB@trolley.proxy.rlwy.net:29389/railway"

# Simple password for posting
ADMIN_PASSWORD = "vetsecret"  # 🔹 Change this to your secret password

def get_connection():
    return psycopg2.connect(DATABASE_URL)

@app.route("/")
def index():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS posts (id SERIAL PRIMARY KEY, title TEXT, content TEXT);")
    cur.execute("SELECT title, content FROM posts ORDER BY id DESC;")
    posts = [{"title": t, "content": c} for (t, c) in cur.fetchall()]
    conn.commit()
    cur.close()
    conn.close()
    return render_template("index.html", posts=posts)

@app.route("/create_post", methods=["POST"])
def create_post():
    title = request.form.get("title")
    content = request.form.get("content")
    password = request.form.get("password")

    if password != ADMIN_PASSWORD:
        return "Mot de passe incorrect ❌", 403

    conn = get_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO posts (title, content) VALUES (%s, %s)", (title, content))
    conn.commit()
    cur.close()
    conn.close()

    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
