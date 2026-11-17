# Video packages

| # | Video | Pillar | Why it should perform | Release order |
|---|---|---|---|---|
| 01 | What Happens to Your Body If You Stay Awake for 11 Days (`../upload-package/`) | Body / health | "Your body" framing plus a real record-holder story | 1st |
| 03 | What If You Fell Into the Mariana Trench? (`03-mariana-trench/`) | Deep sea "what if" | Matches the channel's latest upload theme; a depth meter drives retention | 2nd |
| 02 | Why Planes Almost Never Fly Over Tibet (`02-tibet-no-fly/`) | Hidden-reason explainer | Evergreen "why planes never fly over…" format with strong search demand | 3rd |

Each folder contains `script.md`, `metadata.md` (title, description, chapters, tags, settings, cards, pinned comment, community post), `transcript.txt` (for caption auto-sync), `shorts.md`, and `thumbnails/` (3 options plus editable source).

Re-render thumbnails after editing a source:
```bash
node videos/render.js videos/02-tibet-no-fly T
node videos/render.js videos/03-mariana-trench M
```

**Runtime note:** both new scripts run about 7 minutes at 140 wpm. Each script says what to add to pass 8:00 if you want mid-roll ads.
