import chess

def charger_partie(pgn_path):
    """Charge la partie PGN depuis un fichier."""
    try:
        with open(pgn_path) as pgn_file:
            game = chess.pgn.read_game(pgn_file)
        return game
    except Exception as e:
        print(f"Erreur lors du chargement du fichier PGN: {e}")
        return None