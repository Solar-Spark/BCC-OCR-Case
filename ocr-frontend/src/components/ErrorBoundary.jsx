import React from 'react';
import { Result, Button } from 'antd';

export default class ErrorBoundary extends React.Component {
  constructor(props) {
    super(props);
    this.state = { hasError: false, error: null };
  }
  static getDerivedStateFromError(error) {
    return { hasError: true, error };
  }
  componentDidCatch(error, info) {
    console.error('UI ErrorBoundary:', error, info);
  }
  render() {
    if (this.state.hasError) {
      return (
        <Result
          status="error"
          title="Something went wrong in the UI"
          subTitle={String(this.state.error)}
          extra={[
            <Button key="reload" type="primary" onClick={() => location.reload()}>Reload</Button>
          ]}
        />
      );
    }
    return this.props.children;
  }
}
