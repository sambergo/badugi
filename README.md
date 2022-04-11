# Badugi

[Badugi rules](https://en.wikipedia.org/wiki/Badugi)

## To play the game

```
pip install -r requirements.txt
./play.py
```

## To evolve AI from zero:

```
rm swap.pickle bet.pickle
./train_ai.py
```

"Swapping cards" and "betting" -skills evolve separately. Swapping cards without betting at all first by running `init_ai`. Then AI can evolve further by running `train_bet` and `train_swap`.

[NEAT-Python](https://neat-python.readthedocs.io/en/latest/) creates population of 50 units who play against each other for 100 hands. The best ones are used to breed the next generation and this goes on for 40 generations.

Variables to vary in `train_ai.py`:

```
MAX_HANDS = 100
MAX_GENERATIONS = 40
```

Variables to vary in `config-swap.txt` or `config-bet.txt`:

```
pop_size              = 50

num_hidden              = 0
num_inputs              = 6
num_outputs             = 3
```
