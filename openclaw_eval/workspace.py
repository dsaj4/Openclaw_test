from __future__ import annotations

from pathlib import Path


DEFAULT_WORKSPACE = "workspace"
SKILL_TEMPLATE_MD = """# Skill Name

## Use Cases
- Describe when this skill should be used.

## Inputs
- Describe required inputs and assumptions.

## Workflow
1. Validate prerequisites.
2. Execute the core workflow.
3. Return structured output.

## Outputs
- Describe the output format and artifacts.
"""

SKILL_TEMPLATE_MANIFEST = """{
  "slug": "example-skill",
  "name": "Example Skill",
  "version": "1.0.0",
  "entry_type": "instructional",
  "install_source": "ClawHub",
  "config_required": false,
  "capabilities": ["example_capability"],
  "dependencies": []
}
"""


def init_workspace(root: Path) -> dict[str, Path]:
    paths = {
        "root": root,
        "skills": root / "skills",
        "cases": root / "cases",
        "outputs": root / "outputs",
        "reports": root / "outputs" / "reports",
        "logs": root / "outputs" / "logs",
        "data": root / "outputs" / "data",
        "temp": root / "temp",
        "docs": root / "docs",
    }
    for path in paths.values():
        path.mkdir(parents=True, exist_ok=True)
    template_dir = paths["docs"] / "skill_template"
    template_dir.mkdir(parents=True, exist_ok=True)
    (template_dir / "SKILL.md").write_text(SKILL_TEMPLATE_MD, encoding="utf-8")
    (template_dir / "manifest.json").write_text(SKILL_TEMPLATE_MANIFEST, encoding="utf-8")
    return paths
