import { SafetyBanner } from "./SafetyBanner";
import { StatusBar } from "./StatusBar";

export function AppShell({ connected, children }: { connected: boolean; children: React.ReactNode }) {
  return (
    <main>
      <SafetyBanner />
      <StatusBar connected={connected} />
      {children}
    </main>
  );
}
