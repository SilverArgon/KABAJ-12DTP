# KABAJ via Flask
# Created by Ajax Guo 11/05
# Licensed by EspressoForDunfordWare
from flask import Flask, render_template, request, redirect, session, g
from time import sleep
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
from datetime import datetime


app = Flask(__name__)


# Random generated key to confirm indivdiual user session
# print(os.urandom(24).hex())
SECRET_KEY = "184989dcf7e442d9550c4c9e228f9a752cde4045d9ddb19d"
app.secret_key = SECRET_KEY

def get_db():
    # Stores DB connection to a variable. Prevents crashing and db locking.
    if "db" not in g:
        g.db = sqlite3.connect("kabaj.db")
    return g.db

# Closes database connection when website goes down
@app.teardown_appcontext
def teardown_db(_):
    get_db().close()


def is_logged_in():
    # Checks if user is logged in (aka session)
    return session.get("is_logged_in", False)
   

# Home page (wow)
@app.route("/")
def home():
    return render_template("home.html", logged_in=is_logged_in())

# Signup
@app.route("/signup", methods=["GET", "POST"])
def signup():
    # Requests database to modify to add the details of the newly made account.
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        hashpassword = generate_password_hash(password)
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('''SELECT username FROM User WHERE username = ?''',
                       (username,))
        user_id = cursor.fetchone()
        print(user_id)
        if user_id is not None:
            print("test")
            return render_template("signup.html",
                                   error="Pre-existing account has this username.")
                                
        cursor.execute('''INSERT INTO User
                        (username, password_hash, image_path, admin)
                        VALUES (?,?,'blankpfp.png',false)
                        ''', (username, hashpassword))
        conn.commit()
        session["is_logged_in"] = True
        return redirect("/success")
    return render_template("signup.html")

# Login page
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        conn = get_db()
        cursor = conn.cursor()
        # Check if the account exists first
        cursor.execute('''SELECT id FROM User WHERE username = ?''',
                       (username,))
        user_id = cursor.fetchone()
        if user_id is None:
            return render_template("login.html",
                                   error="Account not found.")
            # If account is not found then it stops rest of code to execute
        cursor.execute('''SELECT password_hash FROM User WHERE id = ?''',
                       (user_id[0],))
        passfetch = cursor.fetchone()[0]
        if not check_password_hash(passfetch, password):
            return render_template("login.html", error="Password Incorrect.")
        session["is_logged_in"] = True,
        return redirect("success")
    return render_template("login.html")
    # Fetches SQL to see if the password matches username.


@app.route("/logout")
def logout():
    # ends user session (wowee)
    session.pop("is_logged_in", False)
    return redirect("/")

# Redirect user here if they sign up/log in successfully. Access is allowed if you have a session.
@app.route("/success")
def success():
    if is_logged_in():
        return render_template("success.html")
    else:
        return render_template("home.html",
                               error="You're not in an account right now.")


# Viewing board ID and checking if user has a session
@app.route("/board/<int:board_id>", methods=["GET","POST"])
def board(board_id):
    if is_logged_in:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('''SELECT name FROM Board WHERE id = ?''', (board_id,))
        name = cursor.fetchone()

        return render_template("post.html", name=name[0], board_id=board_id)  
    else:
        return redirect("/login")


def posttime():
    posttime = datetime.today().strftime("%H%M%d%m%Y")
    return posttime

# When posting gets rerouted to new api
@app.route("/new_post/<int:board_id>", methods=["POST"])
def new_post(board_id):
        postname = request.form.get("postname")
        tag = request.form.get("tag")
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('''INSERT INTO THREAD
                        (title, board_id, pinned,category)
                        VALUES (?,?,false,?)
                        ''', (postname, board_id, tag,))
        conn.commit()
        posttext = request.form.get("posttext")
        user_id = session.get("user_id", None)
        cursor.execute('''INSERT INTO POST
                        (created_at, body, user_id, thread_id) VALUES (?,?,?,?)''', (posttime(), posttext, user_id, board_id))
        conn.commit()
        print ("Post made.")
        return redirect("/")

# This is just error 404
@app.errorhandler(404)
def page_not_found(error):
    return render_template("404.html")


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8080)
# do not execute this code if imported
