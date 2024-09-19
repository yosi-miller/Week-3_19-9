from flask import Flask

from blueprint.players_routes import players_bp
from db import db
from NBA_api.api import fetch_players

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()
    fetch_players()

app.register_blueprint(players_bp)

if __name__ == '__main__':
    app.run(debug=True)
