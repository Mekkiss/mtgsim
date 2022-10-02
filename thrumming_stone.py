from random import shuffle
from tabulate import tabulate
import matplotlib.pyplot as plt


SAMPLES = 10000

class outcome:
    LOTUS_CASTABLE = 1
    LOTUS_UNCASTABLE = -1
    TOO_MANY_MULLIGANS = -2


def build_deck(size=99, approach=27, stone=1):
    other = size - approach - stone
    deck = ['A'] * approach + ['S'] * stone + ['O'] * other
    return deck


def cascade(deck, stack, size=4):
    """ Run a single cascade"""
    triggers = 0
    # reveal the top four cards
    reveal = [deck.pop(), deck.pop(), deck.pop(), deck.pop()]
    # cast the revealed Approaches
    while 'A' in reveal:
        stack.append('A')
        reveal.remove('A')
        triggers += 1

    # Put the remainder on the bottom
    while len(reveal) > 0:
        deck.insert(0, reveal.pop())

    # Resolve the cascade triggers
    for i in range(triggers):
        stack = cascade(deck, stack, size=size)
    
    # Return the stack when done
    return stack


def run_sample(size, approach, stone):
    """
    Run a single simulation
    """
    deck = build_deck(size=size, approach=approach, stone=stone)
    deck.remove('S')  # Thrumming stone on battlefield
    deck.remove('A')  # Approach on stack
    shuffle(deck)
    stack = cascade(deck, ['A'])

    return len(stack)


def total_results(size, approach, stone):
    """
    Run a lot of simulations
    """
    results = []
    for i in range(SAMPLES):
        results.append(run_sample(size, approach, stone))
    return results

def plot_results(results):
    plt.hist(results)
    plt.xlabel("Final stack size")
    plt.ylabel("Sample count")
    plt.show()


if __name__ == '__main__':

    print("Deck: 97 cards, 27 approaches, 1 stone")
    plot_results(total_results(97, 27, 1))
