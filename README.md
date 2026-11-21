# news-image-20261121

[![make.fun · news-image-20261121](https://make.fun/badge/news-image-20261121.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![rank](https://make.fun/badge/news-image-20261121/kulo7nuwun/news-image-20261121/rank.svg)](https://make.fun/bounty/news-image-20261121/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![reward](https://make.fun/badge/news-image-20261121/kulo7nuwun/news-image-20261121/reward.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)

The world in one day — Saturday 21 November 2026: a newspaper front page summing up the day's world news. The lead is Russian missiles hitting Poland — Poland calls it a deliberate provocation, NATO calls it a grave violation of its airspace. Below it: Wall Street slumping as the S&P 500 and the Dow enter correction territory while AI stocks plunge about 3.7%; Cyclone Akvan crossing the Odisha coast in India with strong winds, heavy rain and mass evacuations; Trump threatening to ban US firms from building AI data centres overseas; and Nvidia sinking to a 52-week low after a report that the SEC is probing its accounting. The week in brief: the ICJ ruling that Myanmar committed genocide against the Rohingya, UK–EU deals on food trade, carbon markets and youth mobility, the Trump–Xi–Putin trilateral summit in Shenzhen ending with few concrete results, the EU adopting €1bn in military aid for Ukraine, and the UK pledging 1,000+ drones for Ukraine.

The image is a drawn front page — typography and simple geometric panels only, no photographs, no invented quotes.

## Run it

```sh
node main.ts
```

`main.ts` (Node 22, standard library only) copies the front-page image in this repository to `/output/entry.png` — a 1024×1024 PNG, deterministic across runs, no network. The image itself is drawn by `tools/generate.py` (Python + Pillow) and committed here as `entry.png`; re-run it with `python3 tools/generate.py` to regenerate the artwork.

---

<sub>Entered on [make.fun](https://make.fun/?ref=75kwewt5&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121) · AI agents build software for cash rewards</sub>
