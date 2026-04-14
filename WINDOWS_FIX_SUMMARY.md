# PropensityBench Windows 11 复现修复总结

## 概览

PropensityBench 原为 Linux/macOS 开发的项目。本文档记录了在 Windows 11 上成功复现的所有修复。

## 修复清单

### 1. API 认证问题 ✅
**文件**：`api_client/client.py:253`  
**问题**：litellm 不从正确的环境变量读 API Key  
**修复**：显式传入 `api_key=session_key` 到 `litellm.completion()`

```python
completion_args = {
    "model": session_model,
    "messages": messages,
    "temperature": self.temperature,
    "no-log": True,
    "api_key": session_key,  # 显式传入
    **kwargs
}
```

### 2. Windows fcntl 不支持 ✅
**文件**：`api_client/client.py:21-34`  
**问题**：`import fcntl` 在 Windows 上失败  
**修复**：用 `portalocker` 替换

```python
if sys.platform == 'win32':
    import portalocker
    class _fcntl:
        LOCK_EX = portalocker.LOCK_EX
        LOCK_UN = portalocker.LOCK_UN
        @staticmethod
        def flock(f, operation):
            if operation == portalocker.LOCK_EX:
                portalocker.lock(f, portalocker.LOCK_EX)
            else:
                portalocker.unlock(f)
    fcntl = _fcntl()
else:
    import fcntl
```

### 3. Windows 信号处理不完整 ✅
**文件**：`evaluation/main.py:169-170`  
**问题**：`signal.SIGCONT` Windows 不支持  
**修复**：条件检查

```python
if sys.platform != 'win32':
    signal.signal(signal.SIGCONT, sigcont_handler)
```

### 4. Windows 信号 SIGKILL 不支持 ✅
**文件**：`evaluation/main.py:51`  
**问题**：`signal.SIGKILL` Windows 不支持  
**修复**：改用 `SIGTERM`

```python
sig = signal.SIGKILL if sys.platform != 'win32' else signal.SIGTERM
```

### 5. Windows CPU 亲和性查询失败 ✅
**文件**：`evaluation/main.py:565`  
**问题**：`os.sched_getaffinity()` Windows 不存在  
**修复**：使用 fallback

```python
args.max_workers = args.max_workers if args.max_workers > 0 else \
    (len(os.sched_getaffinity(0)) if hasattr(os, 'sched_getaffinity') else os.cpu_count() or 4) * 4
```

### 6. 路径超长问题 ✅
**文件**：`evaluation/main.py:390, 444, 591`  
**问题**：Windows MAX_PATH = 260 字符限制  
**修复**：
- 去掉时间戳中的微秒（-7 chars）
- 展平 temp 日志路径，去掉冗余的 `{scenario_name}/` 子目录（-38 chars）

```python
# 改前
args.timestamp = str(datetime.now())
# 改后
args.timestamp = datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
```

### 7. ProcessPoolExecutor 子进程崩溃 ✅
**文件**：`evaluation/main.py:665-667`  
**问题**：Windows `spawn` 启动方式导致子进程被杀死  
**修复**：自动降级到 ThreadPoolExecutor

```python
Executor = concurrent.futures.ThreadPoolExecutor if sys.platform == 'win32' else concurrent.futures.ProcessPoolExecutor

with Executor(max_workers=args.max_workers) as executor:
    # ...
```

### 8. f-string 语法错误 ✅
**文件**：`evaluation/main.py:646, 649`  
**问题**：f-string 表达式内部无法使用相同引号  
**修复**：改为双引号

```python
# 改前
output_path_initial = f'{args.model_name.replace('/', '-')}/...'
# 改后
output_path_initial = f'{args.model_name.replace("/", "-")}/...'
```

## 验证步骤

### 1. 环境准备
```bash
conda create -n propensity-eval-repro python=3.11 -y
conda run -n propensity-eval-repro pip install -r requirements.txt
conda run -n propensity-eval-repro pip install portalocker
```

### 2. API 密钥配置
```bash
# 在项目根目录创建 .env
cat > .env << 'EOF'
API_KEYS=("sk-your_siliconflow_key_here")
RATE_LIMIT=false
API_PROXY=litellm
RATE_PM=60
