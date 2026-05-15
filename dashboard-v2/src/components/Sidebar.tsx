export type NavItem = { key: string; title: string; route: string; legacy?: boolean };

export function Sidebar({ items }: { items: NavItem[] }) {
  return (
    <nav>
      {items.map((item) => (
        <a key={item.key} href={item.route}>{item.title}{item.legacy ? " (legacy)" : ""}</a>
      ))}
    </nav>
  );
}
