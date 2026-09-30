# Loopback: Product Bible  `APPROVED IN PRINCIPLE` (Scott, 2026-09-30)

Supersedes the pharmacy-refill-reminder idea. The company is still **Loopback** (Loopback.health),
still "closing the loop," still built on "nobody's job is to notice." What changed is the product:
it is now a **check-in for people who might go quiet**, aimed at catching a catastrophe early.

## 1. The promise
Loopback notices when someone has gone quiet and gets a person they chose to check on them.

**It does not promise safety.** It promises to **shorten the silence**: the time between something going
wrong and somebody knowing. The world will never be 100% safe. A false alarm costs a moment of embarrassment;
a missed catastrophe can cost a life. That asymmetry is why the product exists, and why the rules below exist.

**The origin story (used carefully):** a single father has a heart attack at home, and his two-year-old,
alone with him, isn't found for days. Nobody knew. Told plainly by a nurse or clinic director in an
interview (proposed Ch 8), offstage, never graphic.

## 2. Who it's for
| Use case | Why it matters | Where it can come up in the book |
|---|---|---|
| Older adults living alone (launch) | The man in 4B; Mr. Peralta; Ray | Ch 1, 3 (already planted) |
| Recently discharged patients | The first weeks after a hospital stay are the risky ones | Ch 6, 10 (Dr. Okafor) |
| Far-away caregivers | "Is Mom okay?" without calling six times | Ch 12, 22 |
| **Single parent with a newborn** | Postpartum complications; nobody else in the house | Part 4 hospital pilot; Ch 22 |
| **Single parent with a young child** | The child can't wait: shortest clock of all | Ch 8 (the story); Ch 23 |
| Heat and cold waves | Health departments already keep lists of vulnerable residents | Part 5 |
| People who live alone, broadly (the Ch 24 napkin) | Anyone whose silence would go unnoticed | Ch 24 |

Each one widens the product without changing it. They should arrive naturally (a customer asks, a
hospital asks, Maya or Ray says "what about...?"), never as a sales deck.

## 3. The five rules (amended by Scott, 2026-09-30)
1. **Only the person being watched can turn it on.** No one can install it on someone else. (The same tool, in the wrong hands, is how an abuser controls a partner.)
2. **Minimum signal.** The phone decides "quiet or not quiet" **on the device** and sends only that. No messages, no location, no content, no raw audio leaves the phone. (Signals: section 4.)
3. **They choose their people and what happens.** Who gets told, in what order, and whether the ladder ever reaches emergency services.
4. **Everything sent is visible to the user, and they're told when it's sent.** The app has an **Activity view** listing every notification sent about them (to whom, when, why). Each one also **notifies the user at the moment it goes out** ("We told Dana you've been quiet. Tap if that's wrong."). If the app ever malfunctions, both people know, and the user is never surprised.
5. **They can pause or quit.** "Off the grid until Sunday" is one tap. Quitting needs no explanation.

**The dinner-table test:** could the watcher say to your face everything the app knows about you? If yes, it's
care. If no, it's surveillance.

## 4. How it works

### Signals (the person picks from a short menu)
- **Authenticated unlock (default).** The phone was opened with the owner's face or fingerprint. A toddler tapping an unlocked phone doesn't count.
- **The owner's voice (add-on, for households with small children).** At setup the user records a short voice sample (about ten seconds). The phone builds a voiceprint and keeps it in secure storage **on the device**. Afterward the phone only asks, locally, "was that the owner's voice?" A toddler's noise doesn't count. **Nothing is recorded or transcribed, no audio leaves the phone, and the server learns only "owner's voice heard at 10:42."** The mic-in-use indicator is always visible, and it's one tap to turn off.
- **Motion or steps; a pill cap or bottle opening; a smart speaker or wearable** (optional).
- **An optional one-tap daily "I'm up"** for people who like a ritual.

Voice is the most sensitive signal, so it's **opt-in, not default**. Phones also restrict background microphone use, which is a real engineering problem for Priya and Theo (see section 9).

### The AI's job: learn your normal
The model learns each person's own rhythm and the context they chose to share: a night-shift nurse, a new parent up at 3 a.m., someone who naps at noon. It decides when quiet is unusual *for them*. The goal is **very few false alarms**, because people switch off anything that cries wolf.

### The clock depends on who depends on you
The time before anything happens shrinks when someone else relies on you. Story numbers, not medical advice:
| Person | Example window of unusual quiet before the ladder starts |
|---|---|
| Adult living alone | About a day |
| Older adult with a health condition | Half a day of their normal waking hours |
| New mother alone with a newborn | A few hours |
| Single parent with a young child | The shortest: a couple of hours in waking time |

When the user adds "someone depends on me," the windows shrink and the user can pre-agree to an earlier welfare check.

### The escalation ladder (every rung notifies the user)
1. **Nudge the user:** "You've been quiet. Everything okay?" A tap cancels everything, and tells their people "They're fine."
2. **Second nudge, then a call to the user.**
3. **Their first person** gets an alert (and the user is told: "We told Dana.").
4. **Their second person** (and the user is told).
5. **A welfare check by emergency services, only if they pre-agreed.** It is off by default.

**Never police by default.** A welfare check can go badly for someone who was simply asleep or in a mental-health crisis, so it is always a choice made in advance.

### The Activity view
A plain list on the user's phone: what was sent, to whom, when, why, and a "That was a mistake" button. Simple enough for a seventy-year-old to read at a glance.

## 5. The easy yes (opt-in)
**Ask at the moments people are most open:** hospital discharge, bringing the baby home, a parent moving in or out, a first apartment alone, right after a scare.

**Make it a pact.** "I'm your person, you're mine" is an easier yes than "I'm watching you." The watcher says yes too: it's a two-way invitation.

**Setup is about ninety seconds, in three questions:**
1. Who would you want to know? (one or two people; they must accept)
2. How should we tell you're okay? (the signals menu; voice sample if they want it)
3. What should happen, and when? (the ladder in plain sentences, plus the "someone depends on me" toggle)

**The watcher's side:** "You're Dana's person. You'll hear from us only if Dana goes quiet. Here is what to do: call, then knock, then the number Dana gave us."

### At the pharmacy counter (the first test market)
The pharmacy already has the most trusted recurring contact in many people's lives. The technician asks one question: **"If you went quiet for a day, who would you want to know?"** Then they hand over a QR code, and the sign-up finishes on the customer's phone.

**Nate's twenty-second pitch for someone waiting in line:**
> "I'm Nate, I'm with Loopback. One question while you wait: if you went quiet for a day, who'd you want to know? It takes ninety seconds. You choose who. You see everything we send, and you can turn it off any time."

| They say | Good answer |
|---|---|
| "I'm fine." | "I hope so. This only speaks up if you aren't." |
| "I don't want to be tracked." | "We don't know where you are. The phone only says quiet or not quiet." |
| "My kids will worry." | "You decide who gets told. And you see every message." |
| "I'll forget to use it." | "You don't use it. That's the point." |
Most people say no. The story should let Nate take the no seriously.

## 6. Channels and who pays (proposed, to be researched)
- **First test market: a pharmacy chain (Meridian).** Front-door enrollment at the counter, a named person at each store. They pay for retention and better follow-through.
- **Hospitals and postpartum programs.** Enroll new parents at discharge (check-ins tuned to the first weeks, escalation to a nurse line). Hospitals care about readmissions and follow-up gaps.
- **County public health and agencies on aging.** They already keep lists of people they can't check on often enough (heat waves, isolation programs).
- **Health plans and employers** (later).
- Consumers: free or cheap.

## 7. What Loopback will not build (Priya's list, Ch 8)
No location tracking (except when the user presses SOS). No reading messages or content. No selling or sharing data. No ads, and no sponsor names in any message (the drugmaker's $40,000). No secret mode or covert install. No police by default. No alerts about behavior, only about absence.

## 8. The hard cases (good chapter material)
- **Coercion:** someone pressures a partner to "opt in." Mitigations: only self-enrollment, re-consent every few months, a silent way out.
- **Mental-health crises:** a welfare check that makes things worse. Hence: never police by default.
- **People who want to be left alone:** quiet mode, and the ladder stops at their own person.
- **False alarms:** a father at a cabin, a phone left on the counter. The first alert is always a gentle tap, not sirens.
- **A child who can't consent:** the parent consents in advance for both of them.

## 9. The product across the book
| Stage | Version | What happens |
|---|---|---|
| Part 1 | Idea | A system that notices who's gone quiet; "healthcare first"; the man in 4B; Maya rewrites the message |
| Part 2 | Ugly prototype | A morning "You okay?" that texts a person if you don't answer; Dr. Okafor uses it with discharged patients |
| Part 3 | **Version 1: the creepy one** | Investors love "passive monitoring"; Nate and Priya build the phone-data scan. Maya: "tracking me." The Sunday reminder shows him the same error at home. |
| Part 4 | **Version 2: consent-first** | The five rules, the signals menu, the Activity view, the counter script. The pharmacy chain goes live and Nate pitches in line. |
| Part 5 | **Version 3: the named person** | Automated alerts alone get ignored. Each store gets a named person with protected time to make the call. (Carla: "You listened. Nothing changed.") |
| Ch 24 | Next | Living-alone and new-parent use cases widen the company; the napkin stays unfinished |

**The voice debate:** Priya refuses an always-listening microphone; Nate argues the toddler case; they land on on-device voice as an opt-in add-on with a visible indicator, and then hit the phone's own limits (proposed Ch 12 or 13).

**The domain payoff:** *Loopback.com* belongs to a Norwegian shoe company (Ch 3). In Part 5, Nate finally buys it.

## 10. Open questions
- Phone operating systems restrict background microphone use. Fiction can solve it with a bedside or charging mode, or a companion speaker or wearable. Does Scott want the technical problem on the page, or only its result?
- Legal texture (consent, recording, health privacy) should stay light and accurate. Research before any scene leans on it.
- The welfare-check rung: confirm "off by default, pre-agreed only."
- First public-health partner: a county or a hospital system?
