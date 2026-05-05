#!/usr/bin/env python3
import os
import subprocess
from pathlib import Path
from collections import Counter

ROOT = Path.home() / "hartswf0_repo_audit"
REPOS = ROOT / "repos"

SINCE = "2025-05-01"
UNTIL = "2026-05-01"

EXCLUDE_REPOS = {
    "TTS",
    "nomic",
    "langflow",
    "detectron2",
    "AgentVerse",
    "generative-models",
    "mesa-examples",
    "llm_multiagent_debate",
    "large_concept_model",
    "LCM-architecture",
    "CADdrive",
    "THEMsketch-threejs",
    "vue-apps",
    "core-components",
}

CODE_EXTS = {
    ".html", ".js", ".css", ".ts", ".tsx", ".jsx", ".py"
}

DATA_EXTS = {
    ".json", ".geojson", ".csv", ".tsv"
}

EXCLUDE_DIR_PARTS = {
    ".git",
    "node_modules",
    "dist",
    "build",
    "vendor",
    ".next",
    "__pycache__",
    "tests/data",
    "accuracy",
}

EXCLUDE_FILE_PATTERNS = (
    "package-lock.json",
    "yarn.lock",
    "pnpm-lock.yaml",
    ".min.js",
    ".map",
    "embeddings",
    "manifest",
    "dependency_graph",
    "taxonomy",
    "geometry",
    "skeleton",
    "osm",
    "dummy_speakers",
    "data.json",
    "synthesized_data.js",
    "rocky_data.js",
    "embeddings_data.js",
    "onyx-data.js",
)

def sh(cmd, cwd=None):
    return subprocess.run(
        cmd,
        cwd=cwd,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
        check=False,
    ).stdout

def is_empty_repo(repo_dir):
    out = subprocess.run(
        ["git", "-C", str(repo_dir), "rev-parse", "--verify", "HEAD"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    return out.returncode != 0

def skip_path(path):
    s = str(path)
    parts = set(path.parts)
    if parts & EXCLUDE_DIR_PARTS:
        return True
    if any(x in s for x in EXCLUDE_DIR_PARTS):
        return True
    name = path.name
    lower = s.lower()
    return any(p.lower() in lower for p in EXCLUDE_FILE_PATTERNS)

def count_lines(path):
    try:
        with open(path, "rb") as f:
            data = f.read()
        return data.count(b"\n") + (1 if data and not data.endswith(b"\n") else 0), len(data)
    except Exception:
        return 0, 0

def rel_repo_file(file_path, repo_dir):
    return str(file_path.relative_to(repo_dir))

code_rows = []
data_rows = []
edit_counts = []

for repo_dir in sorted(REPOS.iterdir()):
    if not repo_dir.is_dir() or not (repo_dir / ".git").exists():
        continue

    repo = repo_dir.name

    if repo in EXCLUDE_REPOS:
        continue

    if is_empty_repo(repo_dir):
        continue

    for file_path in repo_dir.rglob("*"):
        if not file_path.is_file():
            continue

        rel = Path(rel_repo_file(file_path, repo_dir))

        if skip_path(rel):
            continue

        ext = file_path.suffix.lower()

        if ext in CODE_EXTS:
            lines, bytes_ = count_lines(file_path)
            if lines > 0:
                code_rows.append((lines, bytes_, repo, str(rel)))

        elif ext in DATA_EXTS:
            lines, bytes_ = count_lines(file_path)
            if lines > 0:
                data_rows.append((lines, bytes_, repo, str(rel)))

    log = sh([
        "git", "-C", str(repo_dir),
        "log",
        f"--since={SINCE}",
        f"--until={UNTIL}",
        "--name-only",
        "--format="
    ])

    c = Counter()
    for line in log.splitlines():
        line = line.strip()
        if not line:
            continue
        rel = Path(line)
        if skip_path(rel):
            continue
        if rel.suffix.lower() not in CODE_EXTS:
            continue
        c[str(rel)] += 1

    for path, count in c.items():
        edit_counts.append((count, repo, path))

code_rows.sort(reverse=True)
data_rows.sort(reverse=True)
edit_counts.sort(reverse=True)

def write_tsv(path, rows, header):
    with open(path, "w", encoding="utf-8") as f:
        f.write("\t".join(header) + "\n")
        for row in rows:
            f.write("\t".join(map(str, row)) + "\n")

write_tsv(ROOT / "target_code_mass.tsv", code_rows, ["lines", "bytes", "repo", "path"])
write_tsv(ROOT / "target_data_organs.tsv", data_rows, ["lines", "bytes", "repo", "path"])
write_tsv(ROOT / "target_edit_heat.tsv", edit_counts, ["touches", "repo", "path"])

# combined hot organs: files that are both large and repeatedly touched
line_lookup = {(repo, path): (lines, bytes_) for lines, bytes_, repo, path in code_rows}
hot = []
for touches, repo, path in edit_counts:
    if (repo, path) in line_lookup:
        lines, bytes_ = line_lookup[(repo, path)]
        score = touches * 1000 + lines
        hot.append((score, touches, lines, bytes_, repo, path))

hot.sort(reverse=True)
write_tsv(ROOT / "target_hot_organs.tsv", hot, ["score", "touches", "lines", "bytes", "repo", "path"])

print("DONE")
print("Created:")
print("  target_code_mass.tsv")
print("  target_edit_heat.tsv")
print("  target_hot_organs.tsv")
print("  target_data_organs.tsv")
