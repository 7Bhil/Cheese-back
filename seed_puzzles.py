import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from api.models import Puzzle

# Sample Puzzles (FEN positions)
puzzles = [
    {
        'fen': 'r1bqkbnr/pppp1ppp/2n5/4p3/2B1P3/5Q2/PPPP1PPP/RNB1K1NR w KQkq - 0 1', # Scholar's Mate
        'solution': 'f3f7',
        'difficulty': 'easy',
        'description': 'Le fameux Coup du Berger. Trouvez le mat en un coup !',
        'elo_rating': 800
    },
    {
        'fen': '6k1/5ppp/8/8/8/8/5PPP/6K1 w - - 0 1', # Example back rank
        'solution': 'a1a8',
        'difficulty': 'easy',
        'description': 'Couloir du fond. Mat en un !',
        'elo_rating': 900
    },
    {
        'fen': 'rnbqkbnr/ppppp2p/8/5ppQ/4P3/8/PPPP1PPP/RNB1KBNR b KQkq - 0 1', # Fool's Mate
        'solution': 'g5h5',
        'difficulty': 'easy',
        'description': 'Mat de l\'imbécile dévié. Trouvez le coup fatal.',
        'elo_rating': 700
    }
]

for p in puzzles:
    Puzzle.objects.get_or_create(**p)

print("Puzzles insérés avec succès !")
