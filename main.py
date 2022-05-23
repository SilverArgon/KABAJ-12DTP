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


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8080)
# do not execute this code if imported
