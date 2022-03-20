from collections import defaultdict

card_order_dict = {"2":2, "3":3, "4":4, "5":5, "6":6, "7":7, "8":8, "9":9, "T":10,"J":11, "Q":12, "K":13, "A":14}
hand_dict = {10: "royal-flush", 9:"straight-flush", 8:"four-of-a-kind", 7:"full-house", 6:"flush", 5:"straight", 4:"three-of-a-kind", 3:"two-pairs", 2:"one-pair", 1:"highest-card"}

def check_flush(hand):
    suits = [h[1] for h in hand]
    return len(set(suits)) == 1

def check_royal_flush(hand):
    ranks = [h[0] for h in hand]
    return check_flush(hand) and (''.join(ranks) == "TJQKA" or ''.join(ranks) == "AKQJT")

def check_straight_flush(hand):
    return check_flush(hand) and check_straight(hand)

def check_four_of_a_kind(hand):
    ranks = [i[0] for i in hand]
    rank_counts = defaultdict(lambda:0)
    for v in ranks:
        rank_counts[v]+=1
    return sorted(rank_counts.values()) == [1,4]

def check_full_house(hand):
    ranks = [i[0] for i in hand]
    rank_counts = defaultdict(lambda:0)
    for v in ranks:
        rank_counts[v]+=1
    return sorted(rank_counts.values()) == [2,3]

def check_flush(hand):
    suits = [i[1] for i in hand]
    return len(set(suits)) == 1

def check_straight(hand):
    ranks = [i[0] for i in hand]
    rank_counts = defaultdict(lambda:0)
    for v in ranks:
        rank_counts[v] += 1
    rank_ranks = [card_order_dict[i] for i in ranks]
    rank_range = max(rank_ranks) - min(rank_ranks)
    if len(set(rank_counts.values())) == 1 and (rank_range==4):
        return True
    else:
        # check straight with low Ace
        return set(ranks) == set(["A", "2", "3", "4", "5"])

def check_three_of_a_kind(hand):
    ranks = [i[0] for i in hand]
    rank_counts = defaultdict(lambda:0)
    for v in ranks:
        rank_counts[v]+=1
    return set(rank_counts.values()) == set([3, 1])

def check_two_pairs(hand):
    ranks = [i[0] for i in hand]
    rank_counts = defaultdict(lambda:0)
    for v in ranks:
        rank_counts[v]+=1
    return sorted(rank_counts.values())==[1,2,2]

def check_one_pairs(hand):
    ranks = [i[0] for i in hand]
    rank_counts = defaultdict(lambda:0)
    for v in ranks:
        rank_counts[v]+=1
    return 2 in rank_counts.values()

def get_highest_card(hand: list):
    hand_order = list(map(lambda h: card_order_dict[h[0]], hand))
    highest_card_index = hand_order.index(max(hand_order))
    return hand[highest_card_index]



if __name__ == "__main__":
    hand = ["3S", "JC", "QD", "5D", "AH"]
    print(get_highest_card(hand))
    
    