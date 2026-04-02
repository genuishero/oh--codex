---
name: "debug-first"
description: "当用户说报错、异常、白屏、测试失败、构建失败、接口不对、功能不生效、或者需要定位根因时使用。Use for diagnosis-first work before editing."
---

# Debug First

Use this skill when the task is primarily about finding the real cause of a failure.

## What to do

1. Reconstruct the failing behavior from the user report, logs, stack traces, screenshots, or tests.
2. Identify the owning code path before changing anything.
3. Distinguish symptom, trigger, and root cause.
4. Only after the cause is credible, make the smallest correct fix.
5. Verify the exact failing behavior is resolved.

## Output shape

- Failure summary
- Likely root cause
- Relevant files or logs
- Fix and verification
