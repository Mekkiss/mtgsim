from random import shuffle
from tabulate import tabulate

SAMPLES = 10000

class outcome:
    LOTUS_CASTABLE = 1
    LOTUS_UNCASTABLE = -1
    TOO_MANY_MULLIGANS = -2


def build_deck(land, ramp, other):
    deck = ['L'] * land + ['R'] * ramp + ['O'] * other
    return deck

def keep_opener(hand):
    """
    We keep the opening hand if it has:
    - >= 2 Land
    - total of (land + ramp) <= 4
    - total of (land + ramp) >= 3
    - A lotus.
    """
    if len([x for x in hand if x == 'L']) < 2:
        return False
    if len([x for x in hand if x in ['L', 'R']]) not in [3, 4]:
        return False
    return True

def lotus_castable(deck):
    """
    Returns true of we have at least 5 land/ramp after drawing 5 cards.
    """
    if len([x for x in deck[:11] if x in ['L', 'R']]) > 5:
        return True
    return False

def run_sample(lands, ramp, other):
    """
    Run a single simulation
    """
    deck = build_deck(lands, ramp, other)
    shuffle(deck)
    while not keep_opener(deck[:6]):
        shuffle(deck)
    if not keep_opener(deck[:6]):
        shuffle(deck)
        if not keep_opener(deck[:6]):
        # First mulligan is free
            return outcome.TOO_MANY_MULLIGANS
            
    if lotus_castable(deck):
        return outcome.LOTUS_CASTABLE
    return outcome.LOTUS_UNCASTABLE

def total_results(lands, ramp, other):
    """
    Run a lot of simulations
    """
    results = {outcome.TOO_MANY_MULLIGANS: 0, outcome.LOTUS_CASTABLE: 0, outcome.LOTUS_UNCASTABLE: 0}
    for i in range(SAMPLES):
        results[run_sample(lands, ramp, other)]+=1
    rtable = [[ "Mulligan below 7", "Lotus Uncastable", "Lotus Castable" ],
              [ results[outcome.TOO_MANY_MULLIGANS], results[outcome.LOTUS_UNCASTABLE], results[outcome.LOTUS_CASTABLE]]]
    print(tabulate(rtable, headers="firstrow"))

if __name__ == '__main__':
    print("Deck: 38 lands, 10 ramp, 50 other. Gilded Lotus in opening hand. 10000 samples")
    total_results(38, 2, 48)

        
