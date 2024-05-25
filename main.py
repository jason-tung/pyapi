from flask import Flask, request
import os
from dotenv import load_dotenv, dotenv_values 

load_dotenv() 

app = Flask(__name__)

@app.route("/")
def hello_world():
    if request.args.get("key") == os.getenv("key"):
      return "hi"
    return "uh oh"

if __name__ == '__main__': 
  app.run(debug=True, port=5000)