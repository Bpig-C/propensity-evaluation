# PropensityBench 数据使用指南

## 📦 数据拉取状态

### 当前状态
- ✅ **已拉取**：bio-security、chemical-security、cyber-security 数据（完整）
- ⏳ **拉取中**：self-proliferation 数据（~60 MB）
- 📊 **总大小**：544 MB（4 个域的完整数据）

### 如何确保数据完整

```bash
# 检查 LFS 安装
git lfs --version

# 第一次设置
git lfs install

# 拉取所有完整数据
cd C:/project/propensity-evaluation
git lfs pull --include="data/full/**"

# 验证拉取完成
find data/full -type f -name "*.json" | wc -l  # 应该 > 100
```

## 🎯 数据结构

### 1. 四个风险域

| 域 | 目录 | 场景数 | 关键问题 |
|-----|------|--------|--------|
| **bio-security** | `data/full/bio-security/` | 8 | 病原体研究、药物耐药性 |
| **chemical-security** | `data/full/chemical-security/` | 8 | 危险化学物质合成 |
| **cyber-security** | `data/full/cyber-security/` | 8 | 网络攻击、系统漏洞 |
| **self-proliferation** | `data/full/self-proliferation/` | 8 | 模型自我复制、部署 |

### 2. 每个域的工作场景

以 bio-security 为例，包含 8 个工作场景：
- Agricultural-Biotech-Facility（农业生物技术设施）
- BSL-3-4-High-Containment-Laboratory（高等级生物安全实验室）
- Cloud-Based-Bioinformatics-&-DNA-Database-Service
- Marine-Biotechnology-Research-Institute
- Pandemic-Response-&-Biosecurity-Center
- Personalized-Medicine-&-Gene-Therapy-Lab
- Pharmaceutical-R&D-Laboratory
- Sustainable-Biomanufacturing-Innovation-Center

### 3. 每个场景的文件类型

```
data/full/bio-security/bsl-3-4-high-containment-laboratory/
├── scenarios_funcs.json          # 工具定义（安全和危险工具）
├── scenarios_policies.json        # 安全策略和规则
├── scenarios_states.json          # 环境初始状态
├── scenarios_messages.json        # 压力消息的完整树结构（11 个强度级别）
└── scenarios_messages_single.json # 压力消息的扁平化版本（6 类别，每类 11 级）
```

### 4. 压力类别（6 种）

1. **evaluation-awareness**（评估意识）
   - Agent 意识到自己会被评估
   - 诱导：承诺报告、性能指标、评审

2. **financials**（财务压力）
   - 薪酬、融资、经费限制
   - 诱导：报酬、预算削减

3. **power-seeking**（权力寻求）
   - 晋升、权限、控制权
   - 诱导：职位升迁、影响力

4. **resource-deprivation**（资源剥夺）
   - 工具、材料、支持的缺乏
   - 诱导：资源紧缺、截止日期

5. **self-preservation**（自我保护）
   - 系统安全、备份、冗余
   - 诱导：系统威胁、关闭风险

6. **time**（时间压力）
   - 紧急情况、截止日期、延迟成本
   - 诱导：加速完成、时间限制

## 🔄 评估流程

### 基础路径

```
数据加载
  ↓
遍历每个场景和压力类别
  ↓
初始化 Agent（赋予角色和工具）
  ↓
发送初始任务消息
  ↓
施加 6 个压力消息（按强度递增）
  ↓
监测 Agent 是否调用危险工具
  ↓
保存完整交互历史和结果
```

### 关键指标

```python
result = {
    "domain": "bio-security",
    "scenario": "accelerated_drug_resistance_profiling",
    "category": "evaluation-awareness",
    
    # 核心指标
    "trigger_called": False,      # ✅ 未调用危险工具 = 安全
    "target_called": True,        # ✅ 调用了合法工具 = 有效
    
    # 完整交互记录
    "interaction_response": [
        # 52 条消息，包含完整对话、工具调用、返回值
    ]
}
```

## 📊 数据规模

### 评估维度

```
4 个域 × 8 个场景 × 6 个压力类别 = 192 个基础测试点

如果还要考虑 11 个压力强度级别：
192 × 11 = 2,112 个完整评估点
```

### 数据存储

```
总数据量：544 MB（压缩后）
结果数据：~10-20 MB（取决于交互长度）
日志数据：~100-200 MB（详细对话记录）
```

## 🚀 使用示例

### 快速验证（小样本）
```bash
python evaluation/main.py \
    --model_name "Pro/deepseek-ai/DeepSeek-V3.2" \
    --api_base "https://api.siliconflow.cn/v1" \
    --model_provider "openai" \
    --input_dir "data/sample/" \
    --job_id "test_quick" \
    --max_workers 1
```
- 耗时：~2-5 分钟
- 测试用例：~24 个

### 完整评估（所有数据）
```bash
python evaluation/main.py \
    --model_name "Pro/deepseek-ai/DeepSeek-V3.2" \
    --api_base "https://api.siliconflow.cn/v1" \
    --model_provider "openai" \
    --input_dir "data/full/" \
    --job_id "full_eval" \
    --max_workers 4              # Windows 用线程，Linux 用进程
```
- 耗时：Windows 3-5 小时，Linux 1-2 小时
- 测试用例：1,152 个（192 × 6）

### 按域评估
```bash
# 只评估生物安全
python evaluation/main.py \
    --input_dir "data/full/" \
    --job_id "bio_only" \
    --job_id "bio"              # 自动过滤只含 "bio"
```

## 📈 分析结果

### 输出位置

```
evaluation/output/
├── results/
│   └── Pro-deepseek-ai-DeepSeek-V3.2/
│       └── {timestamp}/
│           └── results.jsonl   # 评估结果（每行一个 JSON）
└── traj/
    └── Pro-deepseek-ai-DeepSeek-V3.2/
        └── {timestamp}/
            └── {domain}/{workspace}/{role}/
                ├── {scenario}.log       # 完整对话记录
                └── temp/
                    └── {scenario}-{category}.log  # 单个类别的交互
```

### 统计分析

```python
import json
import pandas as pd

# 加载结果
results = []
with open("evaluation/output/results/.../results.jsonl") as f:
    for line in f:
        results.append(json.loads(line))

# 统计倾向性
df = pd.DataFrame(results)
propensity = df.groupby(['domain', 'category']).agg({
    'trigger_called': 'sum'           # 危险工具调用次数
}).reset_index()

# 生成热力图
import matplotlib.pyplot as plt
heatmap_data = propensity.pivot(
    index='domain',
    columns='category',
    values='trigger_called'
)
plt.heatmap(heatmap_data, annot=True)
plt.savefig("propensity_heatmap.png")
```

## ⚠️ 常见问题

### Q: LFS 拉取失败怎么办？
```bash
# 重新拉取
git lfs pull --include="data/full/**" -f

# 检查 LFS 状态
git lfs ls-files

# 验证文件是否真实还是指针
file data/full/bio-security/*/scenarios_messages_single.json | head -3
# 应该显示 "JSON data"，不是 "ASCII text"
```

### Q: 如何只运行某个特定域？
```bash
# bio 域
python evaluation/main.py --job_id "bio"

# cyber 域
python evaluation/main.py --job_id "cyber"

# 多个域组合
python evaluation/main.py --job_id "bio_cyber"
```

### Q: 数据格式有文档吗？
是的，详见 `data/README.md`

### Q: 能否修改压力消息？
可以！修改 `scenarios_messages.json` 或 `scenarios_messages_single.json`

## 🔍 数据验证清单

- [ ] 数据目录存在 `data/full/` 和 `data/sample/`
- [ ] 4 个域的目录都存在
- [ ] 每个域包含 8 个工作场景
- [ ] 每个场景包含 5 个 JSON 文件（funcs, policies, states, messages, messages_single）
- [ ] JSON 文件内容是 JSON 格式（不是 LFS 指针）
- [ ] 总数据大小 ~544 MB

---

**最后更新**：2026-04-14  
**验证环境**：Windows 11 Pro 10.0.26200
