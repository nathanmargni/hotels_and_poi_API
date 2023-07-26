from flask import Flask
from server.poi_routes import poi
from server.hotel_routes import hotel


class App:

    app = Flask(__name__)
    app.register_blueprint(hotel)
    app.register_blueprint(poi)

    @staticmethod
    @app.route('/')
    def index():
        return "Welcome to the Tourism homepage!"

if __name__ == '__main__':
    App().app.run(debug=True)