from __future__ import annotations

import json
from functools import lru_cache
from importlib import resources

from .models import CaseSpec, SkillSpec


def _load_json(filename: str) -> list[dict]:
    text = resources.files("openclaw_eval.data").joinpath(filename).read_text(encoding="utf-8")
    return json.loads(text)


def _load_any_json(filename: str):
    text = resources.files("openclaw_eval.data").joinpath(filename).read_text(encoding="utf-8")
    return json.loads(text)


@lru_cache(maxsize=1)
def load_skills() -> dict[str, SkillSpec]:
    return {item["slug"]: SkillSpec.from_dict(item) for item in _load_json("skills.json")}


@lru_cache(maxsize=1)
def load_cases() -> dict[str, CaseSpec]:
    return {item["case_id"]: CaseSpec.from_dict(item) for item in _load_json("cases.json")}


@lru_cache(maxsize=1)
def load_workflow() -> dict:
    return _load_any_json("workflow.json")
