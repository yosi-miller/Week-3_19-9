from models.mba_player_model import NBAPlayer


def get_players_from_db():

    return NBAPlayer.query.filter_by(position=)