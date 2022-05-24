# KABAJ via Flask
# Created by Ajax Guo 11/05
# Licensed by EspressoForDunfordWare
from flask import Flask, render_template, request, redirect
from time import sleep
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3


app = Flask(__name__)


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/signup", methods=["GET", "POST"])
def signup():
    # Requests database to modify to add the details of the newly made account.
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        hashpassword = generate_password_hash(password)
        conn = sqlite3.connect("kabaj.db")
        cursor = conn.cursor()
        cursor.execute ('''INSERT INTO User
                        (username, password_hash, image_path)
                        VALUES (?,?,'blankpfp.png')
                        ''',(username, hashpassword))
        conn.commit()
        conn.close()                
        return redirect("/")
    return render_template("signup.html")

  

@app.route("/login", methods= ["GET","POST"])
def login():
  if request.method == "POST":
    username = request.form.get("username")
    password = request.form.get("password")
    conn = sqlite3.connect("kabaj.db")
    cursor = conn.cursor()
    # Line below is just to check if the account exists first 
    cursor.execute ('''SELECT id FROM User WHERE username = ?''', (username,))
    user_id = cursor.fetchone()
    if user_id is None:
      return render_template("login.html", error = "You do not exist. Stop pretending you do.")
      # That code above just makes it so that if account is not found then it stops rest of code to execute
    cursor.execute ('''SELECT password_hash FROM User WHERE id = ?''', (user_id[0],))
    passfetch =cursor.fetchone()[0]
    if not check_password_hash(passfetch, password):
      return render_template("login.html", error = "Password Incorrect.")
    conn.close()
    return redirect("/")
  return render_template("login.html")
  # Fetches SQL to see if the password matches username. 


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8080)
# do not execute this code if imported
