def collisions_in_hand(hand, card):
    # return len([c for c in hand if card.suit is c.suit or card.number is c.number])
    x = 0
    for c in hand:
        if c.suit == card.suit or c.number == card.number:
            x += 1
    return x


def sort_badugi_hand(hand):
    sorted_hand = []
    hand.sort(key=lambda x: (x.number, collisions_in_hand(hand, x) * -1))
    sorted_hand.append(hand.pop(0))
    for _ in range(3):
        hand.sort(key=lambda x: (collisions_in_hand(sorted_hand, x), x.number))
        sorted_hand.append(hand.pop(0))
    return sorted_hand
