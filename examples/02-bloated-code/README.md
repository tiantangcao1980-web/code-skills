# Example 02 · Bloated Code(code-simplifier 识别能力测试)

> 测试:`code-simplifier` skill 是否能识别 P0/P1/P2 三级共 12 种"虚胖"模式。

## 测什么

用一份**故意虚胖**的 Python 文件作为输入,触发 `code-simplifier` 后:
1. **行为不变**(同一组测试用例,精简前后都过)
2. **删除 ≥30% 行数**(虚胖代码 80 行 → 期望 < 56 行)
3. **每条改动有 P 级别 + 理由**

## 文件

- `before/calculator.py` —— **虚胖版**(80 行,含 12 种问题)
- `before/test_calculator.py` —— 行为基准测试(不改)
- `expected/calculator.py` —— 参考精简版(~50 行)
- `expected/changelog.md` —— 期望改动清单(每条标 P 级别)

## 怎么跑

```bash
examples/02-bloated-code/run.sh
```

会:
1. 跑 `before/test_calculator.py`(应该全过 —— 虚胖但功能对)
2. 把 `expected/calculator.py` 替换 before 跑同一组测试(应该仍全过)
3. 对比 before / expected 行数 + 字符数,打印精简率
4. 检查 expected/changelog.md 里每条改动是否有 P 级别标记

## 触发 simplifier 的 prompt(给 agent)

```
范围: examples/02-bloated-code/before/calculator.py
验证: 跑 before/test_calculator.py 必须全过
要求: 输出精简版 + changelog.md(每条改动标 P0/P1/P2 级别 + 一句话理由)
红线: 不引入新功能,不改公共 API,不动测试
```

期望 simplifier 至少识别出:
- P0:未使用的 import (`os`, `sys`)
- P0:未使用的导出函数 (`legacy_xxx`)
- P0:死代码分支 (`if False:`)
- P0:重复代码块(三处复制粘贴的 print 包装)
- P0:墓碑注释 (`# removed in v2`)
- P1:单实现 interface(`class _AbstractCalc`)
- P1:空壳包装函数 (`def add_wrapper(a, b): return add(a, b)`)
- P1:过度防御 (`if not isinstance(n, (int, float)):` 在 internal helper)
- P1:墓碑式参数 (`unused_param`)
- P2:嵌套 if 改卫语句
- P2:复杂布尔条件
- P2:`as any` 类型断言(N/A in Python,Python 版用 cast)

## 验证准则

- ✅ 测试 before / expected 都全过
- ✅ 行数减少 ≥30%
- ✅ changelog 至少 8 条 P 级别标记
- ❌ 任一项不满足 → fail
