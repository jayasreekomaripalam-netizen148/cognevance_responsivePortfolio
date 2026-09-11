from flask import Flask, render_template, request, jsonify, session, redirect
import sqlite3
from datetime import datetime
import os

app = Flask(__name__)

app.secret_key = os.environ.get(
    "SECRET_KEY",
    "portfolio-development-secret-key"
)

DATABASE = "portfolio.db"

ADMIN_PASSWORD = os.environ.get(
    "ADMIN_PASSWORD",
    "admin123"
)


# ================= DATABASE =================

def get_db_connection():
    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row
    return connection


def init_database():

    connection = get_db_connection()

    connection.execute("""
        CREATE TABLE IF NOT EXISTS contact_messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            message TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
    """)

    connection.commit()
    connection.close()


# ================= HOME =================

@app.route("/")
def home():
    return render_template("index.html")


# ================= CONTACT API =================

@app.route("/api/contact", methods=["POST"])
def contact():

    data = request.get_json()

    if not data:
        return jsonify({
            "success": False,
            "message": "Invalid request."
        }), 400

    name = data.get("name", "").strip()
    email = data.get("email", "").strip()
    message = data.get("message", "").strip()

    # Name validation
    if not name:
        return jsonify({
            "success": False,
            "message": "Name is required."
        }), 400

    if len(name) < 2:
        return jsonify({
            "success": False,
            "message": "Name must contain at least 2 characters."
        }), 400

    # Email validation
    if not email or "@" not in email or "." not in email:
        return jsonify({
            "success": False,
            "message": "Please provide a valid email address."
        }), 400

    # Message validation
    if not message:
        return jsonify({
            "success": False,
            "message": "Message is required."
        }), 400

    if len(message) < 10:
        return jsonify({
            "success": False,
            "message": "Message must contain at least 10 characters."
        }), 400

    # Store message
    connection = get_db_connection()

    connection.execute(
        """
        INSERT INTO contact_messages
        (name, email, message, created_at)
        VALUES (?, ?, ?, ?)
        """,
        (
            name,
            email,
            message,
            datetime.now().isoformat()
        )
    )

    connection.commit()
    connection.close()

    return jsonify({
        "success": True,
        "message": "Your message has been sent successfully!"
    })


# ================= ADMIN LOGIN =================

@app.route("/admin", methods=["GET", "POST"])
def admin():

    if request.method == "POST":

        password = request.form.get("password", "")

        if password == ADMIN_PASSWORD:

            session["admin_logged_in"] = True

            return redirect("/admin")

        return render_template(
            "admin.html",
            logged_in=False,
            error="Invalid admin password."
        )

    if not session.get("admin_logged_in"):

        return render_template(
            "admin.html",
            logged_in=False,
            error=None
        )

    connection = get_db_connection()

    messages = connection.execute(
        """
        SELECT id, name, email, message, created_at
        FROM contact_messages
        ORDER BY id DESC
        """
    ).fetchall()

    connection.close()

    return render_template(
        "admin.html",
        logged_in=True,
        messages=messages,
        error=None
    )


# ================= DELETE MESSAGE =================

@app.route("/admin/delete/<int:message_id>", methods=["POST"])
def delete_message(message_id):

    if not session.get("admin_logged_in"):
        return redirect("/admin")

    connection = get_db_connection()

    connection.execute(
        "DELETE FROM contact_messages WHERE id = ?",
        (message_id,)
    )

    connection.commit()
    connection.close()

    return redirect("/admin")


# ================= LOGOUT =================

@app.route("/admin/logout")
def admin_logout():

    session.pop("admin_logged_in", None)

    return redirect("/admin")


# ================= API MESSAGES =================

@app.route("/api/messages", methods=["GET"])
def messages():

    if not session.get("admin_logged_in"):
        return jsonify({
            "success": False,
            "message": "Unauthorized. Please login as admin."
        }), 401

    connection = get_db_connection()

    rows = connection.execute(
        """
        SELECT id, name, email, message, created_at
        FROM contact_messages
        ORDER BY id DESC
        """
    ).fetchall()

    connection.close()

    return jsonify([
        dict(row)
        for row in rows
    ])


# ================= DATABASE INITIALIZATION =================

init_database()


# ================= START SERVER =================

if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )
