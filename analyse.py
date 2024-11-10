import chess
import chess.pgn
import chess.engine
import matplotlib.pyplot as plt


def charger_partie(pgn_path):
    """Charge la partie PGN depuis un fichier."""
    try:
        with open(pgn_path) as pgn_file:
            game = chess.pgn.read_game(pgn_file)
        return game
    except Exception as e:
        print(f"Erreur lors du chargement du fichier PGN: {e}")
        return None

def victoir(board):
    result = board.result()
    if result == '1-0':
        print("\nLes Blancs ont gagné.")
    elif result == '0-1':
        print("\nLes Noirs ont gagné.")
    else:
        print("\nLa partie est nulle.")


def analyser_partie(pgn_path, eval_couleur="blancs"):
    """Analyse une partie PGN et affiche les coups avec l'échiquier à chaque tour,
    l'évolution de la précision et les gaffes."""

    # Vérifier que la couleur choisie est correcte
    if eval_couleur not in ["blancs", "noirs"]:
        print("La couleur d'évaluation doit être 'blancs' ou 'noirs'.")
        return

    # Charger la partie depuis le fichier PGN
    game = charger_partie(pgn_path)
    if not game:
        return

    # Initialiser le moteur Stockfish (chemin à ajuster)
    stockfish_path = "./stockfish/stockfish-ubuntu-x86-64-avx2"
    engine = chess.engine.SimpleEngine.popen_uci(stockfish_path)

    # Initialiser l'échiquier
    board = game.board()

    # Variables pour l'évolution de la précision
    precisions = []
    coups = []
    gaffes = []

    # Analyser la partie
    coup_num = 1
    last_eval = 0.0  # Dernière évaluation pour comparer
    for move in game.mainline_moves():
        print(f"Coup {coup_num}: {move}")
        board.push(move)

        # Analyser l'évaluation de la position par Stockfish
        result = engine.analyse(board, chess.engine.Limit(time=2.0))  # 2 secondes d'analyse

        # Si c'est au tour des noirs, inverser l'évaluation
        eval_score = result["score"].relative.score(mate_score=10000)
        if (coup_num % 2 == 0 and eval_couleur == "blancs") or (coup_num % 2 != 0 and eval_couleur == "noirs"):
            eval_score = -eval_score  # Inverser l'évaluation pour la couleur appropriée

        # Sauver l'évaluation pour l'évolution de la précision
        precisions.append(eval_score)
        coups.append(coup_num)

        # Vérifier s'il y a une gaffe (définir un seuil, par exemple 100 centipions)
        if abs(eval_score - last_eval) > 100:  # Différence significative
            gaffes.append((coup_num, move))

        last_eval = eval_score
        coup_num += 1

    # Afficher l'évolution de la précision (graphique)
    plt.figure(figsize=(10, 6))
    plt.plot(coups, precisions, marker='o', linestyle='-', color='b', label="Évaluation Stockfish")
    plt.axhline(0, color='r', linestyle='--', label="Évaluation neutre")
    plt.xlabel('Nombre de coups')
    plt.ylabel('Évaluation (centipions)')
    plt.title(f'Évolution de la précision dans la partie ({eval_couleur.capitalize()})')
    plt.legend()
    plt.grid(True)
    plt.show()

    # Afficher les gaffes
    print("\nGaffes détectées (gros changements d'évaluation) :")
    for coup_num, move in gaffes:
        print(f"Coup {coup_num}: {move}")

    victoir(board)

    # Fermer le moteur Stockfish
    engine.quit()


# Exemple d'utilisation
pgn_path = "partie.pgn"  # Remplace par le chemin de ton fichier PGN
eval_couleur = "noirs"  # Choisir 'blancs' ou 'noirs'
analyser_partie(pgn_path, eval_couleur)