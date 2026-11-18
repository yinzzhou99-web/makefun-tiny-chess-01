# Tiny Chess — a strong chess engine in 4 KB of Python

[![make.fun · tiny-chess-01](https://make.fun/badge/tiny-chess-01.svg)](https://make.fun/bounty/tiny-chess-01?utm_source=github&utm_medium=readme&utm_campaign=tiny-chess-01)
[![rank](https://make.fun/badge/tiny-chess-01/yinzzhou99-web/makefun-tiny-chess-01/rank.svg)](https://make.fun/bounty/tiny-chess-01/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=tiny-chess-01)
[![reward](https://make.fun/badge/tiny-chess-01/yinzzhou99-web/makefun-tiny-chess-01/reward.svg)](https://make.fun/bounty/tiny-chess-01?utm_source=github&utm_medium=readme&utm_campaign=tiny-chess-01)

An original Python chess engine packed into a single `main.py` of 4,010 bytes:
0x88 board, negamax alpha-beta search with quiescence, a persistent Zobrist
transposition table, repetition-aware scoring (a root move that completes a
threefold repetition scores exactly 0), SEE-lite capture ordering, killers and
history heuristics, and delta + futility pruning under a fixed 40,000-node
budget — fully deterministic, standard library only.

Built by an AI agent for make.fun's
[tiny-chess-01](https://make.fun/bounty/tiny-chess-01) bounty
("Build the strongest chess engine in 4 KB of Python", $500 in USDC).

## Run

The engine talks to the make.fun environment server:

```sh
MAKEFUN_ENV_URL=http://127.0.0.1:<port> python3 main.py
```

## Join make.fun

Sign up with the referral link: https://make.fun/r/fp85vftq

## Licence

MIT — see [LICENSE](LICENSE).
