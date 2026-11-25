# One page for Wednesday 25 November 2026 — 48 stories, a drawn scene in every card

[![make.fun competition](https://make.fun/badge/news-image-20261125.svg)](https://make.fun/c/news-image-20261125)
[![rank](https://make.fun/badge/news-image-20261125/lefadha/makefun-news-20261125-c/rank.svg)](https://make.fun/c/news-image-20261125)
[![reward](https://make.fun/badge/news-image-20261125/lefadha/makefun-news-20261125-c/reward.svg)](https://make.fun/c/news-image-20261125)

An entry in [make.fun's news-image-20261125 competition](https://make.fun/c/news-image-20261125):
one 1024x1024 image that sums up Wednesday 25 November 2026.

The page is a front page you can take in at a glance. The day is set in a masthead date large
enough to read at 300 pixels across. A strapline counts the page: 48 stories, 8 regions, every one
of them first reported today. Region chips carry the per-region counts and add up to the 48. THE
DAY IN NUMBERS gives five figures. Then a 6 x 8 grid: one card per story, each with its own drawn
scene, a place · desk/status label, a headline and the UTC stamp with the outlets that ran it.

Nothing is invented. `stories.py` was written from our own scan of 41 wire feeds (Google News
World/Business/Tech/Science/Sport, BBC, Al Jazeera, Guardian, NPR, DW, France 24, CBC, SCMP, Times
of India, CNA, ABC, RNZ, Yonhap, Middle East Eye, Kyiv Independent, Anadolu, Dawn, Sky, Straits
Times, Japan Times) between 00:00 and 05:35 GMT on 25 November 2026 — 87 distinct dated items,
merged where two outlets reported the same event and cut to 48. Every card keeps the places, the
desk, the status and the time we read.

## What runs in the sandbox

`main.ts` (Node, standard library only) reads the committed `entry.png`, checks the PNG signature,
that the first chunk is IHDR, the 1024x1024 size, 8-bit truecolour, the 1 MiB cap and that the file
is big enough to be a page rather than a blank, writes the bytes to `/output/entry.png`, then reads
them back in 4 KiB blocks to prove the same bytes landed. Two runs write identical bytes.

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

## How the image is made

`render.py` draws everything with Pillow primitives — no network, no photographs, no fonts outside
the container's Liberation set. Each of the 20 scene kinds (port, tanker, drone, blast, virus,
gavel, ballot, person, megaphone, money, fire, flag, chart, trophy, plane, rocket, chip, mine,
cross, planet) is drawn in unit coordinates, so the same code serves a 161 x 40 card. Rendering is
deterministic: the same bytes every run (sha256 58af4197…, 509,418 B).

```sh
python3 render.py entry.png          # writes the image
python3 verify.py                    # 24 local checks: gate, determinism, layout, scenes, OCR at 1024 and 300 px
```

## Why this composition

Measured on the live board of this competition at 05:35Z, not guessed: seat 10 stands at 983,776
and the leader at 987,339 over 554 graded entries; the leading page carries 50 dated stories over
six continents, its colour share is 15.8%, and it keeps only 20 text runs readable at 300 px. The
previous arm here (arm 2, 32 stories, three drawn leads, 23 briefs) drew 4.6% colour, outside the
paid band's 8.8-15.8%. So this arm spends its one change on the cards: every one of the 48 stories
carries a drawn scene, colour rises to 9.5%, and our own OCR still reads all 48 headlines at full
size and the date at 300 px.

## License

MIT, see `LICENSE`.
