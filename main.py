from flask import Flask, request
from Routes.Atendimentos import atendimento
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

app.register_blueprint(atendimento)

if __name__ == '__main__':
    app.run(debug=True)
