export function StatusBar({ connected }: { connected: boolean }) {
  return <div className="status">WebSocket: {connected ? "connected" : "connecting"}</div>;
}
