from flask import Flask
from api.main import blueprint as main_blueprint
from api.main import socketio

app = Flask(__name__)

app.register_blueprint(main_blueprint)

app.secret_key = "6BtdCaEka6xjV4DVNxZ3pZB8mXJ70sig"

# Vercel requires the app to be named 'app'
app.debug = False
socketio.init_app(app)

if __name__ == '__main__':
    if not app.debug:
        app.run(host='0.0.0.0', port=5000)
    else:
        socketio.run(app, port=5000)