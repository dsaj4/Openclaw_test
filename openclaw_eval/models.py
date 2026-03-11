from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


@dataclass(slots=True)
class SkillSpec:
    slug: str
    name: str
    version: str
    category: str
    description: str
    install_source: str
    install_hint: str
    capabilities: list[str] = field(default_factory=list)
    dependencies: list[str] = field(default_factory=list)
    tags: list[str] = field(default_factory=list)
    config_required: bool = False

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "SkillSpec":
        return cls(**data)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(slots=True)
class CaseSpec:
    case_id: str
    title: str
    difficulty: str
    category: str
    summary: str
    required_skills: list[str]
    estimated_minutes: list[int]
    prompt_source: str
    success_criteria: list[str]
    output_artifacts: list[str]
    prerequisites: list[str] = field(default_factory=list)
    tags: list[str] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "CaseSpec":
        return cls(**data)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(slots=True)
class SkillCheck:
    slug: str
    available: bool
    config_required: bool
    note: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(slots=True)
class EvaluationResult:
    case_id: str
    title: str
    status: str
    mode: str
    started_at: str
    finished_at: str
    duration_seconds: float
    workspace: str
    prompt_source: str
    required_skills: list[SkillCheck]
    success_criteria: list[str]
    output_artifacts: list[str]
    notes: list[str] = field(default_factory=list)
    steps: list[dict[str, Any]] = field(default_factory=list)
    score: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["required_skills"] = [item.to_dict() for item in self.required_skills]
        return data


@dataclass(slots=True)
class RunArtifacts:
    result: EvaluationResult
    json_path: Path
    markdown_path: Path
