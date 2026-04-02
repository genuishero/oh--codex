# Codex Profile 速查

默认不手动切时，主会话按全局配置运行：

- 模型：`gpt-5.4`
- 推理强度：`high`

## 推荐 profile

- `inspect`
  用于查代码、看调用链、找定义、做只读定位。
  倾向更快返回，适合“先看清楚再说”。

- `bug`
  用于排查 bug、报错、白屏、测试失败、构建失败。
  适合先定位根因，再做修复。

- `frontend`
  用于页面、组件、样式、布局、交互、响应式和视觉调整。
  保持较强推理，同时打开 `view_image`。

- `docs`
  用于看官方文档、最新版本、兼容性、API 参数和模型选择。
  开启 `live` web search，适合时效性问题。

- `review`
  用于 code review、回归检查、安全边界和测试覆盖检查。
  以发现风险为主。

- `deep`
  用于复杂架构、跨文件重构、难问题分析和高风险决策。
  是最重的一档。

- `fast`
  用于轻量提问、快速处理、小范围读写和简单任务。
  速度优先。

## 什么时候切

- “先帮我找一下这个链路” -> `inspect`
- “这里白屏 / 报错 / 不生效” -> `bug`
- “帮我改页面和交互” -> `frontend`
- “查官方最新文档” -> `docs`
- “帮我 review 这次改动” -> `review`
- “这个改动比较大，先深挖一下” -> `deep`
- “这个很简单，快速处理” -> `fast`

## CLI 用法

```bash
codex -p inspect
codex -p bug
codex -p frontend
codex -p docs
codex -p review
codex -p deep
codex -p fast
```

## 说明

- profile 是“会话档位”，不是每条消息自动热切顶层模型。
- 自动分流仍然主要依赖 `AGENTS.md`、skills、subagents 和 review/docs 路径。
- 这套仓库带了模型提示 hook，启动会话或模型变化时会显示当前模型。
