# Phase A1 环境检查清单

> 生成时间：2026-04-15
> 执行人：LocalAI (Claude Code)

## 环境基本信息

| 检查项 | 结果 | 说明 |
|--------|------|------|
| OS | Windows 11 Home China 10.0.26200 | ✅ |
| Python（venv） | 3.12.2（.venv） | ✅ uv 创建的项目专属 venv |
| Python（系统） | 3.12.7（base） | 参考，实际使用 .venv |
| fcntl 可用 | ❌ NO | Windows 不支持，已在 client.py 用 portalocker 替代 |
| portalocker 可用 | ✅ YES | 已安装 portalocker==3.2.0 |
| API_KEYS 配置 | ✅ YES | .env 已配置，含以下供应商密钥（值已遮码）：Anthropic（含自定义 proxy）、Moonshot |
| RATE_LIMIT | false | ✅ 适合 Windows 单进程运行 |
| API_PROXY | litellm | ✅ LiteLLM 代理模式 |

## 数据状态

| 路径 | 状态 | 文件大小示例 |
|------|------|------------|
| data/sample/ | ✅ 存在且可读 | 4 个 domain，每个含 1 个 workspace |
| data/sample/cyber-security/...scenarios_funcs.json | ✅ 真实文件 | ~102 KB |
| data/full/bio-security/ | ✅ 完整（真实文件） | ~386 KB/文件 |
| data/full/chemical-security/ | ✅ 完整（真实文件） | — |
| data/full/cyber-security/ | ✅ 完整（真实文件） | — |
| data/full/self-proliferation/ | ✅ 完整（真实文件，8 个 workspace） | ~278 KB–222 KB |

**注**：DATA_STATUS.txt 中标注 self-proliferation 为"LFS 指针"，但实际检查发现已是真实数据，与预期不符（可能是 DATA_STATUS.txt 未更新）。

## 依赖安装

| 状态 | 详情 |
|------|------|
| ✅ PASS | 78 个包已安装到 .venv |
| 修复记录 | requirements.txt 中 numpy==1.24.4 → numpy>=1.26.0（Python 3.12 移除了 distutils） |
| 新增 Windows 依赖 | portalocker>=2.0.0（已加入 requirements.txt） |

安装命令：
```bash
uv venv .venv --python 3.12
uv pip install -r requirements.txt --python .venv/Scripts/python.exe
```

## 导入测试

```
.venv/Scripts/python.exe -c "import sys; sys.path.insert(0,'evaluation'); import evaluation.main; print('ok')"
```

| 结果 | 说明 |
|------|------|
| ✅ PASS | `import ok` |
| 非致命警告 | `Failed to load state from ./state.json: 'SLURM_RESTART_COUNT'` — 正常，SLURM 是 Linux 集群变量，Windows 不存在 |

## 可以跑 smoke test

✅ YES

## 运行环境使用方式

```bash
# 项目内所有命令均使用 .venv 中的 python
.venv/Scripts/python.exe evaluation/main.py [args...]
# 或激活后
source .venv/Scripts/activate
python evaluation/main.py [args...]
```

## 已知问题与注意事项

1. **fcntl → portalocker**：client.py 已通过 `if sys.platform == 'win32'` 分支实现跨平台兼容，无需额外处理。
2. **RATE_LIMIT=false**：已在 .env 中禁用限速，适合 Windows 单进程调试，smoke test 阶段够用。
3. **DATA_STATUS.txt 陈旧**：self-proliferation 标注为"LFS 指针"不准确，实际已拉取真实数据，可正常使用。
4. **SLURM 警告**：state.json 读取时因缺少 SLURM_RESTART_COUNT 环境变量报警，不影响功能，断点续跑逻辑正常初始化（Running using state keys: []）。

## 下一步

Phase A2：最小 Smoke Test
- 使用 data/sample/ 作为输入目录
- 选择一个便宜模型（Moonshot 或 Anthropic claude-haiku）
- 限制为第 1 个 scenario，pressure category = time，max_workers=1
