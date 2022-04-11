# Badugi poker game with NEAT-Python and pygame.

Create badugi AI with [NEAT-Python](https://neat-python.readthedocs.io/en/latest/) and play against it.

[Badugi rules](https://en.wikipedia.org/wiki/Badugi)

## To play the game

```
pip install -r requirements.txt
./play.py
```

## To evolve AI from zero

```
rm swap.pickle bet.pickle
./train_ai.py
```

"Swapping cards" and "betting" -skills evolve separately. Initialize swapping cards capability without betting rounds first by running `init_ai`. Then AI can evolve further by running `train_bet` and `train_swap`. Choose these by commenting others out in `train_ai.py`. Re-create AI in this repo by running `init_ai`, `train_bet` and `train_swap` in that order (Will take a while).

[NEAT-Python](https://neat-python.readthedocs.io/en/latest/) creates population of 50 units who play against each other for 100 hands. The best ones are used to breed the next generation of 50 units and this goes on for 40 generations.

Variables to vary in `train_ai.py`:

```
MAX_HANDS = 100
MAX_GENERATIONS = 40
```

Variables to vary in `config-swap.txt` or `config-bet.txt`:

```
pop_size              = 50

# If modifying fitness functions (better-fitness branch)
num_hidden              = 0
num_inputs              = 6
num_outputs             = 3
```
