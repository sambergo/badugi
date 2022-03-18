import json

hands = []
for card1 in range(1, 14):
    hands.append([card1])
    for card2 in range(max(card1 + 1, 2), 14):
        hands.append([card1, card2])
        for card3 in range(max(card1 + 1, card2 + 1, 3), 14):
            hands.append([card1, card2, card3])
            for card4 in range(max(card1 + 1, card2 + 1, card3 + 1, 3), 14):
                hands.append([card1, card2, card3, card4])

hands.sort(
    key=lambda x: (
        len(x),
        max(x) * -1,
        max(x[:3] if len(x) == 4 else x) * -1,
        max(x[:2] if len(x) >= 3 else x) * -1,
    ),
)

# print(hands)
print(len(hands))


handobj = {}
for i, hand in enumerate(hands):
    k = "-".join(map(str, hand))
    if k in handobj:
        print("ERROR", hand)
    else:
        handobj[k] = i + 1

print(handobj)


open("./tools/hands.json", "w").write(json.dumps(handobj))
