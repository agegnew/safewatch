import flask


class Server:
    def __init__(self):
        self.flask_app = flask.Flask(__name__)

    def start(self):
        self.flask_app.run(host='0.0.0.0', port=911)

    def send_request(self):