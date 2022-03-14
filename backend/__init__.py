import random

TOTAL_PLAYERS = 16384
RARE_TIERS = 129

normal_tiers = ['tier_1', 'tier_2', 'tier_3', 'tier_4', 'tier_5', 'tier_6', 'tier_7', 'tier_8', 'tier_9', 'tier_10']
tiers = ['all_pairs', 'all_the_aces', 'ace_king_off_suit', 'broadway', 'pair_22', 'pair_33', 'pair_44', 'pair_55', 'pair_66', 'pair_77', 'pair_88', 'pair_99', 'pair_TT', 'pair_JJ', 'pair_QQ', 'pair_KK', 'pair_AA', 'ace_king_suited', 'jack_ten_suited']

def get_tiers_distribution():
    tiers_distribution = ["all_pairs"] * 13 + ["all_the_aces"] * 25 + ["pair_22"] * 13 + ["pair_33"] * 12 + ["pair_44"] * 11 + ["pair_55"] * 10 + ["pair_66"] * 9 + ["pair_77"] * 8 + ["pair_88"] * 7 + ["pair_99"] * 6 + ["pair_TT"] * 5 + ["pair_JJ"] * 4 + ["pair_QQ"] * 3 + ["pair_KK"] * 2 + ["pair_AA"] * 1

    for tier in normal_tiers:
        tiers_distribution += [tier] * ((TOTAL_PLAYERS - RARE_TIERS) // 10)

    while len(tiers_distribution) < TOTAL_PLAYERS:
        tiers_distribution.append(random.choice(normal_tiers))
    return tiers_distribution


if __name__ == "__main__":
    print(len(get_tiers_distribution()))
