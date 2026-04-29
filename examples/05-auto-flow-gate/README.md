# Example 05 · Auto-Flow 需求 Gate

> 测试:`auto-flow` skill 的 Phase 0 需求 gate **真的会拦下不完整的需求**,不会偷偷开工。

## 测什么

1. 给 3 份**真实的用户输入**(逐个变完整),验证 gate 的反应是否分级正确:
   - **`inputs/01-vague.md`** —— 极度模糊(应触发 ≥7 项追问)
   - **`inputs/02-partial.md`** —— 部分信息(应触发 3-5 项追问)
   - **`inputs/03-complete.md`** —— 完整(应通过 gate,输出需求快照,等"OK")
2. 验证 `expected/` 下的样板输出格式(给 agent 看的"应该长这样")
3. 验证 6 个干预点都在 SKILL.md 里被声明

## 怎么跑

```bash
examples/05-auto-flow-gate/run.sh
```

会:
1. 检查 3 份输入是否齐全
2. 检查 expected/ 下 3 份对应输出是否齐全
3. 校验 expected/03-snapshot.md 含 11 个完整字段 + 4 个可行性字段
4. 校验 auto-flow/SKILL.md 声明了完整 11 项 + 6 个干预点

## 触发 prompt(给 agent 演练)

```
触发 auto-flow skill。

输入:
  cat examples/05-auto-flow-gate/inputs/01-vague.md
  → 期望:gate 拒绝,列出缺失项 + 样板问句

  cat examples/05-auto-flow-gate/inputs/02-partial.md
  → 期望:gate 拒绝,只追问缺失的 3-5 项

  cat examples/05-auto-flow-gate/inputs/03-complete.md
  → 期望:gate 通过,输出需求快照,等用户说 OK 才进 Phase 1
```

## 验证准则

- ✅ 3 份输入文件存在
- ✅ 3 份期望输出文件存在
- ✅ expected/03-snapshot.md 含 11 项 + 4 项可行性
- ✅ auto-flow/SKILL.md 声明完整 11 项 + 6 个干预点
- ❌ 任一项不满足 → fail
