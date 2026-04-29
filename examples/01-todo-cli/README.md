# Example 01 · TODO CLI(cli-design + cli-init 自我闭环)

> 测试:`cli-design` skill 的"7 铁律"是否真的可被本 CLI 自己 scaffold 落地。

## 测什么

1. **scaffold 出的 CLI 默认就符合 opencli 规范**(不靠后期修补)
2. **scaffold 出的 CLI 自身的 `describe --json` 输出合法 schema**
3. **scaffold 模板覆盖必备 7 项**:bin 入口、describe、version、help、退出码、JSON schema、INTERFACE.md

## 怎么跑

```bash
# 在仓库根目录运行
examples/01-todo-cli/run.sh
```

会做:
1. 删除 `examples/01-todo-cli/scaffold/`(若存在)
2. 用 `bin/code-skills cli-init` 在该目录生成新 CLI
3. 跑 `describe --json` 校验 schema 合法
4. 跑 `help`、`version` 检查命令存在
5. 列出 INTERFACE.md / README.md 是否齐全

## 期望输出

```
[ OK ] scaffold created
[ OK ] describe --json: opencli=0.1, name=todo-cli, commands>=2
[ OK ] help works
[ OK ] version works
[ OK ] INTERFACE.md exists with command tree
[ OK ] README.md exists

ALL PASS
```

## 期望产出物结构

```
scaffold/
├── README.md                # CLI 项目说明
├── INTERFACE.md             # opencli 命令树 + 退出码 + 错误码
├── bin/todo-cli             # bash 调度器
└── scripts/
    ├── _lib.py
    ├── describe.py          # 输出 opencli schema
    └── version.py
```

## 后续手动扩展(让用户演练 cli-design)

scaffold 后,可以触发 `cli-design` skill,让它给 todo-cli 设计 add/list/done 子命令:
- 命令树
- flag 表
- 退出码细分
- 错误码

然后实现 `scripts/add.py` / `scripts/list.py` / `scripts/done.py` 并连接到 `bin/todo-cli`。这部分是**给人/agent 演练用**的,不在自动测试里。

## 验证准则

- ✅ scaffold 不报错
- ✅ describe --json 顶层有 opencli/name/version/commands/common_flags/exit_codes
- ✅ help 显示 USAGE / COMMANDS / EXIT CODES 三段
- ❌ 任一项缺失 → 测试失败 + 打印缺什么
