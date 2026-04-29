# 工作流状态机 · 7 phase enter/exit/artifact

> 每个 phase 都有 enter 条件 / exit 条件 / 强制 artifact。
> **不满足 exit 条件,不准前进**,哪怕用户催。

## 状态总图

```
[START]
   │
   ▼
[Phase 0: Gate]──── 11 项缺失 ───→ 回问用户(不前进)
   │ Gate 通过 + 用户 OK
   ▼
[Phase 1: 需求文档化]── artifact 落盘 ──→ [Phase 2]
   │
   ▼
[Phase 2: 设计规范]── artifact 落盘 ──→ [Phase 3]
   │
   ▼
[Phase 3: 接口契约]── artifact 落盘 ──→ [Phase 4]
   │
   ▼
[Phase 4: 前端实现 (Ralph + simplifier)]── DONE + verify pass ──→ [Phase 5]
   │
   ▼
[Phase 5: 后端实现 (Ralph + simplifier)]── DONE + verify pass ──→ [Phase 6]
   │
   ▼
[Phase 6: 浏览器/E2E 验证]── 7 层全 ✅ 或用户接受 ──→ [Phase 7]
   │
   ▼
[Phase 7: 交付]── simplifier 全量 + README + 部署 ──→ [DONE]
```

---

## Phase 0 · 需求 Gate

| 字段 | 值 |
|------|---|
| **enter** | 用户首次发出需求 |
| **exit** | 11 项填齐 + 4 项可行性通过 + 用户明确说"OK" |
| **artifact** | `docs/0-requirements-snapshot.md`(需求快照) |
| **触发干预** | 任一项缺失 / 可行性 ❌ |

## Phase 1 · 需求文档化

| 字段 | 值 |
|------|---|
| **enter** | Phase 0 artifact 已落盘 |
| **exit** | requirements.md 含 4 节(用户故事 / 功能列表 / 非功能 / 不做清单) |
| **artifact** | `docs/1-requirements.md` |
| **使用 skill** | `spec-workflow` |
| **Ralph?** | 否 |

## Phase 2 · 设计规范

| 字段 | 值 |
|------|---|
| **enter** | Phase 1 artifact 已落盘 |
| **exit** | DESIGN.md 含 8+ 章 + tokens 是合法 JSON + copy.json 5 句无禁用词 |
| **artifact** | `docs/2-DESIGN.md`, `tokens/design-tokens.json`, `docs/2-copy.json` |
| **使用 skill** | `ui-design` + `designdna` + `design-templates` + `copywriting-design` + `taste-skill` 自检 |
| **Ralph?** | 否 |

## Phase 3 · 接口契约

| 字段 | 值 |
|------|---|
| **enter** | Phase 2 artifact 已落盘 |
| **exit** | INTERFACE.md 含命令树或 API 路由表 + 退出码/错误码表 |
| **artifact** | `docs/3-INTERFACE.md` |
| **使用 skill** | `cli-design`(CLI 项目) / `api-design`(API 项目) |
| **Ralph?** | 否 |

## Phase 4 · 前端实现

| 字段 | 值 |
|------|---|
| **enter** | Phase 3 artifact 已落盘 |
| **exit** | Ralph DONE + 单元测试通过 + simplifier P0 跑完 + dev server 起得来 |
| **artifact** | 可运行前端代码 + `docs/4-frontend-build-log.md` |
| **使用 skill** | `frontend-patterns` + 平台 skill(`web-development` / `miniprogram-development` / ...) |
| **Ralph?** | ✅ max=20,DONE 后跑 simplifier P0 微清扫 |
| **触发干预** | 满 20 轮(申请书) / 卡住 3 轮 / 涉及付费 |

## Phase 5 · 后端实现

| 字段 | 值 |
|------|---|
| **enter** | Phase 4 artifact 已落盘 |
| **exit** | Ralph DONE + 单元测试通过 + simplifier P0 跑完 + 服务能起 + 健康检查 200 |
| **artifact** | 可运行后端代码 + `docs/5-backend-build-log.md` |
| **使用 skill** | `backend-patterns` + `cloud-functions` / `cloudrun-development` 等 |
| **Ralph?** | ✅ 同 Phase 4 |
| **触发干预** | 同 Phase 4 |

## Phase 6 · 浏览器/E2E 验证

| 字段 | 值 |
|------|---|
| **enter** | Phase 5 artifact 已落盘(后端可访问) |
| **exit** | 7 层验证报告全 ✅ 或用户明确接受降级 |
| **artifact** | `docs/6-verification-report.md`(7 层每层一行) |
| **使用 skill** | `browser-automation` + `e2e-testing` + `verification-loop` |
| **Ralph?** | 否(验证不需要循环改代码) |
| **触发干预** | 任一层 ❌ → 等用户决定 |

7 层:加载 / 控制台 / 网络 / 视觉回归 / 关键路径 E2E / 微交互 / A11y。

## Phase 7 · 交付

| 字段 | 值 |
|------|---|
| **enter** | Phase 6 通过(或用户接受降级) |
| **exit** | simplifier 全量(P0+P1)跑完 + README + 部署 URL + (可选)demo 视频 |
| **artifact** | 简化后代码 + `README.md` + 部署链接 + `docs/demo/`(可选) |
| **使用 skill** | `code-simplifier` 全量 + `deployment-patterns` / `web-development`(部署部分) + `programmatic-video`(可选) |
| **Ralph?** | 否 |
| **触发干预** | 涉及付费(域名/CDN) / 部署到生产前确认 |

---

## 状态文件(每 phase 必写)

每个 phase 退出时,在 `docs/_state.json` 里更新:

```json
{
  "phase": 4,
  "status": "done",
  "ralph_iterations": 6,
  "simplifier_p0_changes": 12,
  "verification_pass": true,
  "next_phase": 5,
  "intervention_required": false,
  "ts": 1747000000
}
```

让用户(或下一个 agent)随时能 `cat docs/_state.json` 知道当前在哪一步。

---

## 异常路径

| 触发 | 行为 |
|------|------|
| 任一 phase 的 exit 不满足 | 不前进,报告 + 等用户决策 |
| Phase 0 用户长时间不回应 | 收摊,留下 `docs/0-requirements-snapshot.md` 的草稿 |
| Phase 4/5 Ralph 满 20 轮 | 续轮申请书 + 等用户回复 |
| Phase 6 验证 ❌ | 选项:回 Phase 4/5 修复 / 接受降级 / 改需求回 Phase 0 |
| 任一时刻用户主动 `/cancel-ralph` 或 "停" | 立即停止,留下当前 phase 的 artifact |
