from .safety import LiveSafetyDecision, no_live_order
def automatic_disarm_rules(findings: list[str]): return {**LiveSafetyDecision("disarm" if findings else "ok", "auto_disarm", findings, requires_approval=False).to_dict(), **no_live_order()}
