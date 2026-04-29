# Ralph Loop 契约示例(参考样本)

> 给 agent 看的"如果你被这个 example 触发,该写出什么样的契约"

```
【Ralph Loop 契约】
目标: examples/04-ralph-bugfix/before/parser.py 通过 test_parser.py 全部 5 个用例
退出条件: cd before && pytest -q test_parser.py 退出码 = 0
单步耗时上限: 5 分钟
最大迭代数: 4
卡住判定: 连续 2 轮失败用例集合不变
验证手段: cd examples/04-ralph-bugfix/before && pytest -q test_parser.py
```

## 期望迭代轨迹(参考)

### Iteration 1

```
🔁 Iter 1/4
PLAN: 跑一次基线测试,看哪些 case 失败
EXECUTE: pytest -q test_parser.py
VERIFY: 3 fail / 2 pass
        - test_no_scheme_defaults_to_https: ValueError: not enough values
        - test_query_with_equals_in_value: AssertionError
        - test_fragment_stripped_from_path: AssertionError
DECIDE: 🔁 CONTINUE
NEXT: 修 BUG-1(无 scheme 处理),先收一个简单的
```

### Iteration 2

```
🔁 Iter 2/4
PLAN: 给 parse_url 加 "if '://' in url" 分支
EXECUTE: 改 parser.py
VERIFY: 2 fail / 3 pass
        - test_query_with_equals_in_value 仍 fail
        - test_fragment_stripped_from_path 仍 fail
DECIDE: 🔁 CONTINUE (1→3 通过,有进展)
NEXT: 一起修 BUG-2(query split)+ BUG-3(fragment),它们互不相关
```

### Iteration 3

```
🔁 Iter 3/4
PLAN: BUG-2 用 partition 替代 split;BUG-3 在解析前先抽出 fragment
EXECUTE: 改 parser.py 两处
VERIFY: 0 fail / 5 pass ✅
DECIDE: ✅ DONE
```

### 退出报告

```
【Ralph Loop 退出报告】
退出原因: DONE
实际迭代轮数: 3 / 4
最终验证: 5/5 pass
改动文件: examples/04-ralph-bugfix/before/parser.py
遗留问题: 无
建议下一步: 跑 code-simplifier 看 fix 后是否有冗余可删
```

## 反模式(不要这样)

- ❌ 一次试图修 3 个 bug(改大了不知道是谁修好的)
- ❌ 改 test_parser.py 让它过(红线违反)
- ❌ catch Exception 吞错让验证假过
- ❌ DECIDE 写"差不多了"(必须三选一)
- ❌ 不写 NEXT 就 CONTINUE(下一轮没方向 = 在赌)
