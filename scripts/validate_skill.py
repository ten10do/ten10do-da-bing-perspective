#!/usr/bin/env python3
"""Validate the repository's Codex skill without third-party dependencies."""

from __future__ import annotations

import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "SKILL.md"
EXPECTED_REFERENCES = [
    ROOT / "references" / "synthesis.md",
    *[
        ROOT / "references" / "research" / name
        for name in (
            "01-writings.md",
            "02-conversations.md",
            "03-expression-dna.md",
            "04-external-views.md",
            "05-decisions.md",
            "06-timeline.md",
        )
    ],
]


def fail(errors: list[str], message: str) -> None:
    errors.append(message)


def parse_frontmatter(text: str, errors: list[str]) -> dict[str, str]:
    if not text.startswith("---\n"):
        fail(errors, "SKILL.md must start with YAML frontmatter")
        return {}

    end = text.find("\n---\n", 4)
    if end < 0:
        fail(errors, "SKILL.md frontmatter is not closed")
        return {}

    lines = text[4:end].splitlines()
    data: dict[str, str] = {}
    current: str | None = None
    for line in lines:
        if line.startswith((" ", "\t")):
            if current:
                data[current] = f"{data[current]} {line.strip()}".strip()
            continue
        match = re.fullmatch(r"([a-z_]+):(?:\s*(.*))?", line)
        if not match:
            fail(errors, f"unsupported frontmatter line: {line!r}")
            continue
        current, value = match.groups()
        data[current] = "" if value in (None, "|") else value.strip()

    unknown = set(data) - {"name", "description"}
    if unknown:
        fail(errors, f"frontmatter has unsupported keys: {sorted(unknown)}")
    return data


def validate() -> list[str]:
    errors: list[str] = []
    if not SKILL.is_file():
        return ["SKILL.md is missing"]

    try:
        text = SKILL.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return ["SKILL.md is not valid UTF-8"]

    frontmatter = parse_frontmatter(text, errors)
    name = frontmatter.get("name", "")
    description = frontmatter.get("description", "")
    if not re.fullmatch(r"[a-z0-9-]{1,64}", name):
        fail(errors, "frontmatter name must use lowercase letters, digits, and hyphens")
    if name != "da-bing-perspective":
        fail(errors, f"unexpected skill name: {name!r}")
    if not description:
        fail(errors, "frontmatter description is empty")
    if len(description) > 1024:
        fail(errors, f"frontmatter description is too long: {len(description)} characters")

    line_count = len(text.splitlines())
    if line_count >= 500:
        fail(errors, f"SKILL.md has {line_count} lines; expected fewer than 500")

    required_headings = (
        "## 角色规则",
        "## 回答工作流（Agentic Protocol）",
        "## 核心心智模型",
        "## 决策启发式",
        "## 表达 DNA",
        "## 诚实边界",
    )
    for heading in required_headings:
        if heading not in text:
            fail(errors, f"missing required section: {heading}")

    model_count = len(re.findall(r"^### \d+\. ", text, flags=re.MULTILINE))
    if not 3 <= model_count <= 7:
        fail(errors, f"expected 3-7 mental models, found {model_count}")

    if "调研截止：2026-07-13" not in text:
        fail(errors, "honesty boundary must retain the research cutoff date")

    for path in EXPECTED_REFERENCES:
        if not path.is_file():
            fail(errors, f"missing reference: {path.relative_to(ROOT)}")

    agent_yaml = ROOT / "agents" / "openai.yaml"
    if not agent_yaml.is_file():
        fail(errors, "agents/openai.yaml is missing")
    else:
        agent_text = agent_yaml.read_text(encoding="utf-8")
        if "$da-bing-perspective" not in agent_text:
            fail(errors, "agents/openai.yaml default_prompt must mention $da-bing-perspective")

    tracked_text = "\n".join(
        path.read_text(encoding="utf-8")
        for path in [SKILL, agent_yaml, *EXPECTED_REFERENCES]
        if path.is_file()
    )
    placeholders = re.findall(r"\b(?:TODO|FIXME|TBD)\b|待完善|示例占位", tracked_text)
    if placeholders:
        fail(errors, f"found unresolved placeholders: {sorted(set(placeholders))}")

    return errors


def main() -> int:
    errors = validate()
    if errors:
        print("Skill validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("Skill validation passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
