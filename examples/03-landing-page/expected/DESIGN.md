# SnapMatte · Design Specification

## 1. Aesthetic Direction
- 主方向: **瑞士主义 + 工程师感**(Helvetica/Geist 网格 + 大留白 + 单色为主 + 一抹绿色作为强调)
- 局部偏移: 字号比典型瑞士派**大一档**,因受众是开发者,目标是"扫一眼就能记住"
- 参考: Vercel 官网, Linear marketing site, Stripe Press

## 2. Voice & Tone

| 维度 | 选择 |
|------|------|
| 正式度 | 朋友 |
| 理性度 | 逻辑 |
| 温度 | 克制 |
| 幽默度 | 偶尔自嘲 |

关键 5 句文案见 [copy.json](copy.json)。

## 3. Color

| Token | Value | Usage |
|-------|-------|-------|
| color/bg | #0a0a0a | 页面底色(深色优先) |
| color/fg | #fafafa | 正文 |
| color/fg-muted | #a3a3a3 | 次要文本 |
| color/accent | #4ade80 | 主 CTA、链接 |
| color/border | #262626 | 卡片边、分割线 |
| color/success | #22c55e | 成态 |
| color/warning | #facc15 | 警告 |
| color/error | #f87171 | 错态 |

## 4. Typography

| Token | Family | Weight | Size/Line |
|-------|--------|--------|-----------|
| heading/h1 | Geist | 700 | 72/80 |
| heading/h2 | Geist | 600 | 40/48 |
| heading/h3 | Geist | 600 | 24/32 |
| body/default | Geist | 400 | 16/26 |
| body/small | Geist | 400 | 14/22 |
| code | Geist Mono | 400 | 14/22 |

中文 fallback: Noto Sans SC。

## 5. Spacing & Sizing

- 间距步长: **4px**
- 唯一 token: `0 / 4 / 8 / 12 / 16 / 24 / 32 / 48 / 64`(只用这 9 个)
- 圆角: `0 / 4 / 8 / 16`
- 阴影:
  - sm: `0 1px 2px rgba(0,0,0,.05)`
  - md: `0 4px 12px rgba(0,0,0,.1)`
  - lg: `0 12px 32px rgba(0,0,0,.15)`

## 6. Layout

- 主网格: 12 列, gutter 24px, max-width 1280px
- 主页面: **2/3 + 1/3 不对称**(左侧大标题 + 右侧产品截图)
- 移动端: 单列, padding 16px
- 留白原则: 关键元素四周至少 64px

## 7. Motion

- 缓动: `cubic-bezier(0.4, 0, 0.2, 1)`
- 时长: 150ms 微交互 / 300ms 页面级
- **不超过 500ms**(开发者反感慢动效)

## 8. Accessibility

- 对比度: WCAG AA(正文 4.5:1,大字 3:1) — 已校验
- 焦点态: 必须可见,`outline: 2px solid var(--color-accent)`
- 键盘可达: 所有交互
- 屏幕阅读器: 主要图片有 alt,form 有 label

## 9. Iconography

- 库: [Lucide](https://lucide.dev/)
- 尺寸: 16 / 20 / 24
- 描边宽度: 1.5px
- 颜色: 跟随 currentColor

## 10. State Rules

- **Empty**: 不用"暂无数据"。改成"还没人 X 过"或"试试导入示例"
- **Error**: 说人话 + 给出下一步("保存失败,网络好像断了。再试一次?")
- **Loading**: skeleton 优先,spinner 仅用于按钮内
- **Success**: 不用"操作成功"。说具体后果("订单发往杭州")
