from __future__ import annotations

import json
from pathlib import Path

from .models import EvaluationResult, RunArtifacts


def render_markdown(result: EvaluationResult) -> str:
    skills = "\n".join(
        f"- `{item.slug}`: {'available' if item.available else 'missing'}; {item.note}"
        for item in result.required_skills
    )
    steps = "\n".join(
        f"### {step['name']}\n- Status: {step['status']}\n- Detail: {step['detail']}"
        for step in result.steps
    )
    notes = "\n".join(f"- {note}" for note in result.notes) or "- None"
    criteria = "\n".join(f"- {item}" for item in result.success_criteria)
    outputs = "\n".join(f"- {item}" for item in result.output_artifacts)
    score_lines = "\n".join(f"- {key}: {value}" for key, value in result.score.items())
    return f"""# Evaluation Report: {result.case_id} {result.title}

## Summary
- Status: {result.status}
- Mode: {result.mode}
- Started: {result.started_at}
- Finished: {result.finished_at}
- Duration (seconds): {result.duration_seconds}
- Workspace: `{result.workspace}`
- Prompt Source: `{result.prompt_source}`

## Skill Checks
{skills}

## Success Criteria
{criteria}

## Expected Outputs
{outputs}

## Execution Steps
{steps}

## Score
{score_lines}

## Notes
{notes}
"""


def write_reports(result: EvaluationResult, reports_dir: Path) -> RunArtifacts:
    reports_dir.mkdir(parents=True, exist_ok=True)
    stem = result.case_id.lower()
    json_path = reports_dir / f"{stem}.json"
    markdown_path = reports_dir / f"{stem}.md"
    json_path.write_text(json.dumps(result.to_dict(), ensure_ascii=False, indent=2), encoding="utf-8")
    markdown_path.write_text(render_markdown(result), encoding="utf-8")
    return RunArtifacts(result=result, json_path=json_path, markdown_path=markdown_path)
