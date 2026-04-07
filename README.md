# oh--codex

一套偏中文工作流的原生 Codex 配置模板，目标是让 Codex app / CLI 在不依赖外部大插件的前提下，具备更清晰的任务分流、模型分层、repo 级 skills、自定义 agents，以及可选的模型提示 hook。

这套配置适合这些场景：

- 想保留原生 Codex，不想长期依赖额外 orchestration 插件
- 希望用自然语言更稳定地落到 `查找 / 文档 / 调试 / 规划 / 实现 / 审查`
- 希望在 Codex app 里也能用 repo 级 `.codex`、`.agents/skills` 和 hooks
- 想把一套团队配置直接随仓库共享

## 平台支持

- macOS：完整支持这套仓库的 repo 配置、skills、agents 和模型提示 hook
- Windows：支持 repo 配置、skills、agents；hook 脚本与命令已按 Windows/macOS 兼容方式整理
- Windows 当前限制：截至 2026-04-08，Codex 官方 hooks 文档仍标注 `Windows support temporarily disabled`，所以 Windows 端目前无法依赖 Codex 运行时自动触发 hook

换句话说，这个仓库本身已经按 macOS / Windows 共享维护，但 Windows 上的 hook 是否真正触发，取决于 Codex 官方后续恢复该能力。

## 目录结构

```text
.
├── AGENTS.md
├── .codex
│   ├── config.toml
│   ├── PROFILES.zh.md
│   ├── hooks.json
│   ├── agents
│   │   ├── docs_researcher.toml
│   │   ├── repo_mapper.toml
│   │   ├── reviewer.toml
│   │   └── small_fixer.toml
│   └── hooks
│       └── model_notice.py
└── .agents
    └── skills
        ├── debug-first
        ├── frontend-delivery
        ├── official-docs-check
        ├── plan-first
        ├── repo-locate
        ├── review-risks
        └── ship-changes
```

## 默认思路

- 主会话默认模型：`gpt-5.4`
- 只读查找、文档校验、小范围修复：优先 `gpt-5.4-mini`
- 复杂 review、架构判断、高风险改动：优先 `gpt-5.4`
- 通过 `AGENTS.md` 和 skills 做任务分流
- 通过 custom agents 做窄职责子代理
- 通过 hooks 把当前模型提示出来

## 已内置的 profile

- `fast`
- `inspect`
- `bug`
- `frontend`
- `docs`
- `review`
- `deep`

详细说明见：[.codex/PROFILES.zh.md](./.codex/PROFILES.zh.md)

## 使用方式

### Codex app

1. 用 Codex app 打开这个仓库所在目录。
2. 确保使用的是包含这个仓库根目录的 local environment。
3. 修改配置后，重启 Codex app。

官方文档说明：

- Codex app 的 local environment 会读取项目根目录下的 `.codex` 配置
- repo 级 `.agents/skills` 会在 app、CLI、IDE 中生效
- hooks 需要先开启 `features.codex_hooks = true`
- repo 内置的 `model_notice.py` 使用仓库绝对路径调用，避免从子目录启动时找不到 hook

额外说明：

- macOS / Windows 都建议本机 `python` 指向 Python 3
- 如果你的 macOS 只有 `python3` 没有 `python`，给 `python` 补一个别名或软链即可

### CLI

```bash
codex -C /path/to/oh--codex
codex -C /path/to/oh--codex -p inspect
codex -C /path/to/oh--codex -p bug
codex -C /path/to/oh--codex -p docs
```

## 为什么有时看不到“模型切换提示”

这套仓库已经带了模型提示 hook，但要注意几个前提：

- hooks 是实验特性，需要在 `config.toml` 里打开 `codex_hooks = true`
- `systemMessage` 会显示在 UI 或 event stream 中，不一定是非常显眼的固定栏
- 当模型真的从 `A` 切到 `B` 时，macOS 会尝试系统通知并播放两次提示音；Windows 版本也带了兼容逻辑，但当前仍受 Codex 官方 Windows hooks 运行时限制
- profile 是“会话档位”，不是每条消息都自动热切顶层模型
- 如果你没有切 profile，也没有走到另一个子代理，模型通常不会变化

## 适合继续自定义的地方

- [AGENTS.md](./AGENTS.md)
  用来改自然语言触发词和整体工作流偏好
- [.codex/config.toml](./.codex/config.toml)
  用来改模型、reasoning、profile 和 hooks feature
- [.codex/agents](./.codex/agents)
  用来改子代理职责
- [.agents/skills](./.agents/skills)
  用来加 repo 级技能

## 参考

- [Codex local environments](https://developers.openai.com/codex/app/local-environments)
- [Codex hooks](https://developers.openai.com/codex/hooks)
- [Codex skills](https://developers.openai.com/codex/skills)
- [Codex subagents](https://developers.openai.com/codex/subagents)
- [Codex config reference](https://developers.openai.com/codex/config-reference)
