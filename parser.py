import re


def lire_fichier(path):
    """
    fonction qui lit les donnée récupéré sur le fichier temp
    :param path:
    :return:
    """

    # Lire le fichier temporaire
    with open(path, 'r', encoding='utf-8') as f:
        data = f.read()

    # Remplacer les occurrences de la séquence '\n' (chaîne) par un vrai retour à la ligne
    data = data.replace(r'\n', '\n')
    return data


def ecrirefichier(numero, game_parser):
    """

    :param numero:
    :param game_parser:
    :return:
    """
    fichier = "game" + str(numero) + "pgn"
    # Écrire caractère par caractère dans 'partie3.pgn'
    with open(fichier, 'w', encoding='utf-8') as f:
        for c in game_parser:
            f.write(c)  # Écrire chaque caractère


def parser_chess(pgn_brut):
    """
    fonction qui traite le pgn récupérer sur chess.com et le rend lisible pour l'utilisateur et reformater pour stockfish
    :param pgn_brut:
    :return:
    """
    # Remplacer les occurrences de la séquence '\n' (chaîne) par un vrai retour à la ligne
    pgn_brut = pgn_brut.replace(r'\n', '\n')

    # on  sépare les coups des donées
    meta, coups = pgn_brut.split("\n\n", 1)

    # traitement des données
    meta = meta.replace('\\', '')

    # traitement des coups
    coups = re.sub(r"\{(.*?)\}", '', coups)
    coups = re.sub(r"\d\.\.\.\ ", '', coups)
    coups = coups.replace("  ", " ")

    coups_mis_en_forme = re.sub(r"(\d+\.)", r"\n\1", coups)

    # Reconstruire le fichier PGN avec les coups mis en forme
    pgn_mis_en_forme = f"{meta}\n\n{coups_mis_en_forme}"
    return pgn_mis_en_forme


pgn_brute = lire_fichier('partie/temp.txt')

pgn_mis_en_forme = parser_chess(pgn_brute)
numero = 3
ecrirefichier(numero, pgn_mis_en_forme)

print("fichier écrit dans partie/game" + str(numero) + ".pgn")
