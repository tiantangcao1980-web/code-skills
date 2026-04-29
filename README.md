# code-skills · 综合开发与设计技能套件

> **15 个** Claude Code Skill(含 1 个**端到端自动驱动器** `auto-flow` + 9 幕全流程覆盖)
> **+ 2 个嵌入式 Plugin**(ralph-loop / code-simplifier · Anthropic 官方 verbatim)
> **+ 19 个 vendored Cowork 领域插件 / 67 个 skill**(legal / finance / pm / data / marketing / sales / ...,可一键激活)
> **+ 一套对齐 opencli/CLI-Anything 的 CLI**(13 个命令)
> **+ 13 份外部集成档案**
>
> **一句话目标**:**用户提需求 → 自动跑完 9 幕到交付**,只在 6 个预设节点打扰用户。

[![CI](https://github.com/tiantangcao1980-web/code-skills/actions/workflows/ci.yml/badge.svg)](https://github.com/tiantangcao1980-web/code-skills/actions/workflows/ci.yml)

## 15 个 Skill(覆盖 9 幕全流程 + 工具)

### 编排 / 机制层(4 个)
| Skill | 类型 | 一句话 |
|-------|------|--------|
| `auto-flow` ⭐ | 驱动器 | 用户提需求 → Phase 0 gate → 9 幕自动跑到交付,Ralph(≤20 轮)+ Simplifier 配合 |
| `design-dev-flow` | 蓝图 | 9 幕声明式流程(`auto-flow` 是它的引擎) |
| `ralph-loop` 📦 | 循环引擎 | Stop-hook 强制循环,默认 ≤20 轮 + 早停 + 卡住保护 + 续轮申请书 |
| `code-simplifier` 📦 | 质量 | P0/P1/P2 清单式精简,等价行为前提下删冗余 |

### 上游(① 调研 → ② 分析 → ③ 产品)新增
| Skill | 幕 | 一句话 |
|-------|---|--------|
| `user-research` ⭐新 | ① | 桌面 + 竞品 + 5 人深访 + 问卷,产出 research-report |
| `requirement-analysis` ⭐新 | ② | JTBD + User Story + 用户旅程 + MoSCoW + RICE 双视图 |
| `product-spec` ⭐新 | ③ | 11 章 PRD + MVP 切片 + NSM + 风险登记 + 上线/回滚 |

### 中游(④ 设计 → ⑤ 接口)
| Skill | 幕 | 一句话 |
|-------|---|--------|
| `design-templates` | ④ | DESIGN.md + design-tokens.json 模板 |
| `copywriting-design` | ④ | 4 维度语气 + 5 句关键文案 + 禁用词清单 |
| `cli-design` | ⑤ | opencli + CLI-Anything 7 铁律 + 5 步法 |

### 下游(⑧ 测试 → ⑨ 交付)
| Skill | 幕 | 一句话 |
|-------|---|--------|
| `qa-strategy` ⭐新 | ⑧ | 测试金字塔编排 + Quality Gate + 缺陷管理 |
| `browser-automation` | ⑧ | LLM 探索 → Playwright 固化的混合 E2E |
| `programmatic-video` | ⑨ | Remotion 写视频,30-60s demo 标准结构 |

### 工具型(任一幕可调)
| Skill | 类型 | 一句话 |
|-------|------|--------|
| `file-curation` ⭐新 | 工具 | 一堆文件 → 分类 → 摘要 → 索引 → 沉淀 4 步法 |
| `claude-code-resources` | 资源 | Claude Code 生态导航,3 个推荐封顶 |

## 2 个嵌入式 Plugin(Anthropic 官方,Apache-2.0)

| Plugin | 作用 |
|--------|------|
| `ralph-loop/plugin/` | Stop hook + `/ralph-loop` 命令,在会话内强制循环 |
| `code-simplifier/plugin/` | Anthropic 官方 simplifier agent,可被 `Agent(subagent_type="code-simplifier")` 调用 |

verbatim 嵌入,未修改源文件。完整 attribution 见仓库根 `NOTICE`。

## 🆕 19 个 vendored Cowork 领域插件(67 个 skill 可立即激活)

> 把 Anthropic Cowork(Claude Desktop)的领域专家插件 **真实 vendor 进仓库** —— 无需装 Cowork 本身,git clone 即可用。

| Plugin | Skills | License | 域 |
|--------|--------|---------|---|
| `legal` | 6 | Apache-2.0 (Anthropic) | 合同审查 / NDA / 风险评估 / GDPR/CCPA / 法律邮件 |
| `finance` | 6 | Apache-2.0 (Anthropic) | 三表 / 凭证 / 调节 / 方差 / 月结 / SOX 审计 |
| `product-management` | 6 | Apache-2.0 (Anthropic) | feature-spec / roadmap / metrics / user-research-synthesis |
| `data` | 7 | Apache-2.0 (Anthropic) | SQL / 统计 / 可视化 / 仪表盘 / 数据探查 |
| `marketing` | 5 | Apache-2.0 (Anthropic) | brand-voice / campaign / 内容 / 竞品 / 性能分析 |
| `customer-support` | 5 | Apache-2.0 (Anthropic) | 工单分诊 / 升级 / 知识库 / 响应起草 |
| `sales` | 6 | Apache-2.0 (Anthropic) | 客户研究 / 通话准备 / 竞争情报 / 外联 |
| `enterprise-search` | 3 | Apache-2.0 (Anthropic) | 知识合成 / 搜索策略 / 来源管理 |
| `productivity` | 2 | Apache-2.0 (Anthropic) | 任务管理 / 记忆管理 |
| `bio-research` | 5 | Apache-2.0 (Anthropic) | 生物信息(scvi-tools / 单细胞 RNA / Nextflow) |
| `cowork-plugin-management` | 2 | Apache-2.0 (Anthropic) | 元 — 创建 / 定制 Cowork plugin |
| `apollo` | 3 | MIT (Apollo.io) | Apollo.io 销售工作流 |
| `brand-voice` | 3 | MIT (Tribe AI) | 品牌语气发现 / 强制 / 指南生成 |
| `common-room` | 6 | Apache-2.0 (Common Room) | GTM Copilot |
| `slack-by-salesforce` | 2 | MIT (Salesforce) | Slack 集成 |
| 4 个 placeholder | - | (no LICENSE) | design / engineering / human-resources / operations(法律保守不分发) |

**一键激活**:
```bash
bin/code-skills vendor install legal      # 6 个法律 skill 进 ~/.claude/plugins/
bin/code-skills vendor install --all-vendored   # 一次装全 15 个完整 vendor
```

**升级反馈流程**:vendor 改 → PR 上游 → `vendor sync` 拉回。完整 attribution 见 [`vendor/cowork/NOTICE`](vendor/cowork/NOTICE)。

## CLI 命令树(opencli-aligned)

```
code-skills
├── validate              [--json]                  校验 skill
├── install [--symlink|--copy] [--json]             装 skill
├── uninstall [--json]                              卸 skill 软链
├── list [--json]                                   列 skill(📦 标记含 plugin)
├── doctor [--json]                                 检测外部工具
├── describe [--json]                               输出 CLI schema(机器可发现)
├── version [--json]                                显示版本
├── plugin
│   ├── list [--json]
│   ├── status [<name>] [--json]
│   ├── install <name|--all> [--copy] [--json]
│   └── uninstall <name|--all> [--json]
├── demo                                            Remotion passthrough
│   ├── init <project>
│   ├── render <id> [<file>]
│   └── studio
├── browser                                         browser-use passthrough
│   ├── run <task>
│   ├── version
│   └── doctor
├── cli-init <name> [--lang python] [--force]       Scaffold opencli-aligned CLI
├── vendor                                          管理 19 个 Cowork 领域插件
│   ├── list [--json]                               19 plugin / 67 skill 清单
│   ├── status [<plugin>] [--json]                  激活状态
│   ├── install <plugin|--all-vendored> [--copy]    装到 ~/.claude/plugins/code-skills-vendor/
│   ├── uninstall <plugin>
│   ├── diff [--json]                               对比 vendor vs 上游 Cowork cache
│   └── sync [--dry-run] [--json]                   从上游同步更新
└── help [<command>]
```

**通用 flag**(每个子命令都支持):`--help/-h --json --quiet/-q --verbose/-v --no-color --dry-run --yes/-y`

**退出码**:`0` 成功 / `1` 运行时错 / `2` 用法错 / `3` 缺依赖 / `130` 中断

**错误码**(JSON 模式):`USAGE_ERROR / VALIDATION_FAILED / TARGET_EXISTS / NOT_INSTALLED / DEPENDENCY_MISSING / NOT_FOUND / INTERNAL_ERROR`

## 端到端自动化(auto-flow)

> **用户只提一句需求 → 系统自动跑到交付**。

### 流程图(9 幕)

```
   ┌────────────────────────────────────┐
   │ Phase 0 · 需求 Gate(必过)         │
   │   11 项必填,任一缺失 → 回问用户    │
   │   4 项可行性,任一冲突 → 报告改方向 │
   │   ↓ 全齐 + 用户明确 OK             │
   └────────────────────────────────────┘
                  │
   ① 调研 → ② 分析 → ③ PRD → ④ 设计 → ⑤ 接口 → ⑥ 前端 → ⑦ 后端 → ⑧ 测试 → ⑨ 交付
   user-     req-      product-   design-   cli-/       Ralph     Ralph    qa-       Cowork
   research  analysis  spec       templates  api-       +simp     +simp    strategy  pptx/docx
             +spec     +spec      +copy      design     (P0)      (P0)               +simp 全量
             workflow  workflow   writing                                             +deploy
                                                                                      +demo
```

### 用户被打扰的**仅 6 种**情形

| # | 触发点 |
|---|-------|
| 1 | 需求不完整(列缺失项 + 样板问句) |
| 2 | Ralph 满 20 轮未 DONE → 续轮申请书 |
| 3 | Ralph 连续 3 轮 VERIFY 不变 → 卡住报告 |
| 4 | 涉及付费(域名 / CDN / API key) |
| 5 | 涉及破坏性操作(删数据库 / 生产) |
| 6 | ⑧ 测试 Quality Gate 含 ❌ |

其余时间静默执行。详见 [`auto-flow/SKILL.md`](auto-flow/SKILL.md)。

## 快速上手

```bash
# 1. 校验仓库结构
bin/code-skills validate

# 2. 把 9 个 skill 装到 ~/.claude/skills/(软链)
bin/code-skills install

# 3. (可选)装嵌入式 plugin,激活 Stop-hook 真实循环 + agent 调用
bin/code-skills plugin install --all

# 4. 检测外部工具
bin/code-skills doctor

# 5. 让其它 agent 发现本 CLI 能力(opencli schema)
bin/code-skills describe --json | jq '.commands[].name'

# 6. Scaffold 一个新的 opencli-aligned CLI
bin/code-skills cli-init my-tool

# 7. 程序化视频 demo
bin/code-skills demo init my-demo

# 8. LLM 浏览器自动化任务
bin/code-skills browser run "find a repo and star it"
```

## 仓库结构

```
code-skills/
├── README.md / NOTICE
├── bin/code-skills                        # CLI 入口
├── scripts/                               # 12 个子命令实现 + 共享库
│   ├── _lib.py                            # JSON 输出 / 错误格式 / discover_skills
│   ├── validate.py / install.py / list_skills.py
│   ├── doctor.py / describe.py / plugin.py
│   ├── demo.py / browser.py / cli_init.py
├── ralph-loop/                            # ⭐ skill + 嵌入 Anthropic plugin
├── code-simplifier/                       # ⭐ skill + 嵌入 Anthropic plugin
├── design-dev-flow/                       # 9 幕蓝图
├── auto-flow/                             # ⭐ 9 幕驱动器
├── user-research/ requirement-analysis/   # 上游(① ② 幕)
├── product-spec/                          # 上游(③ 幕)
├── cli-design/ claude-code-resources/
├── browser-automation/ programmatic-video/
├── copywriting-design/ design-templates/
├── qa-strategy/ file-curation/            # 测试 + 工具
├── vendor/                                # ⭐ Cowork 19 plugin / 67 skill verbatim
│   └── cowork/
│       ├── NOTICE / README.md / VERSIONS.lock
│       ├── legal/ finance/ data/ ...      # 15 个完整 vendored
│       └── design/ engineering/ ...       # 4 个 placeholder
├── integrations/                          # 13 份外部 / Cowork 集成档案
│   ├── README.md
│   ├── opencli.md / cli-anything.md
│   ├── browser-use.md / agent-browser.md
│   ├── remotion.md
│   ├── huashu-design.md / awesome-design-md.md
│   ├── everything-claude-code.md
│   ├── superpowers.md / taste-skill.md
│   └── perry.md
└── .github/workflows/ci.yml               # 自动跑 validate + schema 校验
```

## 集成的 11 个外部项目

| 项目 | 集成形式 |
|------|---------|
| opencli, CLI-Anything | → `cli-design` skill + 本 CLI 自身遵守 |
| browser-use, agent-browser | → `browser-automation` skill + `code-skills browser` |
| remotion | → `programmatic-video` skill + `code-skills demo` |
| huashu-design | → `copywriting-design` skill |
| awesome-design-md | → `design-templates` skill |
| everything-claude-code | → `claude-code-resources` skill |
| obra/superpowers | 已是 skill 形式,引用借鉴 |
| Leonxlnx/taste-skill | 已是 skill 形式,引用借鉴 |
| PerryTS/perry | 工具引用(TS 原生编译),不做单独 skill |

完整文档见 `integrations/`。

## 设计原则

1. **解耦** —— 9 个 skill / 2 个 plugin / 12 个 CLI 命令,各自能跑
2. **零依赖核心** —— CLI 只用 Python 3 标准库 + bash,**不引入第三方依赖**
3. **强退出条件** —— 任何循环/流程都必须能"明确说出何时停"
4. **opencli 对齐** —— 退出码 / 错误码 / `--json` schema 标准化,可被其它 agent 自动发现调用
5. **不重复造轮子** —— 已有 91 个 skill 能解决就直接调,不在本仓库复述
6. **passthrough 而非打包** —— 外部 CLI(remotion / browser-use)用 `which` 检测 + 转发,不强制安装

## Examples · 测试 skill 的能力与效果

`examples/` 下有 4 个独立 case,各带 `before` / `expected` / `run.sh` 自验脚本:

| # | 名字 | 测哪个 skill | 核心断言 |
|---|------|------------|---------|
| 01 | `todo-cli` | `cli-design` + `cli-init` | scaffold 出的 CLI 自身能输出合法 opencli schema |
| 02 | `bloated-code` | `code-simplifier` | 识别 P0/P1/P2 共 11 种问题 + 删 ≥30% 行 + 行为不变 |
| 03 | `landing-page` | `design-templates` + `copywriting-design` | 产 DESIGN.md + tokens.json + 5 句无禁用词文案 + 可渲染 HTML |
| 04 | `ralph-bugfix` | `ralph-loop` | 写出循环契约 + PLAN/EXEC/VERIFY/DECIDE 4 段 + 修到 5/5 pytest 过 |

```bash
examples/run-all.sh    # 跑全部 22 项子检查
```

## CI

`.github/workflows/ci.yml` 在每次 push/PR 跑:
- `validate` 校验 9 个 skill 结构
- `validate --json` 校验 JSON 输出合法
- `describe --json` 校验 opencli schema 形状(必填字段、命令数、子字段)
- `list --json`
- `doctor`(informational)
- `cli-init` 烟雾测试 + scaffold 出的 CLI 自我 describe 检查
- `examples/run-all.sh` 4 个 example 全部子检查

## 许可

- 本仓库 skill 内容:MIT
- 嵌入式 plugin (`ralph-loop/plugin/`, `code-simplifier/plugin/`):Apache-2.0,见各自目录的 `LICENSE` 与根 `NOTICE`
- 借鉴/链接的外部项目:各自遵循其原 license
