from db import db

class Team(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True)
    teamName = db.Column(db.Integer, nullable=True)
    player1_id = db.Column(db.Integer, nullable=False)
    player2_id = db.Column(db.Integer, nullable=False)
    player3_id = db.Column(db.Integer, nullable=False)
    player4_id = db.Column(db.Integer, nullable=False)
    player5_id = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f'<Team {self.teamName}>'