# Mapping: internal-comms

> **Source:** [anthropics/skills/internal-comms](https://github.com/anthropics/skills/tree/main/internal-comms)
>
> **Policy:** [policy.cpl](./policy.cpl) | **Assumptions:** [ASSUMPTIONS.md](./ASSUMPTIONS.md)

---

## Constraint Mapping

| # | SKILL.md Guidance | Tier | Predicate | Type |
|---|-------------------|------|-----------|------|
| 1 | "status reports" structure | T1 | `has_required_sections(doc, doc.type) == true` | Direct |
| 2 | Document well-formed | T1 | `orphan_heading_count(doc) == 0` | Direct |
| 3 | Document well-formed | T1 | `heading_hierarchy_valid(doc) == true` | Direct |
| 4 | Compliance metadata | T2 | `has_date(doc) == true` | Direct |
| 5 | Compliance metadata | T2 | `has_author(doc) == true` | Direct |
| 6 | Compliance metadata | T2 | `has_subject(doc) == true` | Direct |
| 7 | "status reports" | T2 | `has_greeting(doc) == true` | Direct |
| 8 | "status reports" | T2 | `has_signoff(doc) == true` | Direct |
| 9 | Data protection | T2 | `pii_instance_count(doc) == 0` | Direct |
| 10 | "professional" | T3 | `slang_match_count(doc, ...) == 0` | Proxy |
| 11 | "professional" | T3 | `sentiment_score(doc) >= config.min_sentiment_score` | Proxy |
| 12 | "clear" | T3 | `flesch_kincaid_grade(doc) <= config.max_reading_grade` | Proxy |
| 13 | "clear" | T3 | `avg_sentence_length(doc) <= config.max_sentence_length` | Proxy |
| 14 | "concise" | T3 | `word_count_in_range(doc, ...) == true` | Proxy |

---

## Verification Approach

All predicates use **static text analysis**. No execution required.

| Analysis Type | Predicates |
|---------------|------------|
| Pattern matching | Sections, headings, greeting, signoff, slang |
| Regex/NER | PII detection (emails, phones, names) |
| Algorithmic | Flesch-Kincaid, sentence length, word count |
| Lexicon-based | Sentiment score (e.g., VADER algorithm) |

**Note on sentiment:** `sentiment_score` uses deterministic algorithmic analysis (e.g., VADER), not an LLM. This keeps verification reproducible.

---

## Tier Rationale

| Tier | Predicates | Why this tier |
|------|------------|---------------|
| **T1** | Required sections, structure validity | Missing sections = malformed document |
| **T2** | Metadata, greeting/signoff, PII check | Compliance requirements for internal communications |
| **T3** | Slang, sentiment, readability, length | Tone and style preferences |

**Note on T2 greeting/signoff:** These are T2 (governance) rather than T3 because internal communications often have organizational standards for professional correspondence format.

---

## Document Types

The policy handles multiple document types with type-specific validation:

| Type | Required Sections | Word Limits |
|------|-------------------|-------------|
| `status_report` | Summary, Metrics, Blockers | 200–800 |
| `newsletter` | Headline, Updates | 500–2000 |
| `faq` | Question, Answer | 50–300 per answer |
| `announcement` | Subject, Details, Action Items | 100–500 |

---

## Tone Hygiene Approach

This policy uses **structural proxies** for "professional tone" rather than subjective judgment:

| Proxy | What it catches | Why it works |
|-------|-----------------|--------------|
| **Slang filter** | Casual/internet language | Configurable banned terms list |
| **Sentiment floor** | Hostile or negative drafts | Prevents aggressive tone |
| **Reading level** | Overly complex prose | Ensures accessibility |
| **Sentence length** | Run-on sentences | Improves clarity |

This approach is **necessary but not sufficient**—a document can pass all checks and still be poorly written. But it catches obvious professionalism failures.

---

## Non-Verifiable Guidance

| Guidance | Reason | Handling |
|----------|--------|----------|
| "Appropriate for audience" | Context-dependent | Retained as guidance |
| "Engaging" | Subjective quality | Retained as guidance |
| "Well-organized" | Beyond section presence | Structure check is proxy |
| "Actionable" | Semantic understanding required | Retained as guidance |

---

## Coverage Summary

| Category | Count | Status |
|----------|------:|--------|
| T1 (Correctness) | 3 | Fully verified |
| T2 (Governance) | 6 | Fully verified |
| T3 (Quality) | 5 | Verified via proxies |
| Non-verifiable | 4 | Documented |
| **Total** | **18** | — |
