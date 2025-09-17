from flask import Flask, render_template, request
from werkzeug.security import generate_password_hash
import sqlite3, os

app = Flask(__name__)
DB_PATH = os.path.join(os.path.dirname(__file__), "users.db")

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS users (
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   username TEXT UNIQUE,
                   password TEXT
                 )""")
    conn.commit()
    conn.close()

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        username = request.form["username"].strip()
        password = request.form["password"]
        if not username or not password:
            return render_template("result.html", message="Please provide username and password")
        hashed = generate_password_hash(password, method="pbkdf2:sha256")
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        try:
            c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed))
            conn.commit()
            message = f"hai {username}, you registered"
        except sqlite3.IntegrityError:
            message = "username already exists"
        finally:
            conn.close()
        return render_template("result.html", message=message)
    return render_template("index.html")

if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=3000, debug=True)
