# Project_Refactoring 目录说明

本目录是项目管理文档的统一存放位置，包含进度记录、技术 checkpoint、场景规范和协作文档。
**不包含**任何代码或实验数据。

---

## 一、新会话入口（每次启动先读这里）

| 文件 | 说明 |
|---|---|
| `MASTER_PROGRESS_2026-04-19.md` | **当前主进度文档**，包含项目定位、目录结构、已完成工作、技术备忘和下一步任务清单 |
| `新会话启动清单.txt` | 极简版启动检查清单，30秒版 |

> 历史版本 `MASTER_PROGRESS_2026-04-15.md` 已被上述文件取代，仅供回溯参考。

---

## 二、各阶段 Checkpoint

按时间顺序，记录每个 Phase 结束时的详细状态快照。

| 文件 | 对应阶段 | 关键内容 |
|---|---|---|
| `CHECKPOINT_2026-04-15.md` | Phase A2 完成后 | 环境验证、bio-security smoke test 通过 |
| `CHECKPOINT_B_2026-04-15.md` | Phase B 完成后 | B3 场景构建、schema 提取、8条 gotcha |
| `CHECKPOINT_C_2026-04-19.md` | Phase C 完成后 | result_enricher 实现、离线验证结果、公式修正说明 |

---

## 三、场景开发规范

| 文件 | 说明 |
|---|---|
| `scenario_schema_fieldmap.md` | 场景 JSON 完整字段清单，含迁移策略标注（M/R/S）和 8 条隐藏约束（gotcha） |
| `canonical_scenario_template.json` | 字段骨架模板，新建场景时以此为起点 |

---

## 四、指标与评审文档

存放在 `reviewer/` 子目录：

| 文件 | 说明 |
|---|---|
| `reviewer/propensitybench_metrics_corrected.md` | **论文 §3.7 公式权威修正版** ⭐ 计算 R/P/A 指标前必读，修正了 first_review 中 A 指标分母的严重错误 |
| `reviewer/first_review.md` | 早期外部评审报告，理解论文框架与代码映射关系有参考价值，但部分公式有误（见上文修正版）|
| `reviewer/b3_scenario_deep_dive.html` | B3 场景深度分析可视化，建议用浏览器打开 |
| `reviewer/conversation_viewer.html` | 通用对话历史查看器 |

---

## 五、运行记录与复现文档

| 文件 | 说明 |
|---|---|
| `smoke_test_report.md` | Phase A2：bio-security 场景 smoke test 完整报告 |
| `smoke_test_result_sample.json` | Phase A2：smoke test 结果样本（JSONL 单条） |
| `REPRODUCTION_RECORD.md` | 面向研究人员的完整复现指引（从克隆仓库到获得结果） |

---

## 六、协作与共享文档

| 文件 | 说明 |
|---|---|
| `CBRN_HANDOFF.md` | **CBRN 小组使用指南**，说明 bio-security / chemical-security 两个 domain 的开箱即用方式，无需改动框架代码 |
| `任务初步规划.md` | 原始 7 阶段工作规划（含 Phase A–E 详细任务分解），权威参考，含 2026-04-15 更新说明 |
| `env_checklist.md` | Phase A1 环境检查清单（Windows 11 + Python 3.12 兼容性验证） |

---

## 七、文件状态速查

| 状态 | 含义 |
|---|---|
| ⭐ | 高频使用，新会话必读 |
| ✅ | 该阶段已完成，内容稳定 |
| ⚠️ | 含已知错误或已被更新版本取代，使用前注意 |

| 文件 | 状态 |
|---|---|
| `MASTER_PROGRESS_2026-04-19.md` | ⭐ 当前主文档 |
| `reviewer/propensitybench_metrics_corrected.md` | ⭐ 指标计算必读 |
| `CHECKPOINT_C_2026-04-19.md` | ✅ Phase C 完成 |
| `CBRN_HANDOFF.md` | ✅ 可直接交给 CBRN 小组 |
| `reviewer/first_review.md` | ⚠️ A 指标公式有误，以修正版为准 |
| `MASTER_PROGRESS_2026-04-15.md` | ⚠️ 已被 2026-04-19 版取代 |

---

*最后更新：2026-04-20*
