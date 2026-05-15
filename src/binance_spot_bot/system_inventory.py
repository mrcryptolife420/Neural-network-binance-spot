from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

from .redaction import redact_payload


@dataclass(frozen=True)
class SystemModuleRef:
    path: str
    exists: bool


@dataclass(frozen=True)
class SystemCommandRef:
    command: str
    safe_env_required: bool = True
    live_trading_enabled: bool = False


@dataclass(frozen=True)
class SystemEvidenceRef:
    path: str
    exists: bool
    secret_free_expected: bool = True


@dataclass(frozen=True)
class SystemCapability:
    name: str
    status: str
    notes: str = ""


@dataclass(frozen=True)
class SystemSubsystem:
    name: str
    status: str
    modules: list[SystemModuleRef] = field(default_factory=list)
    cli_commands: list[SystemCommandRef] = field(default_factory=list)
    dashboard_pages: list[str] = field(default_factory=list)
    tests: list[str] = field(default_factory=list)
    docs: list[str] = field(default_factory=list)
    evidence_artifacts: list[SystemEvidenceRef] = field(default_factory=list)
    roadmaps: list[str] = field(default_factory=list)
    capabilities: list[SystemCapability] = field(default_factory=list)
    safety_level: str = "paper_only"
    readiness_score: int = 0
    readiness_notes: list[str] = field(default_factory=list)
    live_trading_enabled: bool = False


@dataclass(frozen=True)
class SystemInventoryReport:
    status: str
    subsystems: list[SystemSubsystem]
    no_live_statement: str
    live_trading_enabled: bool = False
    signed_endpoints_used: bool = False


SUBSYSTEM_SPECS: tuple[dict[str, Any], ...] = (
    {
        "name": "config/preflight/security",
        "modules": ["config.py", "preflight.py", "security.py"],
        "commands": ["validate-config", "preflight", "redaction-self-test"],
        "docs": ["docs/security-hardening.md"],
        "roadmaps": ["001", "004", "087"],
    },
    {
        "name": "data pipeline",
        "modules": ["binance_data_ingestion.py", "data_store_v2.py", "data_quality_v2.py", "incremental_features.py"],
        "commands": ["fetch-public-data", "public-data-status", "warmup-indicators"],
        "docs": ["docs/data-pipeline-v2-feature-store-contracts.md"],
        "roadmaps": ["076", "096"],
    },
    {
        "name": "feature/indicator/label store",
        "modules": ["features.py", "indicator_compute.py", "indicator_registry.py", "label_store.py", "feature_store_contracts.py"],
        "commands": ["warmup-indicators"],
        "docs": ["docs/data-pipeline-v2-feature-store-contracts.md"],
        "roadmaps": ["016", "077", "096"],
    },
    {
        "name": "evaluation/backtest",
        "modules": ["evaluation.py", "backtest.py", "paper_experiment_split.py"],
        "commands": ["strategy-calibrate"],
        "docs": ["docs/model-research-walkforward-dataset-governance.md"],
        "roadmaps": ["016", "077"],
    },
    {
        "name": "model training/registry/promotion",
        "modules": ["training_pipeline.py", "model_training.py", "model_registry.py", "model_promotion_gate.py"],
        "commands": ["model-register", "model-promote"],
        "docs": ["docs/model-training-pipeline-v2.md"],
        "roadmaps": ["097"],
    },
    {
        "name": "model monitoring/drift/downgrade",
        "modules": ["model_monitoring_pipeline.py", "feature_drift.py", "prediction_drift.py", "model_downgrade_policy.py"],
        "commands": ["model-monitoring-report"],
        "docs": ["docs/shadow-paper-model-monitoring.md"],
        "roadmaps": ["098"],
    },
    {
        "name": "runtime/paper/demo/testnet-readiness",
        "modules": ["runtime.py", "runtime_event_bus.py", "runtime_snapshot_builder.py", "paper.py", "demo_spot.py"],
        "commands": ["run-local", "dashboard", "dashboard-smoke"],
        "docs": ["docs/runtime-core-event-bus-snapshot-optimization.md"],
        "roadmaps": ["002", "017", "095"],
    },
    {
        "name": "paper accounting/risk/execution",
        "modules": ["paper_accounting.py", "risk.py", "execution.py", "demo_execution_sandbox.py"],
        "commands": ["demo-execution-preview", "demo-execution-test-order"],
        "docs": ["docs/demo-spot-execution-sandbox.md"],
        "roadmaps": ["026", "078"],
    },
    {
        "name": "portfolio ensemble/allocation/rotation",
        "modules": ["ensemble_prediction.py", "allocation_policy.py", "rotation_governance.py", "portfolio_rotation_evidence.py"],
        "commands": ["paper-portfolio-ops", "paper-portfolio-optimize"],
        "docs": ["docs/paper-portfolio-ensemble-governance.md"],
        "roadmaps": ["079", "099"],
    },
    {
        "name": "dashboard",
        "modules": ["ui/streamlit_app.py", "ui/page_registry.py", "dashboard_smoke_v2.py"],
        "commands": ["dashboard", "dashboard-smoke", "dashboard-browser-smoke"],
        "docs": ["docs/dashboard-component-refactor-lazy-loading.md"],
        "roadmaps": ["019", "094"],
    },
    {
        "name": "operator evidence/support bundles",
        "modules": ["operator_ops.py", "support_bundle.py", "evidence_scorecard.py"],
        "commands": ["operator-report", "support-bundle", "evidence-scorecard"],
        "docs": ["docs/operator-manual-local-paper-os.md"],
        "roadmaps": ["083", "102"],
    },
    {
        "name": "backup/restore/disaster recovery",
        "modules": ["backup_restore.py", "disaster_recovery_drills.py", "restore_preview.py"],
        "commands": ["state-archive", "support-bundle-restore-preview"],
        "docs": ["docs/disaster-recovery-drills.md"],
        "roadmaps": ["088"],
    },
    {
        "name": "release/migration",
        "modules": ["release_candidate.py", "migration_dry_run.py", "safe_update_rollback.py"],
        "commands": ["check-all"],
        "docs": ["docs/local-release-management-versioned-upgrade-paths.md"],
        "roadmaps": ["089"],
    },
    {
        "name": "roadmap execution/Codex task packs",
        "modules": ["roadmap_execution_report.py", "roadmap_mover.py", "codex_task_packs.py"],
        "commands": ["check-all"],
        "docs": ["docs/developer-experience-codex-task-packs.md"],
        "roadmaps": ["090"],
    },
    {
        "name": "repository knowledge graph",
        "modules": ["repo_knowledge_store.py", "repo_knowledge_report.py", "impact_analysis.py"],
        "commands": ["check-all"],
        "docs": ["docs/repository-knowledge-graph.md"],
        "roadmaps": ["091"],
    },
    {
        "name": "test selection/check-all",
        "modules": ["check_all.py", "intelligent_test_selector.py", "test_inventory.py"],
        "commands": ["check-all"],
        "docs": ["docs/intelligent-test-selection-ci-acceleration.md"],
        "roadmaps": ["092"],
    },
    {
        "name": "performance profiling",
        "modules": ["profiling_core.py", "performance_budget.py", "runtime_profiler.py", "dashboard_profiler.py"],
        "commands": ["check-all"],
        "docs": ["docs/performance-profiling-runtime-bottleneck-analysis.md"],
        "roadmaps": ["093"],
    },
    {
        "name": "permissions/compliance",
        "modules": ["permission_profiles.py", "compliance_report.py", "operator_roles.py"],
        "commands": ["operator-quality-gate"],
        "docs": ["docs/local-permission-profiles-operator-roles.md"],
        "roadmaps": ["087"],
    },
    {
        "name": "AI ops/action center",
        "modules": ["ops_assistant.py", "action_center.py", "approval_workflow.py"],
        "commands": ["operator-report"],
        "docs": ["docs/local-ai-ops-assistant-safe-operator-guidance.md"],
        "roadmaps": ["085", "086"],
    },
)


def _module_ref(root: Path, module: str) -> SystemModuleRef:
    return SystemModuleRef(path=f"src/binance_spot_bot/{module}", exists=(root / "src" / "binance_spot_bot" / module).exists())


def _test_refs(root: Path, roadmaps: list[str]) -> list[str]:
    tests = root / "tests"
    if not tests.exists():
        return []
    refs: list[str] = []
    for number in roadmaps:
        refs.extend(str(path.relative_to(root)) for path in tests.glob(f"test*{number}*.py"))
    return sorted(set(refs))


def _doc_refs(root: Path, docs: list[str]) -> list[str]:
    return [doc for doc in docs if (root / doc).exists()]


def _roadmap_refs(root: Path, numbers: list[str]) -> list[str]:
    refs: list[str] = []
    for base in (root / "Roadmap docs", root / "Voltooid docs"):
        if not base.exists():
            continue
        for number in numbers:
            refs.extend(str(path.relative_to(root)) for path in base.glob(f"{number}-*.md"))
    return sorted(set(refs))


def build_system_inventory(root: Path | str = ".") -> SystemInventoryReport:
    root = Path(root)
    subsystems: list[SystemSubsystem] = []
    for spec in SUBSYSTEM_SPECS:
        modules = [_module_ref(root, module) for module in spec["modules"]]
        existing = sum(1 for module in modules if module.exists)
        status = "implemented" if existing == len(modules) else "partially_implemented" if existing else "missing"
        score = int(round((existing / max(1, len(modules))) * 100))
        missing = [module.path for module in modules if not module.exists]
        notes = ["all referenced modules present"] if not missing else [f"missing modules: {', '.join(missing)}"]
        subsystems.append(
            SystemSubsystem(
                name=spec["name"],
                status=status,
                modules=modules,
                cli_commands=[SystemCommandRef(command=command) for command in spec["commands"]],
                dashboard_pages=[spec["name"]],
                tests=_test_refs(root, spec["roadmaps"]),
                docs=_doc_refs(root, spec["docs"]),
                evidence_artifacts=[SystemEvidenceRef(path=f"data/milestone/{spec['name'].replace('/', '-').replace(' ', '-')}.json", exists=False)],
                roadmaps=_roadmap_refs(root, spec["roadmaps"]),
                capabilities=[SystemCapability(name=spec["name"], status=status)],
                readiness_score=score,
                readiness_notes=notes,
            )
        )
    report_status = "ready" if all(subsystem.status != "missing" for subsystem in subsystems) else "review"
    return SystemInventoryReport(
        status=report_status,
        subsystems=subsystems,
        no_live_statement="Paper OS milestone inventory is read-only and never enables live trading.",
    )


def system_inventory_to_dict(report: SystemInventoryReport) -> dict[str, Any]:
    return redact_payload(asdict(report))


def system_inventory(root: Path | str = ".") -> dict[str, Any]:
    return system_inventory_to_dict(build_system_inventory(root))


def write_system_inventory_report(root: Path | str = ".", out_dir: Path | str | None = None) -> dict[str, str]:
    root = Path(root)
    out = Path(out_dir) if out_dir else root / "data" / "milestone" / "system-inventory"
    out.mkdir(parents=True, exist_ok=True)
    payload = system_inventory(root)
    json_path = out / "system_inventory.json"
    md_path = out / "system_inventory.md"
    json_path.write_text(json.dumps(payload, indent=2, default=str), encoding="utf-8")
    lines = [
        "# System Inventory",
        "",
        f"Status: {payload['status']}",
        "Live trading: disabled",
        "",
    ]
    for subsystem in payload["subsystems"]:
        lines.append(f"- {subsystem['name']}: {subsystem['status']} ({subsystem['readiness_score']}%)")
    md_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return {"json": str(json_path), "markdown": str(md_path), "live_trading_enabled": "False"}
