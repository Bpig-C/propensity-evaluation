import re
from collections import Counter
from pathlib import Path

text = (Path(__file__).parent / "call_graph.dot").read_text(encoding="utf-8", errors="replace")

node_fqn = {}
for m in re.finditer(r'"([\w]+)"\s*\[.*?tooltip="([^\\]+)', text):
    node_fqn[m.group(1)] = m.group(2).split("\\n")[0].strip()

edges = []
for m in re.finditer(r'"([\w]+)"\s*->\s*"([\w]+)"', text):
    s = node_fqn.get(m.group(1), m.group(1))
    d = node_fqn.get(m.group(2), m.group(2))
    sm = ".".join(s.split(".")[:-1]) if "." in s else s
    dm = ".".join(d.split(".")[:-1]) if "." in d else d
    if sm != dm:
        edges.append((sm, s.split(".")[-1], dm, d.split(".")[-1]))

matrix = Counter((sm, dm) for sm, _, dm, _ in edges)
print("跨模块调用矩阵（次数最多的前20）：")
for (sm, dm), cnt in matrix.most_common(20):
    print(f"  {sm:45} → {dm}  ×{cnt}")
