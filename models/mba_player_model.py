from db import db

class NBAPlayer(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True)
    playerName = db.Column(db.String(50), nullable=True)
    position = db.Column(db.String(2), nullable=True)
    games = db.Column(db.Integer, nullable=True)
    gamesStarted = db.Column(db.Integer, nullable=True)
    minutesPg = db.Column(db.Float, nullable=True)
    fieldGoals = db.Column(db.Integer, nullable=True)
    fieldAttempts = db.Column(db.Integer, nullable=True)
    fieldPercent = db.Column(db.Float, nullable=True)
    threeFg = db.Column(db.Integer, nullable=True)
    threeAttempts = db.Column(db.Integer, nullable=True)
    threePercent = db.Column(db.Float, nullable=True)
    twoFg = db.Column(db.Integer, nullable=True)
    twoAttempts = db.Column(db.Integer, nullable=True)
    twoPercent = db.Column(db.Float, nullable=True)
    effectFgPercent = db.Column(db.Float, nullable=True)
    ft = db.Column(db.Integer, nullable=True)
    ftAttempts = db.Column(db.Integer, nullable=True)
    ftPercent = db.Column(db.Float, nullable=True)
    offensiveRb = db.Column(db.Integer, nullable=True)
    defensiveRb = db.Column(db.Integer, nullable=True)
    totalRb = db.Column(db.Integer, nullable=True)
    assists = db.Column(db.Integer, nullable=True)
    steals = db.Column(db.Integer, nullable=True)
    blocks = db.Column(db.Integer, nullable=True)
    turnovers = db.Column(db.Integer, nullable=True)
    personalFouls = db.Column(db.Integer, nullable=True)
    points = db.Column(db.Integer, nullable=True)
    team = db.Column(db.String(3), nullable=False)
    season = db.Column(db.Integer, nullable=False)
    playerId = db.Column(db.String(10), nullable=False)

    def __repr__(self):
        return f'<NBAPlayer {self.playerName}>'
