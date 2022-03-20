from collections import defaultdict
from functools import cmp_to_key
from itertools import combinations
import json

card_order_dict = {"2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9, "T": 10, "J": 11, "Q": 12, "K": 13, "A": 14}
hand_name_dict = {10: "royal-flush", 9: "straight-flush", 8: "four-of-a-kind", 7: "full-house", 6: "flush", 5: "straight", 4: "three-of-a-kind", 3: "two-pairs", 2: "one-pair", 1: "highest-card"}

def get_royal_flush(hand: list):
    ranks = [card[0] for card in hand]
    ranks = sorted(ranks, key=cmp_to_key(lambda rank1, rank2: card_order_dict[rank2] - card_order_dict[rank1]))
    if get_flush(hand) and ''.join(ranks) == "AKQJT":
        return [rank + hand[0][1] for rank in ranks]
    return None

def get_straight_flush(hand: list):
    if get_flush(hand) and get_straight(hand):
        return get_straight(hand)
    return None

def get_four_of_a_kind(hand: list):
    rank_counts = defaultdict(lambda:0)
    for card in hand:
        rank_counts[card[0]]+=1
    if sorted(rank_counts.values()) == [1,4]:
        for card in hand:
            if rank_counts[card[0]] == 4:
                return [card[0] + suit for suit in "cshd"]
    return None

def get_full_house(hand: list):
    hand = sorted(hand, key=cmp_to_key(lambda card1, card2: card_order_dict[card2[0]] - card_order_dict[card1[0]]))
    rank_counts = defaultdict(lambda:[])
    threes = ""
    for card in hand:
        rank_counts[card[0]].append(card)
        if len(rank_counts[card[0]]) == 3:
            threes = card[0]
            
    for rank in rank_counts.keys():
        if not len(rank_counts[rank]) in [2, 3]:
            return None
        
    if len(set([card[0] for card in hand])) == 2:
        full_house_hand = rank_counts[threes]
        for card in hand:
            if len(rank_counts[card[0]]) == 2:
                full_house_hand += rank_counts[card[0]]
                break
        return full_house_hand
    
    return None

def get_flush(hand: list):
    hand = sorted(hand, key=cmp_to_key(lambda card1, card2: card_order_dict[card1[0]] - card_order_dict[card2[0]]))
    suits = [card[1] for card in hand]
    if len(set(suits)) == 1:
        return hand[::-1]

def get_straight(hand: list):
    hand = sorted(hand, key=cmp_to_key(lambda card1, card2: card_order_dict[card1[0]] - card_order_dict[card2[0]]))

    differences = [card_order_dict[hand[i][0]] - card_order_dict[hand[i - 1][0]] for i in range(1, len(hand))]
    
    if len(set(differences)) == 1 and differences[0] == 1:
        return hand[::-1]
    else:
        if set([card[0] for card in hand]) == set(["A", "2", "3", "4", "5"]):
            hand.insert(0, hand[-1])
            hand.pop()
            return hand[::-1]
    return None

def get_three_of_a_kind(hand: list):
    rank_counts = defaultdict(lambda:0)
    for card in hand:
        rank_counts[card[0]]+=1
        
    if max(list((rank_counts.values()))) == 3:
        three_of_a_kind_hand = []
        for card in hand:
            if rank_counts[card[0]] == 3:
                three_of_a_kind_hand.append(card)
        return three_of_a_kind_hand

    return None

def get_two_pairs(hand: list):
    hand = sorted(hand, key=cmp_to_key(lambda card1, card2: card_order_dict[card2[0]] - card_order_dict[card1[0]]))

    rank_counts = defaultdict(lambda:0)
    for card in hand:
        rank_counts[card[0]] += 1
    
    if sorted(rank_counts.values()) == [1,2,2]:
        two_pairs_hand = []
        for card in hand:
            if rank_counts[card[0]] == 2:
                two_pairs_hand.append(card)
        return two_pairs_hand
    return None
    
def get_one_pair(hand: list):
    hand = sorted(hand, key=cmp_to_key(lambda card1, card2: card_order_dict[card2[0]] - card_order_dict[card1[0]]))

    rank_counts = defaultdict(lambda:0)
    for card in hand:
        rank_counts[card[0]] += 1
    
    if 2 in rank_counts.values():
        one_pair_hand = []
        for card in hand:
            if rank_counts[card[0]] == 2:
                one_pair_hand.append(card)
            if len(one_pair_hand) == 2:
                return one_pair_hand
    
    return None

def get_highest_card(hand: list):
    hand_order = list(map(lambda h: card_order_dict[h[0]], hand))
    highest_card_index = hand_order.index(max(hand_order))
    return [hand[highest_card_index]]

def get_hand_value(hand: list):
    if get_royal_flush(hand):
        return 10, get_royal_flush(hand)
    if get_straight_flush(hand):
        return 9, get_straight_flush(hand)
    if get_four_of_a_kind(hand):
        return 8, get_four_of_a_kind(hand)
    if get_full_house(hand):
        return 7, get_full_house(hand)
    if get_flush(hand):
        return 6, get_flush(hand)
    if get_straight(hand):
        return 5, get_straight(hand)
    if get_three_of_a_kind(hand):
        return 4, get_three_of_a_kind(hand)
    if get_two_pairs(hand):
        return 3, get_two_pairs(hand)
    if get_one_pair(hand):
        return 2, get_one_pair(hand)
    return 1, get_highest_card(hand)
    
def play_game(first_player_combo: str, second_player_combo: str, the_flops: str):
    """
    :param first_player_combo: str - the first player's combo (ex. "Ac3h")
    :param second_player_combo: str - the second player's combo (ex. "Ac3h")
    :param the_flops: str - the 5 cards drawn on the table (ex. "Ac,3h,Qc,5d,Th")
    :return: dict containing
    {
        winner: int (1 for first_player, 2 for second player, -1 for draw),
        best_hand_1: list,
        best_hand_1_name: str,
        best_hand_2: list,
        best_hand_2_name: str,
        bad_beat: bool (True if the loser has a hand better than),
        tie_with_hands: bool
    }
    """
    
    player1_cards = [first_player_combo[:2], first_player_combo[2:]]
    player2_cards = [second_player_combo[:2], second_player_combo[2:]]
    the_flops = the_flops.split(",")
    
    best_hand1, best_hand_value1, full_hand1 = [], 0, []
    best_hand2, best_hand_value2, full_hand2 = [], 0, []
    
    for table_cards in combinations(the_flops, 3):
        table_cards = list(table_cards)
        if best_hand_value1 < get_hand_value(table_cards + player1_cards)[0]:
            best_hand_value1, best_hand1 = get_hand_value(table_cards + player1_cards)
            full_hand1 = table_cards + player1_cards
            
        if best_hand_value2 < get_hand_value(table_cards + player2_cards)[0]:
            best_hand_value2, best_hand2 = get_hand_value(table_cards + player2_cards)
            full_hand2 = table_cards + player2_cards
    
    if best_hand_value1 > best_hand_value2:
        bad_beat_hand = ["Ac", "Ad", "Ah", "Kc", "Ks"]
        
        bad_beat = get_hand_value(bad_beat_hand)[0] <= best_hand_value2
        
        return_dict = {
            "winner": 1,
            "best_hand_1": best_hand1,
            "best_hand_1_name": hand_name_dict[best_hand_value1],
            "best_hand_2": best_hand2,
            "best_hand_2_name": hand_name_dict[best_hand_value2],
            "bad_beat": bad_beat,
            "tie_with_hands": False
        }
        
        return json.dumps(return_dict)
    
    elif best_hand_value2 > best_hand_value1:
        bad_beat_hand = ["Ac", "Ad", "Ah", "Kc", "Ks"]
        
        bad_beat = get_hand_value(bad_beat_hand)[0] <= best_hand_value1
        
        return_dict = {
            "winner": 2,
            "best_hand_1": best_hand1,
            "best_hand_1_name": hand_name_dict[best_hand_value1],
            "best_hand_2": best_hand2,
            "best_hand_2_name": hand_name_dict[best_hand_value2],
            "bad_beat": bad_beat,
            "tie_with_hands": False
        }
        
        return json.dumps(return_dict)
        
    else:
        
        return_dict = {
            "best_hand_1": best_hand1,
            "best_hand_1_name": hand_name_dict[best_hand_value1],
            "best_hand_2": best_hand2,
            "best_hand_2_name": hand_name_dict[best_hand_value2],
            "tie_with_hands": True
        }
        
        full_hand1 = sorted(full_hand1, key=cmp_to_key(lambda card1, card2: card_order_dict[card2[0]] - card_order_dict[card1[0]]))
        full_hand2 = sorted(full_hand2, key=cmp_to_key(lambda card1, card2: card_order_dict[card2[0]] - card_order_dict[card1[0]]))

        # full-house case
        if best_hand_value1 == 7:
            
            # check 3 cards first
            if card_order_dict[best_hand1[0][0]] > card_order_dict[best_hand2[0][0]]:
                return_dict["winner"] = 1
            elif card_order_dict[best_hand1[0][0]] < card_order_dict[best_hand2[0][0]]:
                return_dict["winner"] = 2
            else:
                
                # check the pair now
                rem_card1, rem_card2 = "", ""
                for card in full_hand1:
                    if card[0] != best_hand1[0][0]:
                        rem_card1 = card[0]
                
                for card in full_hand2:
                    if card[0] != best_hand2[0][0]:
                        rem_card2 = card[0]
                
                if card_order_dict[rem_card1] > card_order_dict[rem_card2]:
                    return_dict["winner"] = 1
                elif card_order_dict[rem_card1] < card_order_dict[rem_card2]:
                    return_dict["winner"] = 2
                else:
                    return_dict["winner"] = -1
                
                return json.dumps(return_dict)
        
        else:
            for i in range(len(full_hand1)):
                card1 = full_hand1[i][0]
                card2 = full_hand2[i][0]
                if card_order_dict[card1] > card_order_dict[card2]:
                    return_dict["winner"] = 1
                elif card_order_dict[card1] < card_order_dict[card2]:
                    return_dict["winner"] = 2
            
            if return_dict.get("winner", -2) == -2:
                return_dict["winner"] = -1

        bad_beat_hand = ["Ac", "Ad", "Ah", "Kc", "Ks"]
        
        if return_dict["winner"] == 1:
            bad_beat = get_hand_value(bad_beat_hand)[0] <= best_hand_value2
            return_dict["bad_beat"] = bad_beat
        elif return_dict["winner"] == 2:
            bad_beat = get_hand_value(bad_beat_hand)[0] <= best_hand_value1
            return_dict["bad_beat"] = bad_beat
        
        return json.dumps(return_dict)
                
    
    
    
    