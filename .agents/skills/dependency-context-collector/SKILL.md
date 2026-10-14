---
name: dependency-context-collector
description: >-
  Recursively trace local module imports from a Python entry point and bundle only the relevant call
  graph into a minimal Markdown context. Use whenever working on a single feature, reproducing a
  bug from a test file, or answering questions about an execution flow without reading unrelated files.
---

# Smart Dependency Context Collector

## Overview

When refactoring a specific module, fixing a bug reproduced by a single unit test, or implementing a new feature in an entrypoint file, loading the entire codebase into context wastefully consumes tokens and introduces distraction.

The Smart Dependency Context Collector parses the abstract syntax tree (`ast`) of the given entrypoint file, traces all imported local project modules up to a configurable depth (default 3), ignores external standard library and 3rd-party dependencies, and packages the exact relevant source files into a unified, cleanly formatted Markdown bundle.

## When to Use

Activate this skill immediately whenever:

1. You are tasked with fixing a bug reproduced by a specific test file (e.g. `tests/test_login.py`).
2. You need to understand the exact runtime execution chain starting from an entrypoint (e.g. `main.py`, `cli.py`, or an API route handler).
3. You need to provide a focused, multi-file context to a subagent or prompt without including hundreds of irrelevant project files.

## How to Execute

### Method 1: CLI

Run via `run_command`:

```bash
uv run py-token-usage-reducer trace-deps <ENTRY_FILE> [--root <PROJECT_ROOT>] [--depth <MAX_DEPTH>] [-o <OUTPUT_PATH>]
```

Examples:

```bash
# Trace dependencies of a CLI entry point:
uv run py-token-usage-reducer trace-deps src/cli/parser.py -o context/cli_deps.md

# Trace dependencies of a test file with depth 2:
uv run py-token-usage-reducer trace-deps tests/test_core.py --depth 2
```

### Method 2: In-Memory / Python Import

```python
from src.modules.dep_tracer import trace_dependencies

res = trace_dependencies("src/cli/parser.py", project_root=".", max_depth=3)
print(f"Traced {len(res['dependency_files'])} files ({res['tokens']} tokens)")
bundled_context = res["bundled_markdown"]
```

## Verification

- [ ] All locally imported files in the call chain are included.
- [ ] Third-party libraries (`pydantic`, `pytest`, etc.) and standard libraries are filtered out.
- [ ] Output is neatly organized with file headers and syntax-highlighted code blocks.
