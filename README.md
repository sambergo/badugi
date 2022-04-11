# Badugi

[Badugi rules](https://en.wikipedia.org/wiki/Badugi)

## To evolve AI:

```bash
rm *.pickle
./init_ai.py

```

Variables to vary in `init_ai.py`:

- `max_generations`
- `max_hands`

Variables to vary in `config-swap.txt` or `config-bet.txt`:

```text
pop_size              = 50

num_hidden              = 0
num_inputs              = 6
num_outputs             = 3
```
