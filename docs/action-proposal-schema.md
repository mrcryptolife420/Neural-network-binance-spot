# Action Proposal Schema

`ActionProposal` is the canonical Action Center input.

Core fields: `proposal_id`, `source`, `title`, `description`, `category`, `command`, `safety_class`, `required_evidence`, `expected_outputs`, `confirm_phrase`, `no_auto_execute=true`, and `live_trading_enabled=false`.

Safety classes are `read_only`, `safe_generate_artifact`, `confirm_required`, `destructive_confirm_required`, `paper_risk_reducing`, `paper_risk_changing`, and `forbidden`.

