from random import shuffle
from statistics import median


def create_deck():
    suits = ['H', 'D', 'S', 'C']
    card_numbers = ['2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14']
    deck = []

    for suit in suits:
        for num in card_numbers:
            # deck.append([suit, num])
            deck.append(num)

    shuffle(deck)
    p1 = deck[:26]
    p2 = deck[26:]
    return game_play(p1, p2)


def game_play(p1_deck, p2_deck):

    count = 0
    board_cards = []
    while p1_deck and p2_deck:

        print(f'round: {count}')
        print(len(p1_deck))
        print(len(p2_deck))
        if count > 5000:
            return 'draw', count
        count += 1
        if int(p1_deck[0]) > int(p2_deck[0]):
            if board_cards:
                p1_deck.extend(board_cards)
                board_cards = []
            p1_popped_card = p1_deck.pop(0)
            p2_popped_card = p2_deck.pop(0)
            p1_deck.extend([p1_popped_card, p2_popped_card])

        elif int(p2_deck[0]) > int(p1_deck[0]):
            if board_cards:
                p2_deck.extend(board_cards)
                board_cards = []
            p1_popped_card = p1_deck.pop(0)
            p2_popped_card = p2_deck.pop(0)
            p2_deck.extend([p1_popped_card, p2_popped_card])

        else:
            for _ in range(4):
                try:
                    board_cards.extend([p1_deck.pop(0), p2_deck.pop(0)])
                except IndexError:
                    if len(p1_deck) > len(p2_deck):
                        return 'p1', count
                    else:
                        return 'p2', count

    if p1_deck:
        return 'p1', count
    else:
        return 'p2', count


# result = create_deck()
# print(result)

p1 = 0
p2 = 0
draw = 0
n = 100
tot_rounds = []

for _ in range(n):
    result, rounds = create_deck()

    if result == 'p2':
        p1 += 1
        tot_rounds.append(rounds)
    elif result == 'p1':
        p2 += 1
        tot_rounds.append(rounds)
    else:
        draw += 1

print(f'simulation ran {n} times')
print(f'Player 1 won {p1} times')
print(f'Game was draw {draw} times')
print(f'Player 2 won {p2} times')
print(f'average number of rounds per game without draws was {sum(tot_rounds) / (p1 + p2)}')
print(f'median number of rounds per game without draws was {median(tot_rounds)}')
print(f'longest game took {max(tot_rounds)} rounds')
print(f'shortest game took {min(tot_rounds)} rounds')

