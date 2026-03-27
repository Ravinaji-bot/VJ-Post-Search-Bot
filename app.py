# Updated app.py - 24/7 Online Logic
from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Bot is Running Live 🚀'

if __name__ == "__main__":
    app.run()
    
