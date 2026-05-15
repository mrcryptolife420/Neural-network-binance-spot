import React from "react";

type ErrorBoundaryState = { error?: Error };

export class ErrorBoundary extends React.Component<React.PropsWithChildren, ErrorBoundaryState> {
  state: ErrorBoundaryState = {};

  static getDerivedStateFromError(error: Error): ErrorBoundaryState {
    return { error };
  }

  render() {
    if (this.state.error) {
      return <section className="panel error-panel">Dashboard error captured. Check /system/logs.</section>;
    }
    return this.props.children;
  }
}
