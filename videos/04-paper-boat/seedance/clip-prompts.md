# Seedance 2.0 production plan — "The Paper Boat" (1080p, 16:9)

Ready to run when the Higgsfield account has a plan and credits for it.

## Cost (quoted from Higgsfield on 2026-11-17)
| Item | Count | Credits each | Total |
|---|---|---|---|
| Seedance 2.0, 1080p, `mode: std`, 15 s, `generate_audio: false` | 20 clips | 180 | **3,600** |
| Character reference images (optional, recommended) | 2–3 | small | ~10 |
| Voiceover (seed_audio, voice Celine), about 420 words | 8 lines | ~0.5–1.5 | **~15** |
| **Total** | | | **~3,625 credits** |

**Requirements:** Seedance 2.0 at 1080p needs `mode: "std"`, which requires the **Plus plan or higher**. The account is currently on the free plan with 1.7 credits.

## Locked style (paste at the start of EVERY clip prompt)
```
Warm 2D storybook animation, soft painterly textures, gentle rim light, cozy muted palette of teal, mustard yellow and warm wood, rainy-day atmosphere, consistent characters: MIRA — 7-year-old girl, medium-brown skin, two puffy hair buns, big round eyes, yellow raincoat; GRANDPA — elderly man, light-brown skin, white hair on the sides, bald top, round glasses, white mustache, green cardigan. No text, no logos, no speech, no lip movement.
```
Generate a **character reference sheet** of Mira and Grandpa first (generate_image), then pass it as `image_references` on every clip for consistency.

## Clips (15 s each = 5:00)
| # | Time | Clip prompt (after the style block) |
|---|---|---|
| 1 | 0:00 | Slow push-in on a rain-streaked kitchen window at dawn; inside, Grandpa sits at a wooden table holding a square of white paper, hands perfectly still, confused expression. |
| 2 | 0:15 | Close-up of Grandpa's wrinkled hands holding the blank paper; raindrops on the window behind; he looks up, lost. |
| 3 | 0:30 | Flashback, warmer golden tones: Grandpa (slightly younger) quickly folding a paper boat while 4-year-old Mira watches amazed. |
| 4 | 0:45 | Flashback: Grandpa and little Mira in raincoats racing two paper boats down a rainwater stream along a street curb, laughing and splashing. |
| 5 | 1:00 | Flashback: Grandpa writing a tiny note and tucking it inside a paper boat, winking at Mira. Fade back to cooler present-day tones. |
| 6 | 1:15 | Present day: Grandpa opens the fridge and places his keys inside next to the milk, then walks away; Mira notices from the doorway. |
| 7 | 1:30 | Mira at the window looking from the rain to Grandpa at the table; determined expression forms on her face. |
| 8 | 1:45 | Mira at the table folding paper with her tongue out in concentration; her first result looks like a paper hat — she puts it on her head. |
| 9 | 2:00 | Mira's second attempt flops over looking like a paper frog; she frowns; third attempt crumples into a ball that bounces off her forehead. |
| 10 | 2:15 | Mira places a lopsided paper boat in a sink full of water; it sinks with a few bubbles; outside the window the rain is getting lighter. |
| 11 | 2:30 | Mira searching Grandpa's bookshelf, pulling books aside; she discovers an old dented blue tin box behind them. |
| 12 | 2:45 | Mira opens the tin box: dozens of small yellowed paper boats inside; warm light falls on her amazed face. |
| 13 | 3:00 | Close-up: Mira's small hands very carefully unfolding an old paper boat, revealing crease lines and faded handwriting in the center (unreadable). |
| 14 | 3:15 | Mira refolding the paper along the old creases, one step at a time; a perfect paper boat forms in her hands; she smiles. |
| 15 | 3:30 | Mira runs down a hallway holding the paper boat up high toward the kitchen. |
| 16 | 3:45 | Grandpa looks at the boat with a blank expression; Mira places a fresh square of paper in his hands and puts her small hands on top of his. |
| 17 | 4:00 | Close-up of four hands folding paper together; gradually Grandpa's fingers start moving faster on their own; he makes the final fold alone. |
| 18 | 4:15 | Grandpa looks up at Mira and smiles with recognition; he hands her a pencil; she writes a secret note and tucks it into the boat. |
| 19 | 4:30 | Outside under the last light drizzle: Mira and Grandpa crouch at the curb and place two paper boats into the rainwater stream. |
| 20 | 4:45 | Wide shot: two paper boats sail side by side down the shining street as the clouds part and sunlight breaks through; Mira and Grandpa hold hands. |

## Assembly
Join the 20 clips in order. Lay `voiceover` lines on the scene starts in `script.md`, add soft piano and rain ambience, burn captions from `../transcript.txt`, and export H.264 1080p.
