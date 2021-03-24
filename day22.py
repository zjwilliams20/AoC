#########################
# day 22
#########################

with open('input/day22', 'r') as file:
    raw = ''.join(file.readlines())
    decks = raw.strip().split('\n\n')
player1 = [int(d) for d in decks[0].split('\n')[1:]]
player2 = [int(d) for d in decks[1].split('\n')[1:]]


def score(deck):
    '''compute the winning player's score based on the 
       order of cards in their deck
       '''
    return sum(card * (i+1) for i, card in enumerate(reversed(deck)))
        
def game(player1, player2, recursiveCombat=False):
    '''play a game of War with two decks'''

    history = set()
    while player1 and player2:
        # make sure we don't play infinite Recursive War
        state = (tuple(player1), tuple(player2))
        if state in history and recursiveCombat:
            return player1, player2
        history.add(state)

        # draw the top two cards
        card1 = player1.pop(0)
        card2 = player2.pop(0)

        # determine if we can recurse
        if len(player1) >= card1 and len(player2) >= card2 and recursiveCombat:
            p1_sub, _ = game(player1[:card1], player2[:card2], True)
            winner = 1 if p1_sub else 2
        # otherwise, play a normal game
        else:
            winner = 1 if card1 > card2 else 2
        
        # adjust winner's deck
        if winner == 1:
            player1 += [card1, card2]
        else:
            player2 += [card2, card1]
    return player1, player2


# let's play a game
p1_normal, p2_normal = game(player1.copy(), player2.copy())
print(f"Part 1 winner: {max(score(p1_normal), score(p2_normal))}")

# let's play a better game, hehe
p1_recursive, p2_recursive = game(player1.copy(), player2.copy(), True)
print(f"Part 2 winner: {max(score(p1_recursive), score(p2_recursive))}")
