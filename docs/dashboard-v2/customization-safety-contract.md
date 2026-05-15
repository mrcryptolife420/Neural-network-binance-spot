# Customization Safety Contract

Dashboard V2 workspaces are local-only operator views. They can combine safe widgets, analytics and watchlists, but they cannot add live trading routes, signed order actions, remote telemetry or arbitrary code.

Mandatory locks: `no_live_banner`, `stop_button`, `safety_widgets_locked=true`, `live_trading_enabled=false`.
