---
name: "repo-locate"
description: "当用户想快速定位代码时使用：某个函数、模块、接口、页面、命令、配置在哪里定义，谁在调用，哪些文件相关，或某条代码路径如何连接。Use for read-only repository lookup and code-path tracing."
---

# Repo Locate

Use this skill for read-only codebase lookup.

## What to do

1. Stay read-only.
2. Prefer fast local search first.
3. Answer the direct question first.
4. Include only the smallest useful set of files, symbols, and relationships.
5. If the task turns into planning or implementation, stop after mapping and hand control back.

## Output shape

- Direct answer
- Relevant files
- Short relationship note
- Optional next step
