# Blackjack_simulation
Blackjack simulation using python 3

This project is a python script that simulates a game of Blackjack between 2-5 players. In a standard game of Blackjack, 
each player starts with two cards. The player decides whether to draw another card (or \emph{hit}) depending on whether 
the sum of the values of the hand adds up to 21 (or \emph{Blackjack}). The goal is to have the hand sum up to as close to 
21 as possible but without going 21 (which is a \emph{bust}). The simulation shuffles a standard deck of cards and each 
player is controlled by the computer AI. The computer AI uses a card counting system that allows it to calculate the 
probability of reaching Blackjack each round and uses that probability to decide whether it's safe to take a hit or not. 

This simulation allows the user to analyze the outcomes of a game of Blackjack with a desired number of players. The user 
can see the printed results of one game of Blackjack or disable the printed text, allowing the user to analyze the results 
of multiple games without effecting efficiency. For each game, the user can change the number of players, number of rounds 
per game, and the risk factor of taking a hit. The risk factor is a value from 0-1, where it represents the minimum 
probability for the next hit taken to sum up to 21. Thus a lower risk factor indicates the riskier the play.

By implementing card counting into the game, we can analyze the benefits of making risky plays. The simulations showed that
being the last player of the game has a slight advantage compared to being the first player. Making riskier plays over the 
other players also shows a slight advantage. However, further analysis is necessary to make concrete conclusions. 
