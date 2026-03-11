from __future__ import annotations

import argparse
import json
from pathlib import Path

from .registry import load_cases, load_skills, load_workflow
from .runner import EvaluationRunner
from .workspace import DEFAULT_WORKSPACE, init_workspace


def _workspace_path(path: str | None) -> Path:
    return Path(path or DEFAULT_WORKSPACE).resolve()


def cmd_init(args: argparse.Namespace) -> int:
    workspace = _workspace_path(args.workspace)
    paths = init_workspace(workspace)
    print(json.dumps({key: str(value) for key, value in paths.items()}, ensure_ascii=False, indent=2))
    return 0


def cmd_list_cases(args: argparse.Namespace) -> int:
    for case in sorted(load_cases().values(), key=lambda item: item.case_id):
        print(f"{case.case_id}\t{case.difficulty}\t{case.category}\t{case.title}")
    return 0


def cmd_show_case(args: argparse.Namespace) -> int:
    case = load_cases().get(args.case_id)
    if case is None:
        print(f"Case not found: {args.case_id}")
        return 1
    print(json.dumps(case.to_dict(), ensure_ascii=False, indent=2))
    return 0


def cmd_list_skills(args: argparse.Namespace) -> int:
    for skill in sorted(load_skills().values(), key=lambda item: item.slug):
        print(f"{skill.slug}\t{skill.category}\t{skill.install_source}\t{skill.name}")
    return 0


def cmd_show_skill(args: argparse.Namespace) -> int:
    skill = load_skills().get(args.slug)
    if skill is None:
        print(f"Skill not found: {args.slug}")
        return 1
    print(json.dumps(skill.to_dict(), ensure_ascii=False, indent=2))
    return 0


def cmd_run(args: argparse.Namespace) -> int:
    case = load_cases().get(args.case_id)
    if case is None:
        print(f"Case not found: {args.case_id}")
        return 1
    runner = EvaluationRunner(workspace=_workspace_path(args.workspace))
    artifacts = runner.run_and_write(case=case, dry_run=args.dry_run)
    print(
        json.dumps(
            {
                "status": artifacts.result.status,
                "json_report": str(artifacts.json_path),
                "markdown_report": str(artifacts.markdown_path),
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


def cmd_show_workflow(args: argparse.Namespace) -> int:
    print(json.dumps(load_workflow(), ensure_ascii=False, indent=2))
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="openclaw-eval", description="OpenClaw research evaluation CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    init_parser = subparsers.add_parser("init", help="Initialize a workspace")
    init_parser.add_argument("--workspace", help="Workspace directory")
    init_parser.set_defaults(func=cmd_init)

    list_cases_parser = subparsers.add_parser("list-cases", help="List registered cases")
    list_cases_parser.set_defaults(func=cmd_list_cases)

    show_case_parser = subparsers.add_parser("show-case", help="Show a case definition")
    show_case_parser.add_argument("case_id", help="Case ID, for example F1")
    show_case_parser.set_defaults(func=cmd_show_case)

    list_skills_parser = subparsers.add_parser("list-skills", help="List registered skills")
    list_skills_parser.set_defaults(func=cmd_list_skills)

    show_skill_parser = subparsers.add_parser("show-skill", help="Show a skill definition")
    show_skill_parser.add_argument("slug", help="Skill slug, for example agent-browser")
    show_skill_parser.set_defaults(func=cmd_show_skill)

    workflow_parser = subparsers.add_parser("show-workflow", help="Show the execution workflow")
    workflow_parser.set_defaults(func=cmd_show_workflow)

    run_parser = subparsers.add_parser("run", help="Run or validate a case")
    run_parser.add_argument("case_id", help="Case ID, for example F1")
    run_parser.add_argument("--workspace", help="Workspace directory")
    run_parser.add_argument("--dry-run", action="store_true", help="Validate only; do not attempt execution")
    run_parser.set_defaults(func=cmd_run)

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
