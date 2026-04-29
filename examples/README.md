# Examples · 测试 code-skills 的能力与效果

> 4 个独立的测试 case,每个验证 1-3 个 skill 的**核心能力**,有 before / expected / 自验脚本。

## 索引

| # | 名字 | 测试的 skill | 核心断言 |
|---|------|------------|---------|
| 01 | [todo-cli](01-todo-cli/) | `cli-design` + `cli-init` | scaffold 出的 CLI 自身能输出合法 opencli schema |
| 02 | [bloated-code](02-bloated-code/) | `code-simplifier` | 能识别 12 种 P0/P1/P2 问题,删 ≥30% 行,行为不变 |
| 03 | [landing-page](03-landing-page/) | `design-templates` + `copywriting-design` | 产出合法 DESIGN.md + design-tokens.json + 5 句无禁用词文案 |
| 04 | [ralph-bugfix](04-ralph-bugfix/) | `ralph-loop` | 走完 PLAN/EXEC/VERIFY/DECIDE 直到 pytest 全过 |
| 05 | [auto-flow-gate](05-auto-flow-gate/) | `auto-flow` | Phase 0 11 项 + 4 项可行性 + 6 个干预点全部声明,且 3 份输入分级触发 |

## 一键跑全部

```bash
examples/run-all.sh
```

会:
1. 跑 example 01 的 cli-init scaffold + describe 校验
2. 跑 example 02 的 simplifier 自检(对比 before / expected 行数)
3. 跑 example 03 的 DESIGN.md 章节校验 + 文案禁用词扫描
4. 跑 example 04 的 pytest(应失败)+ 演示循环契约

输出:每个 example 一行 ✅/❌,最后总览。

## 怎么解读结果

- **✅** = skill 的**机制**能跑,产出符合规范
- **效果**(产出物的"好不好")需要人眼判断,我们在每个例子的 expected/ 里给了一份**参考答案**,你可以对比

## 不在 examples 里的 skill

| Skill | 为什么不做独立 example |
|-------|----------------------|
| `design-dev-flow` | 它是 7 个其他 skill 的**编排器**,无独立产出 → 跑 01-04 就是它的 demo |
| `claude-code-resources` | 查询型 skill,无文件产出 → 见 `integrations/everything-claude-code.md` 的 Q&A 示例 |
| `browser-automation` | 需要真实浏览器 + Playwright + 网络,放进 examples 会让 CI 不稳 → 见 SKILL.md 的脚本示例 |
| `programmatic-video` | 需要 Node + remotion 渲染 → 见 `integrations/remotion.md` 的命令示例 |

这 4 个 skill 的"能力"已在 SKILL.md 里给出可执行示例,不为了凑数做空壳 example。
