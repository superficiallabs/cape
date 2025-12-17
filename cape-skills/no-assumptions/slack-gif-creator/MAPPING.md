# Mapping: slack-gif-creator

> **Source:** [anthropics/skills/slack-gif-creator](https://github.com/anthropics/skills/tree/main/slack-gif-creator)
>
> **Policy:** [policy.cpl](./policy.cpl)
>
> **Category:** No assumptions needed
>
> **Platform:** [Slack Custom Emoji Guidelines](https://slack.com/help/articles/206870177-Add-custom-emoji-and-aliases-to-your-workspace)

---

## Constraint Mapping

| # | SKILL.md Guidance | Tier | Predicate | Type |
|---|-------------------|------|-----------|------|
| 1 | GIF format | T1 | `gif_format(file) == 'GIF89a'` | Direct |
| 2 | GIF format | T1 | `gif_header_valid(file) == true` | Direct |
| 3 | "Animated GIFs" | T1 | `frame_count(file) > 1` | Direct |
| 4 | "64KB limit is strict" | T1 | `file_size_bytes(file) <= 65536` | Direct |
| 5 | "128x128 dimensions" | T1 | `width(file) == 128` | Direct |
| 6 | "128x128 dimensions" | T1 | `height(file) == 128` | Direct |
| 7 | "Smooth animation" | T1 | `min_frame_delay_ms(file) >= 20` | Direct |
| 8 | "Smooth animation" | T1 | `max_frame_delay_ms(file) <= 100` | Direct |
| 9 | GIF specification | T1 | `color_table_size(file) <= 256` | Direct |
| 10 | Optimization | T3 | `duplicate_frame_count(file) == 0` | Proxy |

---

## Verification Approach

All predicates use **static file inspection**. No execution required.

| Analysis Type | Predicates |
|---------------|------------|
| Header parsing | GIF format, header validity |
| Frame parsing | Frame count, delays, duplicates |
| Metadata | File size, dimensions |
| Color table | Color count |

---

## Tier Rationale

| Tier | Predicates | Why this tier |
|------|------------|---------------|
| **T1** | Format, animation, size, dimensions, timing, colors | Platform rejection or unusable output |
| **T3** | Duplicate frames | Optimization preference |

**Note on frame timing as T1:** Frame delays outside 20–100ms cause:
- Too fast (<20ms): Many platforms cap at 20ms, causing unexpected speed
- Too slow (>100ms): Appears broken or frozen

This is functional behavior, not quality preference.

---

## Slack Emoji Constraints

Slack imposes hard limits on custom emoji:

| Constraint | Limit | Consequence of Violation |
|------------|-------|--------------------------|
| File size | ≤64KB (65,536 bytes) | Upload rejected |
| Dimensions | Exactly 128×128 px | Upload rejected |
| Format | GIF, PNG, JPG | Upload rejected |

For animated emoji, GIF89a is required (GIF87a doesn't support animation).

---

## GIF89a Specification

| Requirement | Value | Standard |
|-------------|-------|----------|
| Header | `GIF89a` | GIF89a spec |
| Color table | ≤256 colors | GIF spec |
| Frame count | >1 for animation | GIF89a spec |
| Frame delay | 10ms–655350ms | GIF spec (but 20–100ms practical) |

---

## Frame Timing

| Frame delay | FPS | Result |
|-------------|-----|--------|
| <10ms | >100 | Browsers cap to 10ms |
| 10–20ms | 50–100 | May be capped by some platforms |
| 20–50ms | 20–50 | Smooth animation (ideal) |
| 50–100ms | 10–20 | Acceptable, slightly slow |
| >100ms | <10 | Appears choppy or frozen |

Default acceptable range: 20–100ms (10–50 FPS).

---

## Coverage Summary

| Category | Count | Status |
|----------|------:|--------|
| T1 (Correctness) | 9 | Fully verified |
| T2 (Governance) | 0 | Not applicable |
| T3 (Quality) | 1 | Optimization only |
| **Total** | **10** | — |
