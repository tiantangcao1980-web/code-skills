# PerryTS/perry

- **URL**: https://github.com/PerryTS/perry
- **Stars**: 2k+
- **License**: 见原仓库
- **类型**: TypeScript 原生编译器(Rust + SWC + LLVM)

## 这是什么

把 TypeScript 直接编译为**原生可执行文件**,不要 Node.js / Electron / 浏览器引擎。输出单个二进制,跨 macOS / Windows / Linux / iOS / tvOS / Android / Web。生态里已经有真实项目在用(Bloom Engine 游戏引擎、Mango MongoDB GUI、Hone 编辑器、dB Meter)。

## 在 code-skills 中的对应

- **不做成 skill** —— Perry 是构建工具,不是开发模式 / 设计模式
- **被引用的位置**:
  - `cli-design` skill 的"分发包装"步骤,可把 TS 写的 CLI 用 Perry 打包成原生二进制(替代 pkg / nexe / bun build)
  - `design-dev-flow` ⑦ 交付幕,如果项目要发原生应用,Perry 是 Electron 的轻量替代

## 何时用

- 写 TS 但要发原生 app(macOS/iOS/Android)
- 不想给桌面工具背 Electron 几百 MB 的包
- CLI 工具要发布单二进制(替代 pkg / Bun build)
- 跨平台原生 app,只想维护一份 TS 代码

## 何时**不**用

- 项目大量依赖 npm 包的运行时反射 / eval(可能编译不过)
- 重度依赖 Node 内置模块的服务端代码(Perry 的覆盖在演进中)
- 已在 Tauri / Wails 上跑得好(没必要切)

## 怎么用

```bash
# 安装(看上游 README 最新方式)
brew install perryts/tap/perry   # 假设有 tap;以 perryts.com 为准

perry compile src/main.ts -o myapp
./myapp                            # 单个原生二进制
```

## 不集成的部分

- 不把 Perry 包装为本仓库的 CLI 子命令(它是构建工具,场景太具体,passthrough 价值低)
- 不在本仓库提供 Perry 项目模板(用 Perry 自己的 starter 即可)
- 不做"该用 Perry / Tauri / Bun / Electron" 决策树(那是构建工具选型 skill 的事 —— 后续可加)
