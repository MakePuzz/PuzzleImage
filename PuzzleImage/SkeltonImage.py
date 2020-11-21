import matplotlib.pyplot as plt

from puzzleimage import PuzzleImage

class SkeltonImage(PuzzleImage):
    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
    
    def get_board(self, ax, cell):
        return ax

    def get_wordlist(self, ax, wordlist):
        return ax