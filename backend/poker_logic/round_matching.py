
from typing import Tuple

import random
from sortedcontainers import SortedSet
import copy


def fix_values(round_players: Tuple):
    public_address_dict = {}

    for player in round_players:
        if player[2] not in public_address_dict:
            public_address_dict[player[2]] = []
        public_address_dict[player[2]].append((player[0], player[1]))

    fixed_list = [(key, *random.sample(value, len(value))) 
                  for key, value in public_address_dict.items()]
    return fixed_list
    

def shuffle_matches(matches, num_actual_players):
    if len(matches) < 2:
        return

    shuffled = copy.deepcopy(matches)
    iternations = num_actual_players * 4

    for _ in range(iternations):
        game1, game2 = random.sample(shuffled, 2)
        unique_players = set([game1[0][0], game1[1][0], game2[0][0], game2[1][0]])

        if len(unique_players) != 4:
            continue
            
        game1[1], game2[1] = game2[1], game1[1]

    return shuffled
        


def get_rounnd_matching(round_players: Tuple):
    round_players = fix_values(round_players)
    num_actual_players = len(round_players)

    cur_players = SortedSet(round_players, key=lambda player: len(player))
    matches = []

    while len(cur_players):
        max_player = cur_players.pop()

        if not len(cur_players):
            num_nfts = len(max_player) - 1
            if num_nfts % 2:
                raise Exception
            
            matches.append(max_player[-1], max_player[-2])
            
            max_player = max_player[:-2]
            if len(max_player) > 1:
                cur_players.add(max_player)
            
        else:
            second_max_player = cur_players.pop()
            
            match_player_1 = [max_player[0], *max_player[-1]]
            match_player_2 = [second_max_player[0], *second_max_player[-1]]

            matches.append([match_player_1, match_player_2])

            max_player = max_player[:-1]
            second_max_player = second_max_player[:-1]

            if len(max_player) != 1:
                cur_players.add(max_player)
            if len(second_max_player) != 1:
                cur_players.add(second_max_player)

    matches = shuffle_matches(matches, num_actual_players)
    return matches
