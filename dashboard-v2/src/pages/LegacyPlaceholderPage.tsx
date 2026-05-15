import { LegacyBadge } from "../components/LegacyBadge";

export function LegacyPlaceholderPage({ title }: { title: string }) {
  return <section><h2>{title}</h2><LegacyBadge reason="Streamlit remains fallback while V2 parity is completed." /></section>;
}
