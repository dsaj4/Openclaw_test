from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path

from .models import CaseSpec, EvaluationResult, SkillCheck
from .registry import load_skills
from .reporting import write_reports
from .workspace import init_workspace


class EvaluationRunner:
    def __init__(self, workspace: Path):
        self.workspace = workspace
        self.paths = init_workspace(workspace)
        self.skills = load_skills()

    def _check_skills(self, case: CaseSpec) -> list[SkillCheck]:
        checks: list[SkillCheck] = []
        for slug in case.required_skills:
            spec = self.skills.get(slug)
            if spec is None:
                checks.append(
                    SkillCheck(
                        slug=slug,
                        available=False,
                        config_required=False,
                        note="Referenced by the case but missing from the skill registry.",
                    )
                )
                continue
            skill_path = self.paths["skills"] / slug
            manifest_path = skill_path / "manifest.json"
            skill_doc_path = skill_path / "SKILL.md"
            fully_installed = skill_path.exists() and manifest_path.exists() and skill_doc_path.exists()
            if fully_installed:
                note = f"Found installed skill with manifest and SKILL.md at {skill_path}."
            elif skill_path.exists():
                missing_parts = []
                if not manifest_path.exists():
                    missing_parts.append("manifest.json")
                if not skill_doc_path.exists():
                    missing_parts.append("SKILL.md")
                note = f"Skill folder exists but is incomplete; missing {', '.join(missing_parts)}."
            else:
                note = f"Install from {spec.install_source}. Hint: {spec.install_hint}"
            checks.append(
                SkillCheck(
                    slug=slug,
                    available=fully_installed,
                    config_required=spec.config_required,
                    note=note,
                )
            )
        return checks

    def run_case(self, case: CaseSpec, dry_run: bool = False) -> EvaluationResult:
        started = datetime.now(UTC)
        checks = self._check_skills(case)
        missing_count = sum(1 for item in checks if not item.available)
        status = "dry-run" if dry_run else "ready" if missing_count == 0 else "blocked"
        notes: list[str] = []
        if missing_count:
            notes.append(f"{missing_count} required skill(s) are not installed in the workspace.")
        if dry_run:
            notes.append("Dry-run mode validates metadata and readiness without running external workflows.")
        if case.output_rules:
            notes.extend(case.output_rules)
        steps = [
            {
                "name": "Workspace initialization",
                "status": "completed",
                "detail": f"Ensured workspace exists at {self.workspace}.",
            },
            {
                "name": "Case metadata load",
                "status": "completed",
                "detail": f"Loaded case {case.case_id} with {len(case.required_skills)} required skill(s).",
            },
            {
                "name": "Skill readiness check",
                "status": "completed" if missing_count == 0 else "warning",
                "detail": "All required skills available." if missing_count == 0 else f"{missing_count} skill(s) missing.",
            },
            {
                "name": "Execution plan",
                "status": "skipped" if dry_run else "pending",
                "detail": "Prompt execution is not automated yet; use the generated report as an operator checklist. A Markdown summary never counts as the main artifact unless the case explicitly requires Markdown.",
            },
        ]
        finished = datetime.now(UTC)
        score = {
            "metadata_completeness": 100,
            "skill_readiness": max(0, 100 - (missing_count * 20)),
            "automation_readiness": 85 if dry_run else 70,
            "overall": round((100 + max(0, 100 - (missing_count * 20)) + (85 if dry_run else 70)) / 3, 1),
        }
        return EvaluationResult(
            case_id=case.case_id,
            title=case.title,
            status=status,
            mode="dry-run" if dry_run else "standard",
            started_at=started.isoformat(),
            finished_at=finished.isoformat(),
            duration_seconds=round((finished - started).total_seconds(), 3),
            workspace=str(self.workspace),
            prompt_source=case.prompt_source,
            required_skills=checks,
            required_apis=case.required_apis,
            success_criteria=case.success_criteria,
            output_artifacts=case.output_artifacts,
            notes=notes,
            steps=steps,
            score=score,
        )

    def run_and_write(self, case: CaseSpec, dry_run: bool = False):
        result = self.run_case(case=case, dry_run=dry_run)
        return write_reports(result=result, reports_dir=self.paths["reports"])
