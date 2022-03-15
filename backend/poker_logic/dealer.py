from poker.hand import Range, Combo
from poker import Suit, Rank
from functools import reduce
from typing import Union
import json

tier_to_combos = {}

def map_suit_to_str(suit: Suit):
    if suit == Suit.CLUBS:
        return 'c'
    if suit == Suit.DIAMONDS:
        return 'd'
    if suit == Suit.HEARTS:
        return 'h'
    return 's'

def map_rank_to_str(rank: Rank):
    if rank == Rank.ACE:
        return 'A'
    if rank == Rank.KING:
        return 'K'
    if rank == Rank.QUEEN:
        return 'Q'
    if rank == Rank.JACK:
        return 'J'
    if rank == Rank.TEN:
        return 'T'
    if rank == Rank.NINE:
        return '9'
    if rank == Rank.EIGHT:
        return '8'
    if rank == Rank.SEVEN:
        return '7'
    if rank == Rank.SIX:
        return '6'
    if rank == Rank.FIVE:
        return '5'
    if rank == Rank.FOUR:
        return '4'
    if rank == Rank.THREE:
        return '3'
    if rank == Rank.DEUCE:
        return '2'

def get_str_from_combo(combo: Combo):
    return map_rank_to_str(combo.first.rank) + map_suit_to_str(combo.first.suit) + map_rank_to_str(combo.second.rank) + map_suit_to_str(combo.second.suit)

def init_combos():
    global tier_to_combos
    
    ranges = {
        "tier_1": "22+, A2s+, K2s+, Q2s+, J2s+, T2s+, 92s+, 82s+, 72s+, 62s+, 52s+, 42s+, 32s, A2o+, K2o+, Q2o+, J2o+, T2o+, 92o+, 82o+, 72o+, 62o+, 52o+, 42o+, 32o".split(","),
        "tier_2": "22+, A2s+, K2s+, Q2s+, J2s+, T2s+, 92s+, 82s+, 72s+, 62s+, 52s+, 42s+, A2o+, K2o+, Q2o+, J4o+, T6o+, 96o+, 86o+, 76o".split(","),
        "tier_3": "22+, A2s+, K2s+, Q2s+, J2s+, T5s+, 96s+, 86s+, 75s+, A2o+, K5o+, Q7o+, J8o+, T8o+".split(","),
        "tier_4": "55+, AKs, A8s-AJs, A6s, A2s-A4s, K4s+, K2s, Q8s+, J8s+, J2s, T9s, 82s, A8o+, K9o+, QTo+, JTo".split(","),
        "tier_5": "55+, A3s+, K7s+, Q8s+, J9s+, T9s, A9o+, KTo+, QJo".split(","),
        "tier_6": "66+, A5s+, K9s+, Q9s+, JTs, ATo+, KJo+".split(","),
        "tier_7": "77+, A9s+, KTs+, QJs, AJo+, KQo".split(","),
        "tier_8": "88+, ATs+, KTs+, QJs, AQo+".split(","),
        "tier_9": "99+, AJs+, KQs, AKo".split(","),
        "tier_10": "TT+".split(","),
        "all_pairs": "22+".split(","),
        "all_the_aces": "AA, A2s+, A2o+".split(","),
        "ace_king_off_suit": "AKs, AKo".split(","),
        "broadway": "TT+, ATs+, KTs+, QTs+, JTs, ATo+, KTo+, QTo+, JTo".split(","),
        "pair_22": "22".split(","),
        "pair_33": "33".split(","),
        "pair_44": "44".split(","),
        "pair_55": "55".split(","),
        "pair_66": "66".split(","),
        "pair_77": "77".split(","),
        "pair_88": "88".split(","),
        "pair_99": "99".split(","),
        "pair_TT": "TT".split(","),
        "pair_JJ": "JJ".split(","),
        "pair_QQ": "QQ".split(","),
        "pair_KK": "KK".split(","),
        "pair_AA": "AA".split(","),
        "ace_king_suited": "AKs".split(","),
        "jack_ten_suited": "JTs".split(",")
    }
    
    for key in ranges.keys():
        lst = [Range(range.strip()) for range in ranges[key]]
        temp = reduce(lambda x,y :x+y, [range.combos for range in lst])
        tier_to_combos[key] = [get_str_from_combo(combo) for combo in temp]

def write_to_file():
    init_combos()
    with open('tiers_hands.json', "w") as file:
        json.dump(tier_to_combos, file, indent=4, sort_keys=True)
    
def draw_combo(tier: str, opp_hand: Union[str, None]) -> str:
    """
    draw a combo for a player given his opponent hand and his tier
    :return: string denoting a combo for the given tier (e.x. "Ah5c")
    """
    
    import random
    with open('tiers_hands.json') as json_file:
        tier_to_combos = json.load(json_file)
    
    combo = random.choice(tier_to_combos[tier])

    if opp_hand == None:
        return combo

    while True:
        if combo[:2] in opp_hand or combo[2:] in opp_hand:
            combo = random.choice(tier_to_combos[tier])
        else:
            break
    
    return combo

if __name__ == "__main__":
    pass