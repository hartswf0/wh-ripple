#!/usr/bin/env python3
import math
import subprocess
from pathlib import Path
from collections import Counter

ROOT = Path.home() / "hartswf0_repo_audit"
REPOS = ROOT / "repos"

SINCE = "2025-05-01"
UNTIL = "2026-05-01"

MINE = {
    ("Loom Mason", "user@example.com"),
    ("Watson Hartsoe", "watson.hartsoe@gmail.com"),
}

CODE_EXTS = {".html", ".js", ".css", ".ts", ".tsx", ".jsx", ".py"}

EXCLUDE_REPOS = {
    "TTS", "nomic", "langflow", "detectron2", "AgentVerse",
    "generative-models", "mesa-examples", "llm_multiagent_debate",
    "large_concept_model", "LCM-architecture", "CADdrive",
    "THEMsketch-threejs", "vue-apps", "core-components",
    "pretext-field"
}

EXCLUDE_DIRS = {
    ".git", "node_modules", "dist", "build", "vendor", ".next", "__pycache__"
}

EXCLUDE_PATTERNS = (
    "package-lock.json", "yarn.lock", "pnpm-lock.yaml",
    ".min.js", ".map",
    "embeddings", "dependency_graph", "dummy_speakers"
)

def run(cmd, cwd=None):
    return subprocess.run(
        cmd,
        cwd=cwd,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
        check=False,
    ).stdout

def has_head(repo_dir):
    result = subprocess.run(
        ["git", "-C", str(repo_dir), "rev-parse", "--verify", "HEAD"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    return result.returncode == 0

def skip_path(path):
    p = Path(path)
    s = str(path).lower()
    if any(part in EXCLUDE_DIRS for part in p.parts):
        return True
    return any(x.lower() in s for x in EXCLUDE_PATTERNS)

def count_lines(path):
    try:
        data = Path(path).read_bytes()
        return data.count(b"\n") + (1 if data and not data.endswith(b"\n") else 0), len(data)
    except Exception:
        return 0, 0

def write_tsv(path, rows, header):
    with open(path, "w", encoding="utf-8") as f:
        f.write("\t".join(header) + "\n")
        for row in rows:
            f.write("\t".join(str(x if not isinstance(x, float) else f"{x:.2f}") for x in row) + "\n")

code_mass = []
edit_heat = []
hot_organs = []
repo_counts = Counter()
debug_authors = Counter()

for repo_dir in sorted(REPOS.iterdir()):
    if not repo_dir.is_dir() or not (repo_dir / ".git").exists():
        continue

    repo = repo_dir.name
    if repo in EXCLUDE_REPOS:
        continue
    if not has_head(repo_dir):
        continue

    commit_lines = run([
        "git", "-C", str(repo_dir),
        "log",
        f"--since={SINCE}",
        f"--until={UNTIL}",
        "--format=%H%x09%aN%x09%aE"
    ]).splitlines()

    counts = Counter()

    for line in commit_lines:
        parts = line.split("\t")
        if len(parts) != 3:
            continue

        sha, name, email = parts
        debug_authors[(name, email)] += 1

        if (name, email) not in MINE:
            continue

        files = run([
            "git", "-C", str(repo_dir),
            "show",
            "--pretty=format:",
            "--name-only",
            sha
        ]).splitlines()

        for file in files:
            file = file.strip()
            if not file:
                continue
            if skip_path(file):
                continue
            if Path(file).suffix.lower() not in CODE_EXTS:
                continue
            counts[file] += 1

    if not counts:
        continue

    repo_counts[repo] = sum(counts.values())

    for rel, touches in counts.items():
        full = repo_dir / rel
        lines, bytes_ = count_lines(full) if full.exists() else (0, 0)
        edit_heat.append((touches, repo, rel))

        if lines > 0:
            code_mass.append((lines, bytes_, repo, rel))
            score = touches * math.log(lines + 1)
            hot_organs.append((score, touches, lines, bytes_, repo, rel))

code_mass.sort(reverse=True)
edit_heat.sort(reverse=True)
hot_organs.sort(reverse=True)
repo_rows = [(count, repo) for repo, count in repo_counts.items()]
repo_rows.sort(reverse=True)

write_tsv(ROOT / "mine_code_mass.tsv", code_mass, ["lines", "bytes", "repo", "path"])
write_tsv(ROOT / "mine_edit_heat.tsv", edit_heat, ["touches", "repo", "path"])
write_tsv(ROOT / "mine_hot_organs.tsv", hot_organs, ["score", "touches", "lines", "bytes", "repo", "path"])
write_tsv(ROOT / "mine_repo_heat.tsv", repo_rows, ["touches", "repo"])

debug_rows = [(count, name, email) for (name, email), count in debug_authors.items()]
debug_rows.sort(reverse=True)
write_tsv(ROOT / "mine_debug_authors_seen.tsv", debug_rows, ["commits_seen", "name", "email"])

print("DONE")
print("Created:")
print("  mine_code_mass.tsv")
print("  mine_edit_heat.tsv")
print("  mine_hot_organs.tsv")
print("  mine_repo_heat.tsv")
print("  mine_debug_authors_seen.tsv")
