# Example 03 · Landing Page(design-templates + copywriting-design)

> 测试:能不能从一句产品定位 → 产出**完整 DESIGN.md + design-tokens.json + 5 句关键文案**,且文案不踩禁用词。

## 测什么

1. **DESIGN.md 章节齐全**(Aesthetic / Voice / Color / Typography / Spacing / Layout / Motion / A11y 至少 8 章)
2. **design-tokens.json 是合法 JSON**,包含 color/spacing/radius 三组
3. **5 句关键文案**(主标题/CTA/空态/错态/成态)无禁用词("极致/亲/我们/操作成功" 等)
4. **HTML demo** 能用纯浏览器打开,视觉与 DESIGN.md 一致

## 输入(假产品)

```
产品: SnapMatte
一句话: 给开发者拍照截图自动加优雅留白与品牌水印
受众: 独立开发者 + 小团队
语气坐标: 朋友 + 逻辑 + 克制 + 偶尔自嘲
```

## 期望产出

- `expected/DESIGN.md` —— 完整设计规范
- `expected/design-tokens.json` —— 合法 JSON tokens
- `expected/copy.json` —— 5 句关键文案
- `expected/index.html` —— 单文件登录页(参考实现)

## 怎么跑

```bash
examples/03-landing-page/run.sh
```

会校验:
1. DESIGN.md 章节齐全
2. design-tokens.json 是合法 JSON 且含必填 token
3. copy.json 5 句齐全 + 无禁用词
4. index.html 能被浏览器打开(检查 HTML5 doctype + 有 `<title>`)

## 触发 prompt(给 agent)

```
触发 design-templates + copywriting-design skill。

输入:
  产品: SnapMatte
  一句话: 给开发者拍照截图自动加优雅留白与品牌水印
  受众: 独立开发者 + 小团队
  语气: 朋友 + 逻辑 + 克制 + 偶尔自嘲

要求产出:
  1. DESIGN.md(10 章模板)
  2. design-tokens.json(color/spacing/radius)
  3. 5 句关键文案(主标题/CTA/空态/错态/成态)
  4. 单文件 index.html(用上述 token + 文案)

红线:
  - 文案不能含禁用词:极致/超快/极速/亲/哦/我们/操作成功/暂无数据/立即体验
  - DESIGN.md 必须含具体 hex 配色,不能写"蓝色调"
  - 字体必须有具体字体名(不是 sans-serif)
```
