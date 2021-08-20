# Minesweeper-AI

## Try it here:
https://colab.research.google.com/drive/1UCPLuQLGiCymiPw4awpYPpM7wnj_sTqt?usp=sharing

## Description
  Python program generates a randomized minesweeper board, and attempts to solve it with a nearly perfect AI. 

## ALGORITHM

    1.) search for simple solutions using only information from adjacent squares  (fastest/preferred)
    
    2.) if no more simple solutions can be currently found, create truth tables for unknown squares, attempting to prove some squares must be either safe or a mine.  (slower but safe)
    
    3.) if no information can be proven from step 2,  calculate the probability of each unknown square being a mine, explore safest choice. (safest guess)
    
    4.) if all unknown squares are equally likely to be a mine, choose randomly.  (last resort)
    
