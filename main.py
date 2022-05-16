# KABAJ via Flask
# Created by Ajax Guo 11/05
# Licensed by EspressoForDunfordWare
from flask import Flask, render_template
from time import sleep

app = Flask(__name__)

@app.route('/')
def home():
  return render_template("home.html")


@app.route('/signup')
def signup():
  return render_template("signup.html")

if __name__ == '__main__':
  app.run(debug= True, host='0.0.0.0', port=8080)
# do not execute this code if imported