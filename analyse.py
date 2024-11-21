import source
import chess
import chess.pgn
import chess.engine
import matplotlib.pyplot as plt


def analyser_partie(pgn_path):
    """
    Analyse une partie PGN et affiche l'évolution de la précision
    et une courbe montrant qui menait dans la partie.

    :param pgn_path: Chemin vers le fichier PGN à analyser
    """
    # Charger la partie depuis le fichier PGN
    mate = 1000

    game = source.charger_partie(pgn_path)
    if not game:
        return

    # Initialiser le moteur Stockfish (chemin à ajuster)
    stockfish_path = "../stockfish/stockfish-ubuntu-x86-64-avx2"
    engine = chess.engine.SimpleEngine.popen_uci(stockfish_path)

    # Initialiser l'échiquier
    board = game.board()

    # Variables pour stocker les données
    evaluations = []
    coups = []
    avantage_blancs = []  # 1 pour Blancs, -1 pour Noirs, 0 pour neutre

    # Analyser la partie
    coup_num = 1
    for move in game.mainline_moves():
        board.push(move)

        # Évaluation de la position par Stockfish
        result = engine.analyse(board, chess.engine.Limit(time=0.1))
        eval_score = result["score"].relative

        if eval_score.is_mate():
            # Gérer les situations de mat
            mate_in = eval_score.mate()
            eval_score = mate if mate_in > 0 else -mate  # Mat pour Blancs ou Noirs
        else:
            eval_score = eval_score.score(mate_score=mate)

        # Stocker l'évaluation en centipions
        evaluations.append(eval_score)
        coups.append(coup_num)

        # Déterminer qui mène
        if eval_score > 75:  # Avantage Blancs
            avantage_blancs.append(1)
        elif eval_score < -75:  # Avantage Noirs
            avantage_blancs.append(-1)
        else:  # Neutre
            avantage_blancs.append(0)

        # Inverser le score des Noirs pour afficher l'opposé de leur évaluation
        if len(coups) % 2 == 1:  # Si c'est le tour des Noirs
            evaluations[-1] = -evaluations[-1]

        coup_num += 1
    print(evaluations)
    # Afficher l'évolution des évaluations
    plt.figure(figsize=(12, 6))
    plt.subplot(2, 1, 1)
    plt.plot(coups, evaluations, marker='o', linestyle='-', color='b', label="Évaluation Stockfish")
    plt.axhline(0, color='r', linestyle='--', label="Évaluation neutre")
    plt.xlabel("Nombre de coups")
    plt.ylabel("Évaluation (centipions)")
    plt.title("Évolution de l'évaluation par Stockfish")
    plt.legend()
    plt.grid(True)

    # Afficher qui menait dans la partie
    plt.subplot(2, 1, 2)
    plt.step(coups, avantage_blancs, where='mid', color='g', label="Avantage : Blancs (1) / Noirs (-1)")
    plt.axhline(0, color='r', linestyle='--', label="Neutre")
    plt.xlabel("Nombre de coups")
    plt.ylabel("Avantage")
    plt.title("Évolution de l'avantage dans la partie")
    plt.yticks([-1, 0, 1], ["Noirs", "Neutre", "Blancs"])
    plt.legend()
    plt.grid(True)

    plt.tight_layout()
    plt.show()

    # Fermer le moteur Stockfish
    engine.quit()
