# This program runs a simulation of a home style game of Blackjack with 2 to 5 players.

# Standard premable
import random as rand
import numpy as np
import matplotlib.pyplot as plt

# Game setup
def generate_deck():
    """Generates a standard deck of cards and the associated value of each card. """
    suits = ['hearts', 'clubs', 'diamonds', 'spades']
    numbers = ['2','3','4','5','6','7','8','9','10','jack','queen','king','ace']
    deck = []
    for s in suits:
        for n in numbers:
            deck.append([n +' '+ s])
    values = [2,3,4,5,6,7,8,9,10,10,10,10,1]*4
    for i,item in enumerate(deck):
        item.append(values[i])
    return deck

def shuffle_deck(deck):
    """Shuffles a standard deck of cards using random.shuffle"""
    rand.shuffle(deck)
    return deck

def generate_hands(deck):
    """Takes two cards from the deck and gives it to the player's hand"""
    hand = []
    hand.append(deck[0])
    hand.append(deck[1])
    deck.remove(deck[0])
    deck.remove(deck[0])
    return hand, deck

def give_players(num_players, deck):
    """Gives each player a hand depending on the number of players in the game."""
    hands = []
    for n in range(num_players):
        hand, deck = generate_hands(deck)
        hands.append(hand)
    return hands, deck

# Turn process
def count(deck):
    """Returns a list of sorted values of the current deck"""
    values = []
    for i in deck:
        values.append(i[1]) #purposly skipping 11 for aces
    return sorted(values)

def hand_values(hand):
    """Returns all possible sums of cards in a hand and accounts for all combinations of Aces in hand"""
    s = [0]
    for i in hand:
        s[0] += i[1]
    aces_count = 0
    for i in hand:
        if i[1] == 1:
            aces_count += 1
    if aces_count >= 1:
        s.append(s[0]+10)
        if aces_count >= 2:
            s.append(s[0]+20)
            if aces_count >= 3:
                s.append(s[0]+30)
                if aces_count == 4:
                    s.append(s[0]+40)
    return s

def hit(hand, deck, unknown):
    """Performs a hit. (Adds card to hand, removes card from deck, remove unknown value of card)"""
    hand.append(deck[0])
    unknown.remove(deck[0][1])
    deck.remove(deck[0])
    return hand, deck, unknown

def give_unknowns(hands, deck):
    """Returns a list of cards that is hidden to the player."""
    unknowns = []
    for i in range(len(hands)):
        unknowns.append(count(deck))

    for num_players in range(len(hands)): #num_player refers to player we want
        for player,hand in enumerate(hands): #player refers to other player
            if num_players != player:
                unknowns[num_players].append(hand[0][1])
    return unknowns

def probability(sum_, unknown, prob):
    """Finds the probability of values summing below 21 out of the current unknown cards."""
    count = 0
    for value in unknown:
        if value + sum_ <= 21:
            count += 1
    if count/len(unknown) > prob:
        return True
    else:
        return False

def turn(player, hands, deck, unknowns, prob_array, prt = False):
    """Simulates a turn of a player during a round."""
    sums = hand_values(hands[player])
    while sums[0] < 21:
        if prt == True:
            print('Player', player,'turn:\n  Current sum:',sums[0], '\n  Current length of deck:', len(deck))
        for value in sums:
            if value == 21:
                return 'blackjack', deck, sums
        if probability(sums[0], unknowns[player], prob_array[player]) == False:
            return 'stand',deck, sums
        else:
            hands[player], deck, unknowns[player] = hit(hands[player], deck, unknowns[player])
            sums = hand_values(hands[player])
    else:
        return 'bust',deck, sums

# Results
def generate_round(deck, n_players, prob_array):
    """Simulates one round of a game, putting together the turns of the selected number of players."""
    hands, deck = give_players(n_players, deck)
    un = give_unknowns(hands, deck)
    outcomes = []
    all_sums = []
    for i in range(n_players):
        outcome, deck, sums = turn(i, hands, deck, un, prob_array)
        outcomes.append(outcome)
        all_sums.append(sums)
    blackjack = []
    stand_values = []
    for player, outcome in enumerate(outcomes):
        if outcome == 'blackjack':
            blackjack.append(player)
    if len(blackjack) == 0:
        high_value = 0
        for i,sums in enumerate(all_sums):
            if outcomes[i] == 'stand':
                for value in sums:
                    if value > high_value and value < 21:
                        high_value = value
        for i,sums in enumerate(all_sums):
            for value in sums:
                if value == high_value:
                    stand_values.append(i)
        return outcomes, deck, stand_values, high_value
    if len(blackjack) == 0 and len(stand_values) == 0:
        return outcomes, deck, [], 0
    return outcomes, deck, blackjack, 21

def round_results(outcome, winners, winning_value):
    """Returns the results of a round: which player won and what the value of their hand was."""
    str_winners = [str(i) for i in winners]

    for i in range(len(outcome)):
        print('Player', i, ":", outcome[i])
    if len(winners) == 1:
        print('Player', ', '.join(str_winners), 'wins with a hand value of', winning_value)
    elif len(winners) == 0:
        print('All players bust')
    else:
        print('Players',', '.join(str_winners), 'tie with a hand value of', winning_value)

def game(num_players, prob_array, num_rounds= 10, print_bool = True):
    """Simulates a game of blackjack, returning the winner of the game and how many
    points they had when they won. An option is included the turn off the results text."""
    deck = shuffle_deck(generate_deck())
    points = [0 for i in range(num_players)]
    count = 0
    while count < num_rounds:
        count += 1
        outcome, deck, winners, winning_value = generate_round(deck, num_players, prob_array)
        
        if print_bool == True:
            print('\nResults for round {}'.format(count))
            round_results(outcome, winners, winning_value)
        
        for i in winners:        
            if winning_value == 21:
                if len(winners) == 1:
                    points[winners[0]] += 2
                else:
                    points[i] += 2/len(winners)
            elif winning_value < 21:
                if len(winners) == 1:
                    points[winners[0]] += 1
                else:
                    points[i] += 1/len(winners)
        
        print_points = []
        for i in points:
            point = float('%.3f'%(i))
            print_points.append(point)
            
        if print_bool == True:
            print('Current points:', print_points)
            
        if len(deck) < 6*num_players:
            deck = shuffle_deck(generate_deck())
    
    game_winners = []
    high_points = max(points)
    for i, point in enumerate(points):
        if point == high_points:
            game_winners.append(str(i))
    
    print_highpoint = float('%0.3f'%high_points)
    
    if print_bool == True:
        print('The winner(s):',', '.join(game_winners),'with',print_highpoint,'points')
    
    return game_winners, np.array(points)

def main():
    rules_text = """
    This project is a python script that simulates a game of Blackjack between 2-5 players. In a standard game
    of Blackjack, each player starts with two cards. The player decides whether to draw another card (or hit)
    depending on whether the sum of the values of the hand adds up to 21 (or Blackjack). The goal is to have the
    hand sum up to as close to 21 as possible but without going 21 (which is a bust). The simulation shuffles
    a standard deck of cards and each player is controlled by the computer AI. The computer AI uses a card counting
    system that allows it to calculate the probability of reaching Blackjack each round and uses that probability to
    decide whether it's safe to take a hit or not. \n
    This simulation allows the user to analyze the outcomes of a game of Blackjack with a desired number of players.
    The user can see the printed results of one game of Blackjack or disable the printed text, allowing the user to
    analyze the results of multiple games without effecting efficiency. For each game, the user can change the number
    of players, number of rounds per game, and the risk factor of taking a hit. The risk factor is a value from 0-1,
    where it represents the minimum probability for the next hit taken to sum up to 21. Thus a lower risk factor
    indicates the riskier the play.

    """
    rules = input('This is a Blackjack simulator. If you wish to read the rules, enter "Y". \nIf not enter any other character:  ')
    if rules == 'Y':
        print(rules_text)

    n_players = input('Input the number of players (2-5): ')
    n_players = int(n_players)
    print('Now enter the risk factor for each player. (Value between 0 to 1) ')
    risks = []
    for n in range(n_players):
        risk = input('Risk factor for player {}: '.format(n))
        risk = float(risk)
        risks.append(risk)
    n_rounds = input('How many rounds in the game? ')
    print('\nThe simulation will now begin...')
    game(n_players, risks, int(n_rounds))

main()


