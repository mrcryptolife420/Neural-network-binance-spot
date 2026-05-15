import type { DashboardV2Event } from "../types/api";

export function connectEvents(onEvent: (event: DashboardV2Event) => void): WebSocket {
  const proto = location.protocol === "https:" ? "wss" : "ws";
  const socket = new WebSocket(`${proto}://${location.host}/ws/events`);
  socket.onmessage = (message) => onEvent(JSON.parse(message.data));
  return socket;
}
