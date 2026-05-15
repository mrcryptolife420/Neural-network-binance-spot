import { CHART_LIMITS } from "./chartLimits";

export function appendLimited<T>(items: T[], next: T, limit = CHART_LIMITS.candles): T[] {
  return [...items, next].slice(-limit);
}
