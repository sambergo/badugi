def get_hand_value(hand):
    """
    Ac 2d 3h 4s
    [ {"suit": "spade", "number": 1 } ]
    """
    suits = []
    numbers = []
    for card in hand:
        has_suit = card["suit"] in suits
        has_number = card["number"] in numbers
        if not has_suit and not has_number:
            suits.append(card["suit"])
            numbers.insert(0, card["number"])
    print(len(suits), numbers)


if __name__ == "__main__":
    test_hand = [
        {"suit": "s", "number": 1},
        {"suit": "h", "number": 4},
        {"suit": "d", "number": 9},
        {"suit": "s", "number": 2},
    ]
    hand_rank = get_hand_value(test_hand)
