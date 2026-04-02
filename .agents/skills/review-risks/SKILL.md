---
name: "review-risks"
description: "当用户要 review、查风险、看回归、安全边界、缺失测试或行为变化时使用。Use for risk-focused code review rather than implementation."
---

# Review Risks

Use this skill when the primary job is finding problems.

## What to do

1. Focus on correctness, regressions, unsafe edge cases, and missing tests.
2. Prefer concrete findings over summaries.
3. Use file references.
4. Keep style comments secondary unless they hide a real bug.

## Output shape

- Findings first
- Open questions or assumptions
- Small change summary only if needed
