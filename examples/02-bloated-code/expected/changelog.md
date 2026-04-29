# Changelog · 02-bloated-code(参考精简清单)

每条改动标 P 级别 + 一句话理由,对照 `code-simplifier` skill 的 P0/P1/P2 清单。

## P0(几乎一定要做)

| # | 改动 | 理由 |
|---|------|------|
| 1 | 删 `import os` / `import sys` | 未使用导入 |
| 2 | 删 `if False:` 死分支 | 永不可达 |
| 3 | 删 tombstone comment(legacy_compat) | 引用已不存在代码的注释 |
| 4 | 删 `legacy_log()` 函数 | 死函数,无调用方 |
| 5 | 抽 `_announce(name, fn, a, b)` 替代三处 announce_* 重复 | 3 次重复结构相同 |

## P1(大概率要做)

| # | 改动 | 理由 |
|---|------|------|
| 6 | 删 `_AbstractCalc` 类 | 单实现 interface,无 mock 需求 |
| 7 | 删 `add_wrapper()` | 空壳包装,只 forward |
| 8 | 删 `add/sub/mul` 内部 isinstance 校验 | internal helper 的过度防御(调用方已保证) |
| 9 | 删 `safe_div(unused_param)` 参数 | 墓碑参数,无人使用 |

## P2(谨慎判断 — 这次做了)

| # | 改动 | 理由 |
|---|------|------|
| 10 | `safe_div` 嵌套 if → 单层 guard | 可读性提升明显 |
| 11 | `is_valid` 复杂布尔 → 多个 guard | 单层条件 + 提前 return |

## 红线遵守(必须满足)

- ✅ 不引入新功能
- ✅ 行为不变(`test_calculator.py` 在 before/expected 都通过)
- ✅ 不删测试
- ✅ 不动公共 API(add/sub/mul/safe_div/is_valid/announce_* 全保留)

## 行数统计

- before: 95 行
- expected: 50 行
- **精简率: 47%**(目标 ≥30%,达成)

## 没做的(列出来,理由要写)

- 没合并 `announce_add/sub/mul` 为单一 `announce(op, a, b)`(三个独立函数是稳定 API,合并会破坏调用方)
