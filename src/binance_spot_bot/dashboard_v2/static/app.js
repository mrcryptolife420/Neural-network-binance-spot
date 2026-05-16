const LOCAL_API_RE = /^https?:\/\/(127\.0\.0\.1|localhost)(:\d+)?$/i;
const queryApi = new URLSearchParams(window.location.search).get("api");
const apiBase = queryApi && LOCAL_API_RE.test(queryApi) ? queryApi.replace(/\/$/, "") : "";
const state = { active: routeToSection(window.location.pathname), cache: {}, lastError: "" };

const sections = {
  overview: [
    ["Health", "GET", "/api/health"],
    ["Config", "GET", "/api/config"],
    ["Pages", "GET", "/api/pages"],
    ["Runtime Snapshot", "GET", "/api/runtime/snapshot"],
    ["Live Status", "GET", "/api/live/status"],
    ["AI Doctor", "GET", "/api/ai-doctor/status"]
  ],
  runtime: [
    ["Runtime Snapshot", "GET", "/api/runtime/snapshot"],
    ["Candles", "GET", "/api/charts/candles"],
    ["Equity", "GET", "/api/charts/equity"]
  ],
  "app-control": [
    ["Health", "GET", "/api/app-control/health"],
    ["Profiles", "GET", "/api/app-control/profiles"],
    ["Profile Templates", "GET", "/api/app-control/profile-templates"],
    ["Secret References", "GET", "/api/app-control/secret-ref-status"],
    ["Profile Matrix", "GET", "/api/app-control/profile-matrix"]
  ],
  "live-training": [
    ["Training Health", "GET", "/api/live-training/health"],
    ["Demo Targets", "GET", "/api/live-training/demo-targets"],
    ["Target Progress", "GET", "/api/live-training/demo-targets/progress"]
  ],
  "live-safety": [
    ["Live Status", "GET", "/api/live/status"],
    ["Evidence Prerequisites", "GET", "/api/live/evidence-prerequisites"],
    ["Dry Run", "POST", "/api/live/dry-run/start"],
    ["Order Preview", "POST", "/api/live/order-preview"],
    ["Sizing Guard", "POST", "/api/live/sizing-guard/check"],
    ["Kill Switch Drill", "POST", "/api/live/safety-drills/kill-switch"],
    ["Emergency Stop", "POST", "/api/live/emergency-stop"],
    ["Evidence Export", "POST", "/api/live/evidence/export"]
  ],
  "live-session": [
    ["Session Status", "GET", "/api/live-session/status"],
    ["Plan Validate", "POST", "/api/live-session/plan/validate"],
    ["Budget", "GET", "/api/live-session/budget"],
    ["Scaling", "GET", "/api/live-session/scaling"],
    ["Heartbeat", "GET", "/api/live-session/heartbeat"],
    ["Emergency Stop", "POST", "/api/live-session/emergency-stop"]
  ],
  "live-governance": [
    ["Governance Status", "GET", "/api/live-governance/status"],
    ["Review", "POST", "/api/live-governance/review/run"],
    ["Scorecard", "POST", "/api/live-governance/scorecards/generate"],
    ["Scaling Decision", "POST", "/api/live-governance/scaling-decision"],
    ["Evidence Export", "POST", "/api/live-governance/evidence/export"]
  ],
  "live-ops": [
    ["Ops Status", "GET", "/api/live-ops/status"],
    ["Detect Incidents", "POST", "/api/live-ops/incidents/detect"],
    ["Runbooks", "GET", "/api/live-ops/runbooks"],
    ["Rollback Drill", "POST", "/api/live-ops/rollback-drills/run"],
    ["Forensic Timeline", "POST", "/api/live-ops/forensics/build-timeline"],
    ["Recovery Gate", "POST", "/api/live-ops/recovery/check"]
  ],
  package: [
    ["Package Status", "GET", "/api/package/status"],
    ["Profiles", "GET", "/api/package/profiles"],
    ["Backup", "POST", "/api/package/backup/create"],
    ["Update Plan", "POST", "/api/package/update/plan"],
    ["Rollback Preview", "POST", "/api/package/rollback/preview"],
    ["Recovery Kit", "POST", "/api/package/recovery-kit/build"],
    ["Evidence Export", "POST", "/api/package/evidence/export"]
  ],
  "ai-doctor": [
    ["Doctor Status", "GET", "/api/ai-doctor/status"],
    ["Start Run", "POST", "/api/ai-doctor/runs/start"],
    ["Collect", "POST", "/api/ai-doctor/runs/latest/collect"],
    ["Match Issues", "POST", "/api/ai-doctor/runs/latest/match-issues"],
    ["Summary", "POST", "/api/ai-doctor/runs/latest/summary"],
    ["Codex Prompt", "POST", "/api/ai-doctor/runs/latest/codex-prompt"],
    ["Export Bundle", "POST", "/api/ai-doctor/runs/latest/export"]
  ],
  diagnostics: [
    ["Health", "GET", "/api/health"],
    ["No Live Proof", "GET", "/api/no-live-proof"],
    ["Route Pages", "GET", "/api/pages"]
  ]
};

function routeToSection(pathname) {
  if (pathname.startsWith("/ai-doctor")) return "ai-doctor";
  if (pathname.startsWith("/package")) return "package";
  if (pathname.startsWith("/live-ops")) return "live-ops";
  if (pathname.startsWith("/live/governance")) return "live-governance";
  if (pathname.startsWith("/live/session")) return "live-session";
  if (pathname.startsWith("/live-training")) return "live-training";
  if (pathname.startsWith("/live")) return "live-safety";
  return "overview";
}

function endpointUrl(path) {
  return `${apiBase}${path}`;
}

async function apiGet(path) {
  return apiFetch(path, { method: "GET" });
}

async function apiPost(path, body = {}) {
  return apiFetch(path, { method: "POST", headers: { "content-type": "application/json" }, body: JSON.stringify(body) });
}

async function apiFetch(path, options) {
  if (queryApi && !LOCAL_API_RE.test(queryApi)) throw new Error("Blocked non-localhost API base");
  const response = await fetch(endpointUrl(path), options);
  if (!response.ok) throw new Error(`${options.method} ${path} failed: ${response.status}`);
  return response.json();
}

function renderJson(target, payload) {
  target.textContent = JSON.stringify(payload, null, 2);
}

function showError(error) {
  state.lastError = String(error.message || error);
  const panel = document.querySelector("#error-panel");
  panel.hidden = false;
  panel.textContent = state.lastError;
}

function clearError() {
  const panel = document.querySelector("#error-panel");
  panel.hidden = true;
  panel.textContent = "";
}

function cardTitle(section) {
  return section.split("-").map((word) => word[0].toUpperCase() + word.slice(1)).join(" ");
}

function renderShell() {
  document.querySelectorAll(".sidebar button").forEach((button) => {
    const active = button.dataset.section === state.active;
    button.classList.toggle("active", active);
    button.onclick = () => {
      state.active = button.dataset.section;
      history.pushState({}, "", sectionToPath(state.active));
      refreshAll();
    };
  });
  const cards = document.querySelector("#cards");
  cards.innerHTML = "";
  for (const [title, method, path] of sections[state.active] || sections.overview) {
    const card = document.createElement("article");
    card.className = "card";
    const toolbar = method === "POST" ? `<div class="toolbar"><button data-action="${path}">Run ${title}</button></div>` : "";
    card.innerHTML = `<h3>${title}</h3>${toolbar}<pre id="panel-${slug(path)}">Loading ${method} ${path}</pre>`;
    cards.appendChild(card);
  }
  document.querySelectorAll("[data-action]").forEach((button) => {
    button.onclick = () => runPanel(button.dataset.action);
  });
}

function sectionToPath(section) {
  const map = { package: "/package", "ai-doctor": "/ai-doctor", "live-ops": "/live-ops", "live-governance": "/live/governance", "live-session": "/live/session", "live-training": "/live-training", "live-safety": "/live" };
  return map[section] || "/";
}

function slug(path) {
  return path.replace(/[^a-z0-9]+/gi, "-").replace(/^-|-$/g, "");
}

async function loadPanel(title, method, path) {
  const target = document.querySelector(`#panel-${slug(path)}`);
  if (!target) return;
  try {
    const payload = method === "POST" ? { status: "ready", action: "click button to run", path, live_trading_enabled: false } : await apiGet(path);
    state.cache[path] = payload;
    renderJson(target, payload);
    if (path === "/api/health") document.querySelector("#backend-status").textContent = "Backend: online";
  } catch (error) {
    target.textContent = String(error.message || error);
    showError(error);
    if (path === "/api/health") document.querySelector("#backend-status").textContent = "Backend: offline";
  }
}

async function runPanel(path) {
  const target = document.querySelector(`#panel-${slug(path)}`);
  if (!target) return;
  try {
    clearError();
    renderJson(target, await apiPost(path));
  } catch (error) {
    target.textContent = String(error.message || error);
    showError(error);
  }
}

async function refreshAll() {
  clearError();
  renderShell();
  await Promise.all((sections[state.active] || sections.overview).map(([title, method, path]) => loadPanel(title, method, path)));
  document.querySelector("#refresh-status").textContent = `Last refresh: ${new Date().toLocaleTimeString()}`;
}

function connectWebSocket() {
  try {
    const wsBase = apiBase || `${window.location.protocol}//${window.location.host}`;
    const wsUrl = wsBase.replace(/^http/, "ws") + "/ws/events";
    const socket = new WebSocket(wsUrl);
    socket.onopen = () => { document.querySelector("#ws-status").textContent = "WebSocket: connected"; };
    socket.onmessage = () => { document.querySelector("#ws-status").textContent = "WebSocket: heartbeat"; };
    socket.onerror = () => { document.querySelector("#ws-status").textContent = "WebSocket: polling fallback"; };
    socket.onclose = () => { document.querySelector("#ws-status").textContent = "WebSocket: polling fallback"; };
  } catch {
    document.querySelector("#ws-status").textContent = "WebSocket: polling fallback";
  }
}

window.onpopstate = () => {
  state.active = routeToSection(window.location.pathname);
  refreshAll();
};

connectWebSocket();
refreshAll();
setInterval(() => {
  if (["overview", "runtime"].includes(state.active)) refreshAll();
}, 2000);
