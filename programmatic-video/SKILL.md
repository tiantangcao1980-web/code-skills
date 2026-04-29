---
name: programmatic-video
description: |
  程序化视频 skill:用 React 组件写视频(Remotion),适合数据驱动 demo / 多语言版本 / CI 自动出片。
  也覆盖"什么时候用 Remotion vs 录屏 vs asciinema",和 30-60 秒 demo 的标准结构。
  触发词:「程序化视频」「自动生成 demo」「用代码做视频」「remotion」「demo 视频」「README gif」「项目演示视频」「product hunt 视频」。
  适用阶段:项目交付前做 demo、PR 描述附演示、ProductHunt / 黑客松提交、营销素材生成。
---

# Programmatic Video · 程序化视频

> 灵感:[remotion-dev/remotion](https://github.com/remotion-dev/remotion) —— Make videos programmatically with React。
> 核心心法:**别录屏剪 5 分钟,用代码生成 30 秒**。可重放、可参数化、可 CI 化。

## 三档选型

| 场景 | 工具 | 一句话 |
|------|------|-------|
| 个人项目快速 demo | QuickTime + iMovie | 5 分钟搞定 |
| 终端类项目 | asciinema → asciicast2gif | 体积小,可重放 |
| 数据驱动 / 多语言 / CI 出片 | Remotion | 写 React,渲染 mp4 |
| 商业精修 | ScreenStudio / Tella | 付费但快 |

**默认推荐**:80% 项目用 QuickTime;数据驱动场景上 Remotion。

---

## 30 秒 demo 标准结构

```
[0-3s]   钩子 — 一句话/一画面让观众停下
[3-10s]  问题 — 没这个产品时多痛
[10-22s] 解法 — 实际操作流程,3 步以内
[22-28s] 效果 — 直观展示成果(数据/对比/截图)
[28-30s] CTA — 网址 / 下载 / GitHub
```

总长不超过 60 秒。互联网上 50% 观众在 6 秒内跳走。

### 钩子的 5 种打开方式
1. **反差**:"以前 30 分钟,现在 30 秒"
2. **痛点提问**:"还在手写 SQL?"
3. **极端结果**:"我们用它做了一个 X"
4. **悬念**:"试试不写代码做这件事"
5. **数据**:"被复制了 1 万次"

---

## Remotion 最小可运行

```bash
npx create-video@latest my-demo
cd my-demo
npx remotion preview        # 浏览器预览
npx remotion render Main out.mp4
```

```tsx
// src/Demo.tsx
import { interpolate, useCurrentFrame } from 'remotion';

export const Demo = ({ title }: { title: string }) => {
  const frame = useCurrentFrame();
  const opacity = interpolate(frame, [0, 30], [0, 1]);
  return (
    <div style={{ flex: 1, background: '#0a0a0a', display: 'flex',
                  alignItems: 'center', justifyContent: 'center', opacity }}>
      <h1 style={{ color: 'white', fontSize: 80 }}>{title}</h1>
    </div>
  );
};
```

```tsx
// src/Root.tsx
import { Composition } from 'remotion';
import { Demo } from './Demo';
export const Root = () => (
  <Composition id="Demo" component={Demo} durationInFrames={150}
               fps={30} width={1920} height={1080}
               defaultProps={{ title: 'Hello' }} />
);
```

---

## 工作流

### 触发场景 A · 项目要做 demo
1. 选档(QuickTime / asciinema / Remotion)
2. 写 storyboard(每 3-5 秒一个场景)
3. 录或写
4. 剪到 30-60 秒
5. 加字幕(60% 观众静音看)
6. 导出 mp4 + gif(README 用)
7. 放进 `docs/demo/` 目录

### 触发场景 B · README 顶部要 hero gif
1. 用 Remotion 或 QuickTime 录 6-10 秒
2. 转 gif 控制 < 5MB(GitHub 限制)
3. 嵌入 README 顶部(在 H1 下,装饰性 badge 上)

### 触发场景 C · 多语言 / 多版本 demo
直接用 Remotion + 参数化 props,跑一次 render 全套出来。

---

## 输出物 / 文件命名

```
docs/demo/
├── hero.mp4
├── hero.gif
├── login.gif
├── feature-x.mp4
└── README.md   # 每个 demo 的复现说明
```

`docs/demo/README.md` 写明:工具、时长、数据源、复现命令。

---

## 反模式

- ❌ **录 5 分钟说"精剪"**:精剪几乎不会做,直接限时录
- ❌ **复杂转场**:观众看产品不看你的剪辑技巧
- ❌ **背景音乐**:版权风险,静音 + 字幕更安全
- ❌ **跟实际产品差异巨大**:被发现 = 信誉透支
- ❌ **没 CTA**:demo 看完不知道去哪,白录
- ❌ **gif 超 5MB**:GitHub README 显示不了

---

## 与其他 skill 的关系

- `design-dev-flow` ⑦ 交付幕的 demo 部分调本 skill
- `code-skills demo <subcmd>` CLI 命令是 Remotion 的 passthrough(见 README)

---

## References

- [Demo 录制详细工作流](references/demo-workflow.md)
- [Remotion 模板速查](references/remotion-templates.md)
