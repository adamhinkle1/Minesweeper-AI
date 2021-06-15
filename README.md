# Minesweeper-AI

  Python program generates randomized minesweeper board, and solves with near perfect AI.

ALGORITHM:
    1.) search for simple solutions using only adjacent squares  (fastest)
    2.) if: no more simple solutions found, create truth tables for unknown squares to check if any squares must be either safe or a mine.  (slower)
    3.) if: safe squares can be marked as either safe or a mine, calculate the probability of each unknown square being a mine, explore safest choice. (educated guess)
    4.) if: all unknown squares are equally likely to be a mine, choose randomly.  (random selection)
    
