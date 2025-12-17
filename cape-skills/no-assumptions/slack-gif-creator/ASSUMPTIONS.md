# Assumptions: slack-gif-creator

> **Source:** [anthropics/skills/slack-gif-creator](https://github.com/anthropics/skills/tree/main/slack-gif-creator)
>
> **Policy:** [policy.cpl](./policy.cpl) | **Mapping:** [MAPPING.md](./MAPPING.md)
>
> **Category:** No assumptions needed
>
> **Platform:** [Slack Custom Emoji Guidelines](https://slack.com/help/articles/206870177-Add-custom-emoji-and-aliases-to-your-workspace)

---

## No Assumptions Required

This skill falls into the **"No Assumptions Needed"** category. All requirements are derived from platform constraints (Slack) and file format specifications (GIF89a).

### Why No Assumptions?

**1. Platform Hard Limits**

Slack's emoji upload has non-negotiable constraints:
- File size: ≤64KB (65,536 bytes)
- Dimensions: Exactly 128×128 pixels

These aren't preferences—Slack's servers reject files that violate them. There's no subjectivity.

**2. File Format Standard**

GIF89a is a strict binary specification:
- Header must be `GIF89a` (not `GIF87a` for animation)
- Color table limited to 256 colors
- Frame structure defined precisely

Either the file conforms or it doesn't.

**3. Implicit Functional Requirement**

When a user asks for an "animated GIF," they expect animation. A single-frame GIF is:
- Technically valid as a GIF file
- Functionally a failure for the task

We verify `frame_count > 1` as a T1 requirement—not an assumption, but a task-derived constraint.

**4. Practical Frame Timing**

While the GIF spec allows delays from 10ms to 655350ms, practical constraints exist:
- <20ms: Many platforms (browsers, Slack) cap at 20ms
- >100ms: Appears broken or frozen

These are empirical facts about platform behavior, not subjective preferences.

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

## What This Policy Verifies

### T1: Objective Correctness

| Check | Source | What it verifies |
|-------|--------|------------------|
| GIF89a format | GIF spec | Valid animated GIF header |
| Header valid | GIF spec | File structure parseable |
| Frame count >1 | Task requirement | Actually animated |
| Size ≤64KB | Slack platform | Won't be rejected |
| 128×128 pixels | Slack platform | Correct emoji dimensions |
| Frame delay 20–100ms | Platform behavior | Animation plays correctly |
| Color table ≤256 | GIF spec | Valid color palette |

### T3: Optimization

| Check | Source | What it verifies |
|-------|--------|------------------|
| No duplicate frames | Best practice | File size optimization |

---

## Why Frame Timing is T1

Frame timing is T1 (correctness), not T3 (quality), because:

**Too fast (<20ms):** Many platforms cap frame delays at 20ms. A GIF authored at 10ms will play at 20ms, causing unexpected 2× slower animation. This is incorrect behavior, not low quality.

**Too slow (>100ms):** A frame delay of 500ms makes the animation appear frozen or broken. Users will think it failed.

These are functional failures, not aesthetic preferences.

---

## The 64KB Challenge

64KB is extremely tight for animated GIFs. Achieving it requires:

| Technique | Savings |
|-----------|---------|
| Reduce colors | 256→64 colors can halve size |
| Reduce frames | Fewer frames = smaller file |
| Reduce dimensions | Smaller than 128×128, then upscale |
| Lossy compression | Tools like gifsicle --lossy |
| Frame disposal | Reuse unchanged pixels |

The policy verifies the constraint is met but doesn't prescribe how.

---

## Configuration Reference

```json
{
  "configuration": {
    "emoji_max_size_bytes": 65536,
    "emoji_width": 128,
    "emoji_height": 128,
    "min_frame_delay_ms": 20,
    "max_frame_delay_ms": 100,
    "max_color_table_size": 256
  }
}
```

These values match Slack's current requirements. Adjust if platform constraints change.

---

## Summary Table

| Constraint | Source | Predicate | Tier |
|------------|--------|-----------|------|
| Valid GIF89a | GIF spec | `gif_format() == 'GIF89a'` | **T1** |
| Is animated | Task requirement | `frame_count() > 1` | **T1** |
| Size ≤64KB | Slack platform | `file_size_bytes() <= 65536` | **T1** |
| 128×128 pixels | Slack platform | `width() == 128`, `height() == 128` | **T1** |
| Frame timing | Platform behavior | `frame_delay in [20ms, 100ms]` | **T1** |
| Color table | GIF spec | `color_table_size() <= 256` | **T1** |
| No duplicates | Best practice | `duplicate_frame_count() == 0` | **T3** |
