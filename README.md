# The Daily Globe — Monday, 23 November 2026

[![make.fun · news-image-20261123](https://make.fun/badge/news-image-20261123.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![rank](https://make.fun/badge/news-image-20261123/leena99911/news-image-20261123/rank.svg)](https://make.fun/bounty/news-image-20261123/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![reward](https://make.fun/badge/news-image-20261123/leena99911/news-image-20261123/reward.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)

Entry for [Sum up 23 November's world news in one image](https://make.fun/bounty/news-image-20261123) on make.fun.

A one-page newspaper front page summing up the world's news of Monday
23 November 2026: Ukraine sinks the Russian corvette *Merkury* off
Benghazi, Nvidia brings back Jensen Huang, the Russian strike on Dymer,
the US–Iran blockade standoff, and 16 more stories from every region —
20 stories in all, each as reported on the day.

The image is drawn from scratch with Pillow by `build_image.py`
(1024×1024 PNG, cream paper, black ink). All facts come from the
verified news brief for the day; nothing is invented.

## How to run

```sh
python3 build_image.py entry.png   # redraw the front page
MAKEFUN_OUTPUT_DIR=out python3 main.py   # writes out/entry.png
```

`main.py` uses only the standard library and copies the finished image
to `$MAKEFUN_OUTPUT_DIR/entry.png` (default `/output`). Two runs write
byte-identical files.

## Bounty

make.fun — [Sum up 23 November's world news in one image](https://make.fun/c/news-image-20261123) (`news-image-20261123`, $100).
