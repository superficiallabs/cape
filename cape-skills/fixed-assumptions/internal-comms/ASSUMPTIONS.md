# Assumptions: internal-comms

> **Source:** [anthropics/skills/internal-comms](https://github.com/anthropics/skills/tree/main/internal-comms)
>
> **Policy:** [policy.cpl](./policy.cpl) | **Mapping:** [MAPPING.md](./MAPPING.md)

---

## Overview

The internal-comms skill asks for "professional," "clear," and "concise" communications. These are subjective qualities that cannot be verified directly. We use **tone hygiene** proxies—structural indicators that correlate with professionalism without requiring subjective judgment.

**Philosophy:** We verify what "professional" is *not* rather than what it *is*. No slang, no hostility, not too complex, not too long. Passing these checks doesn't guarantee good writing—it guarantees the writing isn't obviously unprofessional.

**Verification approach:** All predicates use static text analysis—pattern matching, algorithmic readability scores, and lexicon-based sentiment. No execution required.

---

## Assumption 1: No Slang (Professionalism)

**Original guidance:**
> "professional tone"

**Interpretation:**
Professional communications avoid casual/internet slang. We maintain a configurable banned terms list.

**Predicate:**
```
slang_match_count(doc, config.banned_terms) == 0
```

**Tier:** T3 (Preference)

**Default banned terms:**
```json
["lol", "lmao", "rofl", "idk", "gonna", "wanna", "gotta", "kinda", "tbh", "ngl", "imo", "btw"]
```

**Threshold rationale:**

| Match count | Interpretation |
|-------------|----------------|
| 0 | Professional—no slang detected (pass) |
| 1–2 | Casual slip—likely unintentional |
| 3+ | Consistently informal—not professional |

Default threshold is 0 (strict), but can be relaxed for informal cultures.

**What counts as slang:**
- Internet abbreviations (lol, brb, afk)
- Casual contractions (gonna, wanna, gotta)
- Opinion markers (tbh, imo, ngl)

**What doesn't count:**
- Standard contractions (don't, won't, can't)
- Industry jargon (appropriate in context)
- Proper acronyms (API, CEO, Q3)

**Customization:**
- Casual culture: reduce list or raise threshold
- Strict formal: expand list to include more casual terms
- Industry-specific: add domain slang to ban list

---

## Assumption 2: Sentiment Floor (Professionalism)

**Original guidance:**
> "professional tone"

**Interpretation:**
Professional communications should not be hostile or overtly negative. We set a sentiment floor to catch aggressive drafts.

**Predicate:**
```
sentiment_score(doc) >= config.min_sentiment_score
```

**Tier:** T3 (Preference)

**Default threshold:** `min_sentiment_score: 0.0` (neutral)

**Implementation:** Uses algorithmic sentiment analysis (e.g., VADER), not an LLM. This ensures deterministic, reproducible results.

**Threshold rationale:**

| Sentiment | Interpretation |
|-----------|----------------|
| < -0.5 | Hostile—aggressive language |
| -0.5 to 0.0 | Negative—critical but not hostile |
| 0.0 | Neutral—professional baseline (default) |
| 0.0 to 0.5 | Positive—constructive tone |
| > 0.5 | Very positive—enthusiastic |

**What this catches:**
- Hostile phrasing ("This is unacceptable")
- Passive-aggressive language
- Overtly negative framing

**What this doesn't catch:**
- Subtle negativity
- Appropriate criticism (may need context)
- Sarcasm (often neutral sentiment score)

**Customization:**
- Feedback documents: may need negative sentiment for critiques—lower to `-0.3`
- Customer-facing: raise to `0.2` for positive tone
- Announcements: raise to `0.1` for generally positive framing

---

## Assumption 3: Reading Level (Clarity)

**Original guidance:**
> "clear communication"

**Interpretation:**
Clear writing is accessible to a broad audience. We use Flesch-Kincaid grade level as a readability proxy.

**Predicate:**
```
flesch_kincaid_grade(doc) <= config.max_reading_grade
```

**Tier:** T3 (Preference)

**Default threshold:** `max_reading_grade: 10` (10th grade / age 15–16)

**Implementation:** Purely algorithmic—based on syllable count and sentence length. No NLP model required.

**Threshold rationale:**

| Grade level | Audience | Examples |
|-------------|----------|----------|
| 5–6 | General public | USA Today, most web content |
| 7–8 | Average adult | Time magazine |
| 9–10 | Educated adult | Wall Street Journal (default) |
| 11–12 | College level | Academic papers |
| 13+ | Graduate level | Legal documents, technical papers |

**Limitations:**
- Doesn't measure clarity of ideas
- Technical terms inflate score (may be appropriate)
- Very short documents have unstable scores

**Customization:**
- Executive summaries: lower to `8`
- Technical documentation: raise to `12` (jargon expected)
- All-hands communications: lower to `8` for broad accessibility

---

## Assumption 4: Sentence Length (Clarity)

**Original guidance:**
> "clear communication"

**Interpretation:**
Long sentences are harder to parse. We cap average sentence length as a clarity proxy.

**Predicate:**
```
avg_sentence_length(doc) <= config.max_sentence_length
```

**Tier:** T3 (Preference)

**Default threshold:** `max_sentence_length: 25` words

**Threshold rationale:**

| Avg length | Interpretation |
|------------|----------------|
| < 15 | Very short—may feel choppy |
| 15–20 | Short—easy to read |
| 20–25 | Medium—professional standard (default ceiling) |
| 25–30 | Long—harder to follow |
| > 30 | Very long—likely run-on sentences |

**Customization:**
- Quick updates: lower to `20`
- Narrative content: allow up to `30`
- Technical writing: may need longer for complex explanations

---

## Assumption 5: Word Count Bounds (Conciseness)

**Original guidance:**
> "concise"

**Interpretation:**
Different document types have appropriate length ranges. Too short suggests incomplete; too long suggests bloat.

**Predicate:**
```
word_count_in_range(doc, config.word_limits[doc.type]) == true
```

**Tier:** T3 (Preference)

**Default thresholds by type:**

| Document type | Min words | Max words | Rationale |
|---------------|-----------|-----------|-----------|
| `status_report` | 200 | 800 | Substantive but focused |
| `newsletter` | 500 | 2000 | Room for multiple updates |
| `faq_answer` | 50 | 300 | Per answer, not total |
| `announcement` | 100 | 500 | Key info without bloat |

**What this catches:**
- Stub documents (too short to be useful)
- Bloated documents (could be tighter)

**Customization:**
- Adjust per organizational norms
- Some types may not have limits (set very wide range)
- Can disable by setting min=0, max=999999

---

## Not Verified (T1/T2 Only)

These constraints are objectively verifiable without assumptions:

| Constraint | Tier | Why no assumption needed |
|------------|------|--------------------------|
| Required sections present | T1 | List comparison—deterministic |
| Heading structure valid | T1 | DOM/structure analysis |
| Metadata present (date/author/subject) | T2 | Field presence check |
| Greeting present | T2 | Pattern matching |
| Sign-off present | T2 | Pattern matching |
| No PII | T2 | Regex + entity detection |

---

## Not Verified (Genuinely Subjective)

| Guidance | Reason | Handling |
|----------|--------|----------|
| "Appropriate for audience" | Requires knowing audience | Retained as guidance |
| "Engaging" | Subjective quality | Retained as guidance |
| "Well-organized" | Beyond section presence | Structure is proxy only |
| "Actionable" | Requires semantic understanding | Retained as guidance |
| "Timely" | Context-dependent | Retained as guidance |

---

## Configuration Reference

```json
{
  "configuration": {
    "max_reading_grade": 10,
    "max_sentence_length": 25,
    "min_sentiment_score": 0.0,
    "banned_terms": ["lol", "lmao", "rofl", "idk", "gonna", "wanna", "gotta", "kinda", "tbh", "ngl", "imo", "btw"],
    "status_report_sections": ["Summary", "Metrics", "Blockers"],
    "newsletter_sections": ["Headline", "Updates"],
    "faq_sections": ["Question", "Answer"],
    "announcement_sections": ["Subject", "Details", "Action Items"],
    "word_limits": {
      "status_report": { "min": 200, "max": 800 },
      "newsletter": { "min": 500, "max": 2000 },
      "faq_answer": { "min": 50, "max": 300 },
      "announcement": { "min": 100, "max": 500 }
    }
  }
}
```

Override any threshold at evaluation time to match your organizational standards.
