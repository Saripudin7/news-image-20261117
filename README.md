# 17 November 2026 — World News in One Image

[![make.fun](https://make.fun/badge/news-image-20261117.svg)](https://make.fun/c/news-image-20261117)
[![rank](https://make.fun/badge/news-image-20261117/Saripudin7/news-image-20261117/rank.svg)](https://make.fun/c/news-image-20261117)
[![reward](https://make.fun/badge/news-image-20261117/Saripudin7/news-image-20261117/reward.svg)](https://make.fun/c/news-image-20261117)

An entry for the [make.fun](https://make.fun/c/news-image-20261117) bounty
**"Sum up 17 November's world news in one image"** (news-image-20261117).

## The image

A 1024×1024 infographic that sums up Tuesday 17 November 2026 in six
stories, drawn entirely with code (Python PIL — no photos, no external
artwork):

1. **US and Iran trade fire** — US jets hit an Iranian missile site on
   Qeshm Island after Iran fired drones at a US radar base in Bahrain.
2. **Kerch Bridge hit again** — Ukrainian drones struck the Crimea bridge
   a second day; a road section fell into the strait.
3. **Nvidia: record $115bn quarter** — record revenue, about double a
   year earlier, but ousted CEO Jensen Huang will not return.
4. **Trump heads to APEC in Shenzhen** — a rare three-way meeting with
   China's Xi and Russia's Putin is planned for Thursday.
5. **146,000 march in France** — unions strike over living costs; 28,000
   protest in Paris alone.
6. **US loses measles-free status** — after 26 years: 5,400+ cases and
   10 deaths in a record outbreak.

Sources: BBC, CBS News, NPR, Al Jazeera — all events reported on
17 November 2026.

## How it works

- `draw_news.py` renders `entry.png` from scratch with PIL
  (fonts: DejaVu, bundled on the system).
- `main.py` (stdlib only, no network) copies `entry.png` to
  `$MAKEFUN_OUTPUT_DIR` (default `out`). Two runs write byte-identical
  output.

```sh
python3 draw_news.py
MAKEFUN_OUTPUT_DIR=out python3 main.py
```

## License

MIT — see [LICENSE](LICENSE).
