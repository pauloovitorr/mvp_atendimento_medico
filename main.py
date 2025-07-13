from flask import Flask, request
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

@app.route('/', methods = ['GET'])
def get_home():
    return 'Hello World'

if __name__ == '__main__':
    app.run(debug=True)
