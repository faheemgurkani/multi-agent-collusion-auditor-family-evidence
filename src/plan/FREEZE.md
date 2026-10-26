# Freeze record (v1)

**Frozen at:** 2026-10-25T11:20:43Z (UTC), **before any agent run or auditor call** (no Colosseum output exists in this workspace at this time).

Any edit to a file below after this time must be recorded in [deviations.md](deviations.md) with a version bump (v2, …), and all affected auditing must be re-run.

| File | SHA-256 |
|---|---|
| `methodology.md` | `0f995fadbdec97b23f96e1aacde24ee6fc581421b1eb3cda0d6ecf668bb2cd8e` |
| `frozen/auditor_prompt_v1.md` | `f05316b962999e59c97c814aca3830ba5301427ffe2a53379659ebdf44587427` |
| `frozen/view_descriptions_v1.md` | `d3905f42ccec55e3da422caa49f7dad833a6af6add4ed179c74ef031b20d74f7` |
| `frozen/summarizer_prompt_v1.md` | `1a45a8cf1488250e7dee75351cdf7da66eb66a199101d9813d2f729ad944ca2e` |
| `frozen/recognition_probe_v1.md` | `ac924776cee0d1b2d63f882ccc9bdf666330c25c1c2361c665933bbd428184ae` |

Verify: `cd src/plan && shasum -a 256 methodology.md frozen/*.md`
