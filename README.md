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
./train_ai.py init / bet / swap
```

"Swapping cards" and "betting" -skills evolve separately. Initialize swapping cards capability without betting rounds first by running `./train_ai.py init`. Then AI can evolve further by running `bet` and `swap`. Re-create AI in this repo by running `./train_ai.py init bet swap` (Will take a while).

[NEAT-Python](https://neat-python.readthedocs.io/en/latest/) creates population of 50 units who play against each other for 100 hands. The best ones breed the next generation of 50 units and this goes on for 40 generations.

Variables to vary in `train_ai.py`:

```
MAX_HANDS = 100
MAX_GENERATIONS = 40
```

Variables to vary in `config-swap.txt` and `config-bet.txt`:

```
pop_size              = 50

# If modifying fitness functions (better-fitness branch)
num_hidden              = 0
num_inputs              = 5
num_outputs             = 3
```

## TODO

- For better performance:
  - `sort_badugi_hand` and `get_hand_rank` most time consuming functions.
  - `Card` and `Dealer` as classes make it slow?
  - Add multiprocessing
- For better fitness:
  - check `better-fitness` branch
