class RuntimeEventBus:
    def __init__(self): self.events = []
    def publish(self, event): self.events.append(event); return {"status": "published", "live_trading_enabled": False}
    def drain(self): events, self.events = self.events, []; return events
