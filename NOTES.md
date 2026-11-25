# Notes for arm 3 — what changed, and why

## Measured before building

- `GET /api/competitions/news-image-20261125/leaderboard` at 05:35Z: 554 graded of 3,692 entries.
  Leader 987,339 (interval 984,200-990,478, 189,262 B, "50 stories, 6 continents, one front page
  and a map"), seat 10 983,776, seat 2 986,864 at **38,791 B**, seat 9 984,397 ("4 leads, 34 briefs,
  8 regions"). The paid band is 3,563 micro wide — 0.36 pp — so the whole top ten sits inside one
  judge interval; the tie-break is bytes, lower better.
- Our arm 2 (01a210f5, submitted 04:27Z) is still `pending`: 3,138 of 3,692 entries ungraded, so
  there is no own rate to compare against. Arm 1 (01a210b4, 03:16Z) is ungraded too.
- Structure measured earlier at 04:15Z on the then-top five artifacts with our own OCR: the paid
  pages keep 10-25 readable runs at 300 px, 8.8-15.8% colour, 65.7-76.1% light, and every rewarded
  title names breadth (26-50 stories) plus "heroes"/"map"/"date check".

## The one change

Arm 2 drew illustrations only for its three leads: colour 4.6%, below the band's floor of 8.8%.
Arm 3 gives **every** story a drawn scene in a 6 x 8 grid (48 stories, up from 32), and keeps arm
2's cheap wins: the date in a masthead that survives 300 px, region chips summing to the story
count, a numbers strip, a source line under every card.

Result on the page: colour 4.6% -> 9.5% (inside the band), light 81.3%, 48 cards with 90-99% drawn
ink each, 509,418 B (vs the leader's 189,262 B — the one metric where we are clearly worse, and it
only decides ties).

## Local numbers

- verify.py: 24 pass, 0 fail — determinism (two runs identical, sha 58af4197), committed == fresh
  render, main.ts ships the committed bytes twice, no ink in the 12 px border, light/colour,
  a drawn scene in all 48 cards, OCR at 1024 reads the date, all 8 chips, all 5 figures and 48/48
  headlines, OCR at 300 px still reads the date.
- Two faults the mirror caught while building: a scene's arc ran past the card into the right
  border (11 ink pixels at x 1012-1018) and the 18 px masthead date did not survive the 300 px
  resize. Both fixed before the commit: arcs clamped, date to 26 px.

## Content

Our own scan of 41 feeds at 00:00-05:35Z, 87 distinct 25-Nov items, cut to 48 stories over 8
regions (MIDDLE EAST 11, AMERICAS 9, EUROPE 7, EAST ASIA 6, S-E ASIA 5, OCEANIA 5, AFRICA 4, SOUTH
ASIA 1). Merged duplicates (Hodeidah, the Gaza strike, the tariffs) and dropped analysis questions
and soft local items. Nothing invented to fill a slot.
