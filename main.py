from flask import Flask
from Controllers.Whatsapp_ctrl import WhatsappCtrl

app = Flask(__name__)

app.add_url_rule('/', 'index', WhatsappCtrl.index, methods= ['POST'])


if __name__ == "__main__":
    app.run(debug=True)

