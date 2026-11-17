# Upload Metadata — "What Happens to Your Body If You Stay Awake for 11 Days"

Copy and paste each block into YouTube Studio → **Create → Upload video**.

---

## 1. Title

**Primary (66 chars):**
```
What Happens to Your Body If You Stay Awake for 11 Days
```

**Alternates** (use in Studio's *Test & Compare* or swap after 48 h if CTR < 4%):
1. `A Teen Stayed Awake for 264 Hours. Here's What Happened to Him`
2. `Your Body Without Sleep: Hour by Hour (Day 11 Is Terrifying)`
3. `What If You Never Slept Again? Day 1 to Day 11`

Rules followed: under 70 chars so it isn't cut off on mobile, "you/your body" framing, a specific number, curiosity gap.

---

## 2. Thumbnails (1280×720 PNG, all under 2 MB)

| File | Concept | Best for |
|---|---|---|
| `thumbnails/thumbnail-A.png` | Bloodshot eyes, red circle and arrow, "DAY 11?!", "NO SLEEP" | **Default.** Strongest emotional face plus question |
| `thumbnails/thumbnail-B.png` | Split screen: "DAY 1" happy vs "DAY 11" spiral eyes | Transformation contrast, reads instantly at small size |
| `thumbnails/thumbnail-C.png` | "11 DAYS AWAKE", "264 HOURS", clock, shadow figure | Hallucination/creepy angle, pairs with alt title #1 |

**A/B test:** upload all three in Studio → *Test & Compare* (YouTube picks the winner by watch time, usually within 1–2 weeks).
**Editable source:** `thumbnails/thumbnail-source.html`. Re-render with `node thumbnails/render.js thumbnails`.

---

## 3. Description

```
What happens to your body if you stay awake for 11 days straight? In 1963, a 17-year-old named Randy Gardner stayed awake for 264 hours for a science fair project, and scientists watched every step. Here's what sleep deprivation does to you, hour by hour.

From your brain getting "tipsy" after 24 hours, to microsleeps, hallucinations, and believing you're a famous football player, this is what really happens when you stop sleeping. And why you should never, ever try it.

⏱ TIMESTAMPS
0:00 It's 3 a.m. and you've been awake for 72 hours
0:45 The teenager who stayed awake for 11 days
1:21 Hour 16: I'm fine, totally fine
1:48 Hour 24: Your brain is basically tipsy
2:33 Hour 36: Microsleeps
3:15 Day 2: Your brain's cleaning crew goes on strike
3:48 Day 3: Reality starts to glitch
4:17 Day 4: The football player moment
4:42 Days 5–7: Running on fumes
5:34 Days 8–11: The final stretch
6:23 Why you should NEVER try this
7:16 Quiz answer

💬 What's the longest YOU'VE ever stayed awake? Tell us in the comments!

🔔 Subscribe for more and stay on the bright side!

#sleep #sleepdeprivation #humanbody

Disclaimer: This video is for entertainment and educational purposes only. It is not medical advice. If you have trouble sleeping, please talk to a doctor.

Sources:
- Gulevich, Dement & Johnson (1966), "Psychiatric and EEG observations on a case of prolonged (264 hours) wakefulness," Archives of General Psychiatry
- Dawson & Reid (1997), "Fatigue, alcohol and performance impairment," Nature
- Xie et al. (2013), "Sleep drives metabolite clearance from the adult brain," Science
- Spiegel et al. (2004), "Sleep curtailment in healthy young men is associated with decreased leptin levels, elevated ghrelin levels, and increased hunger and appetite," Annals of Internal Medicine

Music: [add your track + license]
Animation: [add credit]
```

> ⚠️ **Re-check the timestamps after the final edit.** They are calculated from the script at about 140 wpm (estimated total about 7:50). YouTube needs the first chapter at 0:00, at least 3 chapters, and each chapter at least 10 seconds long.

---

## 4. Tags (≈470 / 500 chars)

```
sleep deprivation, what happens if you dont sleep, stay awake for 11 days, randy gardner, 264 hours awake, no sleep for days, sleep deprivation effects, what happens to your body without sleep, longest time without sleep, microsleep, sleep facts, human body facts, brain facts, hallucinations from no sleep, all nighter, insomnia, why we need sleep, science explained, educational animation, what if
```

**Hashtags:** the first 3 in the description show above the title: `#sleep #sleepdeprivation #humanbody`

---

## 5. Studio settings

| Setting | Value |
|---|---|
| Audience | **No, it's not made for kids.** Choosing "made for kids" turns off comments and end screens. The topic suits a general audience, not specifically kids |
| Age restriction | None |
| Paid promotion | Tick only if you have a sponsor |
| Altered or synthetic content | **Yes** if you use realistic AI voice or AI visuals that look real. Cartoon animation does not need it |
| Category | **Education** (alternative: Science & Technology) |
| Video language / caption language | English |
| Captions | Subtitles → Add → **Auto-sync**, paste `transcript.txt` |
| License | Standard YouTube License |
| Comments | On, sort by Top |
| Shorts remixing | Allow |
| Recording date / location | Leave blank |
| Monetization | On; ad breaks around 2:33, 4:42 and 6:23 (only if the video is 8:00 or longer, otherwise automatic) |

> 💡 If the final cut runs **8:00 or longer**, you can place mid-roll ads manually. At about 7:50 you are just short, so a 15-second slower read or a slightly longer outro gets you there.

---

## 6. End screen (last 20 s, from about 7:30)
- **Element 1:** Video → "Best for viewer" (or your best-performing video)
- **Element 2:** Playlist → "The Human Body" (create it if needed)
- **Element 3:** Subscribe button
- Leave the bottom-left area clear for the animated "Zzz" sleeping character from the script

## 7. Cards
| Time | Card |
|---|---|
| 1:48 | Poll: "Longest you've stayed awake?": <24 h / 24–48 h / 48 h+ / I need my 8 hours |
| 4:17 | Video: your next body/brain video |
| 6:23 | Playlist: Human Body |

---

## 8. Pinned comment
```
QUICK QUIZ 🧠 Without scrolling back: how many HOURS did Randy stay awake? 👇
(Bonus: what's the longest YOU'VE ever gone without sleep? 😴)
```

## 9. Community post (24 h before release)
```
POLL 😴 Tomorrow's video: a teenager stayed awake for 11 DAYS straight. What do you think happened on day 4?
🏈 He thought he was a famous athlete
👻 He saw ghosts
😡 He got super angry
😴 He fell asleep standing up
```

---

## 10. Publishing schedule
- Upload as **Private**, then **Schedule** about 2 h before your audience's peak (Studio → Analytics → Audience → *When your viewers are on YouTube*). With no data yet, Thursday–Saturday at 2–4 pm in your main audience's time zone is a reasonable default.
- Make sure processing reaches **HD** before it goes live.
- Post 2 Shorts (see `shorts.md`) on days +1 and +3, each linking the full video via "Related video".

## 11. 48-hour health check
| Metric | Target | If it misses |
|---|---|---|
| CTR | ≥ 5% | Swap to the next thumbnail or alt title |
| Avg. view duration | ≥ 45% | Tighten the 0:45–1:48 section in the next video |
| 30-s retention | ≥ 70% | Hook is working; keep the format |
