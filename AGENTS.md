# Global Codex Guide

## Language

- Always respond in Chinese-simplified unless the user explicitly asks for another language.

## Default Posture

- Classify each request first: `locate`, `docs`, `debug`, `explain`, `plan`, `implement`, or `review`.
- Prefer direct work over meta discussion.
- Ask only when the next step is destructive, irreversible, or blocked by a real ambiguity.
- Keep outputs concise, concrete, and evidence-based.
- When the request can fit multiple categories, use this order:
  `docs` over memory, `debug` over blind edits when there is an error or failing behavior, `locate` before `implement` when the code path is unclear, `review` after meaningful changes.

## Routing

- `locate`: when the user asks where code lives, who calls something, which files are involved, how a flow connects, or wants a quick read-only lookup.
  Common triggers: `在哪`, `谁调用`, `哪里定义`, `哪些文件`, `调用链`, `入口`, `出口`, `链路`, `trace`, `引用`, `搜索`.
  Use the `repo-locate` skill when it matches.
- `docs`: when the user asks for latest behavior, official guidance, API parameters, compatibility, versions, model choice, framework usage, or anything that may have changed recently.
  Common triggers: `官方`, `文档`, `最新`, `兼容`, `版本`, `参数`, `API`, `model`, `OpenAI`, `Codex`, `React`, `Vue`, `Next.js`.
  Use the `official-docs-check` skill when it matches.
  Prefer `docs_researcher` for isolated documentation lookup.
- `plan`: when the user asks for a plan, approach, tradeoffs, breakdown, risks, or says not to code yet.
  Common triggers: `先分析`, `先别写`, `方案`, `路线`, `拆解`, `怎么做`, `利弊`, `风险`.
  Use the `plan-first` skill when it matches.
- `debug`: when the user reports an error, failing test, crash, white screen, unexpected behavior, broken build, or says something does not work.
  Common triggers: `报错`, `报异常`, `不生效`, `白屏`, `挂了`, `失败`, `编译不过`, `测试挂了`, `为什么没反应`, `定位问题`.
  Use the `debug-first` skill when it matches.
  Map the failing path before editing. If the root cause is localized and small, `small_fixer` is allowed.
- `implement`: when the user asks to implement, fix, refactor, add, remove, rename, or update code/config/scripts.
  Common triggers: `实现`, `修复`, `重构`, `补测试`, `改一下`, `加一个`, `删掉`, `替换`, `迁移`.
  Use the `ship-changes` skill when it matches.
  If the issue is already understood, the scope is narrow, and the change should stay within about `1-3` files without new dependencies or schema changes, prefer `small_fixer`.
- `review`: when the user asks for code review, regression checking, risk analysis, security review, or missing-test review.
  Common triggers: `review`, `帮我看下`, `有没有问题`, `风险`, `回归`, `安全`, `测试够吗`.
  Use the `review-risks` skill when it matches.

## Domain Shortcuts

- When the request is about generic frontend UI work such as `页面`, `组件`, `样式`, `布局`, `响应式`, `交互`, `动效`, or `视觉`, prefer the `frontend-delivery` skill unless a more specific domain skill already matches.

## Editing Rules

- Inspect existing code before editing.
- Match existing patterns before adding new abstractions.
- Keep diffs small and reversible.
- Do not add new dependencies without explicit request.
- If a task is clearly implementation-oriented, do the work instead of stopping at a plan.

## Verification

- For code changes, run the most relevant diagnostics, tests, or build checks before claiming completion.
- For reviews, lead with concrete findings and file references.
- For lookups, return the direct answer first, then the smallest useful set of supporting file paths.
- For documentation-heavy answers, separate verified facts from local assumptions and cite the official source when available.

## Subagents

- Subagents are for explicitly requested parallel work or clearly bounded high-value splits.
- Prefer these custom agents when their role is a good fit:
  - `repo_mapper`: read-only code mapping and path tracing
  - `reviewer`: correctness, regression, and security review
  - `docs_researcher`: official docs verification through MCP
  - `small_fixer`: narrow, implementation-focused follow-up fixes
- Keep the main session in charge when the task is cross-file, ambiguous, architecture-heavy, or likely to change direction during execution.
- Do not spawn subagents for trivial work.

## Model Guidance

- Use the main session with `gpt-5.4` for broad reasoning, architecture, ambiguous debugging, risky refactors, reviews with non-obvious tradeoffs, and final synthesis.
- Use `repo_mapper` or `docs_researcher` on `gpt-5.4-mini` for read-heavy lookup, path tracing, and isolated documentation verification.
- Use `small_fixer` on `gpt-5.4-mini` only after the issue is already localized and the likely fix is straightforward.
- Use `reviewer` on `gpt-5.4` when the primary goal is finding bugs, regressions, unsafe edge cases, or missing tests.
