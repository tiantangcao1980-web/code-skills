# Integrations · 外部项目集成索引

本目录用一致的精简模板,记录每个被本仓库借鉴/吸纳的外部项目:**这是什么、对应到哪个 skill、何时用、怎么用、什么不集成**。

## 完整索引

| 项目 | 类型 | 对应 skill / 集成形式 |
|------|------|----------------------|
| [opencli](opencli.md) | CLI 规范 | → `cli-design` skill;本 CLI 自身也对齐 |
| [CLI-Anything](cli-anything.md) | CLI 方法论 | → `cli-design` skill 的 5 步法 |
| [browser-use](browser-use.md) | Python LLM 浏览器自动化 | → `browser-automation` skill;`code-skills browser` 命令 passthrough |
| [agent-browser](agent-browser.md) | Vercel agent + 浏览器 | → `browser-automation` skill 的 serverless 模式 |
| [remotion](remotion.md) | 程序化视频 | → `programmatic-video` skill;`code-skills demo` 命令 passthrough |
| [huashu-design](huashu-design.md) | 文案话术设计 | → `copywriting-design` skill |
| [awesome-design-md](awesome-design-md.md) | 设计规范模板 | → `design-templates` skill |
| [everything-claude-code](everything-claude-code.md) | Claude Code 资源汇总 | → `claude-code-resources` skill |
| [obra/superpowers](superpowers.md) | Skill 集合 | 引用(已是 skill 形式,不重做) |
| [Leonxlnx/taste-skill](taste-skill.md) | 审美品味 skill | 引用(已是 skill 形式) |
| [PerryTS/perry](perry.md) | TS 原生编译器(Rust) | 工具引用,不做成 skill |

## 模板字段

每份文档统一包含:
- **URL / License / Stars** —— 一行可见的元数据
- **这是什么** —— 2-3 句
- **在 code-skills 中的对应** —— skill 名 + 借鉴的具体点
- **何时用** —— 决定调用的场景
- **怎么用** —— 最短可运行示例
- **不集成的部分** —— 显式声明本仓库**不**做哪些,避免误用

## 与 references/ 的区别

- `<skill>/references/*.md` —— skill **内部**的延伸阅读,被 SKILL.md 直接 link
- `integrations/*.md` —— **外部项目**的集成档案,提供项目背景与归属
