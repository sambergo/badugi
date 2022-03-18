import json

hand_ranks = json.loads(open("./hands.json").read())


def get_winners(players):
    """
    :input: List of players objects
    :return: Filtered list of winner(s)
    """
    winners = []
    best_rank = 0
    for player in players:
        rank = get_hand_rank(player.hand)
        if rank > best_rank:
            winners = [player]
            best_rank = rank
        elif rank == best_rank:
            winners.append(player)
    return winners


def get_hand_rank(hand):
    """
    :input example:
    hand = [
        {"suit": "d", "number": 2},
        {"suit": "h", "number": 7},
        {"suit": "c", "number": 12},
        {"suit": "c", "number": 13},
    ]
    :return: Rank integer, higher the better
    """
    badugi_hand = []
    for card in hand:
        has_suit = card["suit"] in [bhc["suit"] for bhc in badugi_hand]
        has_number = card["number"] in [bhc["number"] for bhc in badugi_hand]
        if not has_suit and not has_number:
            badugi_hand.append(card)
    k = "-".join(map(str, [x["number"] for x in badugi_hand]))
    # print(k)
    rank = hand_ranks[k]
    # print(rank)
    return rank


if __name__ == "__main__":
    hand = [
        {"suit": "d", "number": 2},
        {"suit": "h", "number": 7},
        {"suit": "c", "number": 12},
        {"suit": "c", "number": 13},
    ]
    get_hand_rank(hand)