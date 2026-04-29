# Example 04 · Ralph Loop Bugfix

> 测试:`ralph-loop` skill 的 PLAN/EXEC/VERIFY/DECIDE 模式能不能从一个**已知坏**的代码 + 失败测试,迭代到全过。

## 测什么

1. **能写出循环契约**(目标 / 退出条件 / 最大迭代数 / 验证手段)
2. **每轮报告**包含 PLAN/EXECUTE/VERIFY/DECIDE 四段
3. **DECIDE 三选一**(DONE / CONTINUE / ABORT)
4. **最终退出**:`pytest` 全过 → DONE

## 输入(故意 bug 的代码)

`before/parser.py` 是一个 URL 解析函数,有 **3 个 bug**:
1. 不处理无 scheme 的 URL(`example.com/foo` → 报 `IndexError`)
2. query string 解析丢了第一个 `=`(`?a=1` → `{"a": "1=1"}`)
3. fragment 没去掉(`#top` 留在 path 里)

`before/test_parser.py` 写了 5 个 case,**4 个失败**(3 个针对单 bug 的 case + 1 个综合 `test_full` 命中所有 bug)。

## 期望:agent 跑完 ralph-loop 后

1. 输出循环契约(在 `expected/contract.md` 里给参考样本)
2. 经历 2-4 轮迭代,每轮都有完整四段报告
3. 修好 `parser.py` → 5/5 测试过
4. 输出退出报告(改了哪些文件、迭代轮数、遗留)

`expected/parser.py` 是参考修复版本。

## 怎么跑

```bash
examples/04-ralph-bugfix/run.sh
```

会:
1. 跑 `before/test_parser.py`(应该 3 fail / 2 pass)
2. 跑 `expected/test_parser.py`(应该 5/5 pass)
3. 检查 `expected/contract.md` 是否有循环契约 4 个必填字段

## 触发 prompt(给 agent / 用户演练)

```
触发 ralph-loop skill。

目标: examples/04-ralph-bugfix/before/parser.py 必须通过 test_parser.py 全部 5 个用例
退出条件: pytest test_parser.py 退出码 = 0
最大迭代数: 4
卡住判定: 连续 2 轮失败用例集合不变
验证手段: cd before && pytest -q test_parser.py

红线:
  - 不能改 test_parser.py(那是验证手段)
  - 不能 catch 全局 except 来吞错
```

## 验证准则

- ✅ before/test_parser.py 跑出 4 fail 1 pass(确认 bug 真存在)
- ✅ expected/test_parser.py 跑出 5 pass(确认参考版本对)
- ✅ expected/contract.md 含目标/退出条件/最大迭代数/验证手段
- ❌ 任一项不满足 → fail
