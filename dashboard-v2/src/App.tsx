import { useEffect, useMemo, useState } from "react";
import { getJson } from "./api/client";
import { connectEvents } from "./api/ws";
import { AppShell } from "./components/AppShell";
import { ErrorBoundary } from "./components/ErrorBoundary";
import { Sidebar } from "./components/Sidebar";
import { LogsPage } from "./pages/LogsPage";
import { DemoSpotWizardPage } from "./pages/DemoSpotWizardPage";
import { OverviewPage } from "./pages/OverviewPage";
import { PaperSessionWorkflowPage } from "./pages/PaperSessionWorkflowPage";
import { StartBotWizardPage } from "./pages/StartBotWizardPage";
import { applySnapshot, initialDashboardState, reduceEvent, type DashboardState } from "./store/dashboardStore";
import type { DashboardV2Health, DashboardV2Page, DashboardV2Snapshot } from "./types/api";
import { AnalyticsPage } from "./workspace/AnalyticsPage";
import { PreferencesPage } from "./workspace/PreferencesPage";
import { WatchlistsPage } from "./workspace/WatchlistsPage";
import { WorkspacePage } from "./workspace/WorkspacePage";
import { ExtensionPacksPage } from "./workspace/ExtensionPacksPage";
import { MarketIntelligencePage } from "./workspace/MarketIntelligencePage";
import { StrategyLabPage } from "./workspace/StrategyLabPage";
import { PortfolioLabPage } from "./workspace/PortfolioLabPage";
import { ControlCenterPage } from "./workspace/ControlCenterPage";
import { LiveTrainingPage } from "./workspace/LiveTrainingPage";
import { LiveSafetyPage } from "./workspace/LiveSafetyPage";
import { LiveSessionPage } from "./workspace/LiveSessionPage";
import { LiveGovernancePage } from "./workspace/LiveGovernancePage";
import { LiveOpsPage } from "./workspace/LiveOpsPage";
import { PackageCenterPage } from "./workspace/PackageCenterPage";
import { AIDoctorPage } from "./workspace/AIDoctorPage";
import "./styles/app.css";

const fallbackPages: DashboardV2Page[] = [
  { key: "overview", title: "Overview", route: "/", live_trading_enabled: false },
  { key: "demo_spot_trading", title: "Demo Spot Trading", route: "/demo-spot-trading", live_trading_enabled: false },
  { key: "start_bot", title: "Start Bot", route: "/start", live_trading_enabled: false },
  { key: "paper_session_workflow", title: "Paper Session", route: "/paper-session-workflow", live_trading_enabled: false },
  { key: "workspaces", title: "Workspaces", route: "/workspaces", live_trading_enabled: false },
  { key: "watchlists", title: "Watchlists", route: "/watchlists", live_trading_enabled: false },
  { key: "preferences", title: "Preferences", route: "/preferences", live_trading_enabled: false },
  { key: "analytics", title: "Analytics", route: "/analytics", live_trading_enabled: false },
  { key: "extension_packs", title: "Extension Packs", route: "/extension-packs", live_trading_enabled: false },
  { key: "market_intelligence", title: "Market Intelligence", route: "/market-intelligence", live_trading_enabled: false },
  { key: "strategy_lab", title: "Strategy Lab", route: "/strategy-lab", live_trading_enabled: false },
  { key: "portfolio_lab", title: "Portfolio Lab", route: "/portfolio-lab", live_trading_enabled: false },
  { key: "control_center", title: "Control Center", route: "/control-center", live_trading_enabled: false },
  { key: "live_training", title: "Live Training", route: "/live-training", live_trading_enabled: false },
  { key: "live_safety", title: "Live Safety", route: "/live", live_trading_enabled: false },
  { key: "live_session", title: "Live Session", route: "/live/session", live_trading_enabled: false },
  { key: "live_governance", title: "Live Governance", route: "/live/governance", live_trading_enabled: false },
  { key: "live_ops", title: "Live Ops", route: "/live-ops", live_trading_enabled: false },
  { key: "package_center", title: "Package Center", route: "/package", live_trading_enabled: false },
  { key: "ai_doctor", title: "AI Doctor", route: "/ai-doctor", live_trading_enabled: false },
  { key: "system_logs", title: "System Logs", route: "/system/logs", live_trading_enabled: false },
];

export default function App() {
  const [state, setState] = useState<DashboardState>(initialDashboardState);
  const route = window.location.pathname;

  useEffect(() => {
    getJson<DashboardV2Health>("/api/health").then((health) => setState((old) => ({ ...old, health })));
    getJson<{ pages: DashboardV2Page[] }>("/api/pages").then((payload) => setState((old) => ({ ...old, pages: payload.pages })));
    getJson<DashboardV2Snapshot>("/api/runtime/snapshot?profile=overview").then((snapshot) => setState((old) => applySnapshot(old, snapshot)));
    const socket = connectEvents((event) => setState((old) => reduceEvent(old, event)));
    socket.onopen = () => setState((old) => ({ ...old, connected: true, stale: false }));
    socket.onclose = () => setState((old) => ({ ...old, connected: false, stale: true }));
    return () => socket.close();
  }, []);

  const nav = useMemo(() => {
    const merged = [...fallbackPages, ...(state.pages.length ? state.pages : [])];
    const seen = new Set<string>();
    return merged.filter((item) => {
      if (seen.has(item.route)) return false;
      seen.add(item.route);
      return true;
    }).slice(0, 20);
  }, [state.pages]);
  const page =
    route === "/system/logs" ? <LogsPage state={state} /> :
    route === "/start" ? <StartBotWizardPage /> :
    route === "/demo-spot-guided" || route === "/demo-spot-trading" ? <DemoSpotWizardPage /> :
    route === "/paper-session-workflow" ? <PaperSessionWorkflowPage /> :
    route.startsWith("/workspaces") ? <WorkspacePage /> :
    route === "/watchlists" ? <WatchlistsPage /> :
    route === "/preferences" ? <PreferencesPage /> :
    route === "/analytics" ? <AnalyticsPage /> :
    route.startsWith("/extension-packs") || route === "/templates" || route === "/analytics-presets" || route === "/workflow-packs" ? <ExtensionPacksPage /> :
    route.startsWith("/market-intelligence") ? <MarketIntelligencePage /> :
    route.startsWith("/strategy-lab") ? <StrategyLabPage /> :
    route.startsWith("/portfolio-lab") ? <PortfolioLabPage /> :
    route.startsWith("/control-center") ? <ControlCenterPage /> :
    route.startsWith("/live-training") ? <LiveTrainingPage /> :
    route.startsWith("/live-ops") ? <LiveOpsPage /> :
    route.startsWith("/package") ? <PackageCenterPage /> :
    route.startsWith("/ai-doctor") ? <AIDoctorPage /> :
    route.startsWith("/live/governance") ? <LiveGovernancePage /> :
    route.startsWith("/live/session") ? <LiveSessionPage /> :
    route.startsWith("/live") ? <LiveSafetyPage /> :
    <OverviewPage />;

  return (
    <ErrorBoundary>
      <AppShell connected={state.connected}>
        <Sidebar items={nav} />
        <section className="panel">
          <h1>{state.health?.app_name ?? "Dashboard V2"}</h1>
          <p>{state.health?.no_live_statement ?? "LOCAL REALTIME DASHBOARD - NO LIVE TRADING"}</p>
        </section>
        {page}
      </AppShell>
    </ErrorBoundary>
  );
}
