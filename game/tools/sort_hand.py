def collisions_in_hand(hand, card):
    return len([c for c in hand if card.suit is c.suit or card.number is c.number])


def sort_badugi_hand(hand):
    new_hand = []
    old_hand = sorted(
        hand,
        key=lambda x: (x.number, collisions_in_hand(hand, x)),
    )
    new_hand.append(old_hand.pop(0))
    for _ in range(3):
        old_hand = sorted(
            old_hand,
            key=lambda x: (collisions_in_hand(new_hand, x), x.number),
        )
        new_hand.append(old_hand.pop(0))
    return new_hand
