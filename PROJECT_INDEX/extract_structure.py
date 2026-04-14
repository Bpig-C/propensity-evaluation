import re, json, sys
from pathlib import Path

target = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(".")
results = {"routes": [], "paths": [], "urls": [], "classes": [], "cli_args": []}

for f in target.rglob("*.py"):
    text = f.read_text(errors="replace")
    # 路由
    for m in re.finditer(r'@\w+\.(?:route|get|post|put|delete|patch)\(["\']([^"\']+)', text):
        results["routes"].append({"file": str(f), "route": m.group(1)})
    # 文件路径字符串
    for m in re.finditer(r'["\'](\~?/[^"\']{5,})["\']', text):
        p = m.group(1)
        if not p.startswith("http"):
            results["paths"].append({"file": str(f), "path": p})
    # URL
    for m in re.finditer(r'["\']https?://[^"\']+["\']', text):
        results["urls"].append({"file": str(f), "url": m.group(0).strip("\"'")})
    # 类定义
    for m in re.finditer(r'^class\s+(\w+)\s*(?:\(([^)]*)\))?', text, re.MULTILINE):
        results["classes"].append({"file": str(f), "class": m.group(1), "bases": m.group(2) or ""})
    # CLI argparse 参数
    for m in re.finditer(r'add_argument\(["\'](-{1,2}[\w\-]+)["\']', text):
        results["cli_args"].append({"file": str(f), "arg": m.group(1)})

out = Path("PROJECT_INDEX/structure_extract.json")
out.write_text(json.dumps(results, indent=2, ensure_ascii=False), encoding="utf-8")
print(f"Classes: {len(results['classes'])}, URLs: {len(results['urls'])}, CLI args: {len(results['cli_args'])}, Paths: {len(results['paths'])}")
