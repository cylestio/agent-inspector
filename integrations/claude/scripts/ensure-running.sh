#!/bin/bash
# Agent Inspector - Ensure Running Script
# This script checks if agent-inspector is installed and running,
# and starts it if necessary.

set -e

# Check if agent-inspector is installed
if ! command -v agent-inspector &> /dev/null; then
    echo "Agent Inspector not found. Installing..."
    pip install agent-inspector
    if [ $? -ne 0 ]; then
        echo "ERROR: Failed to install agent-inspector. Please run: pip install agent-inspector"
        exit 1
    fi
    echo "Agent Inspector installed successfully."
fi

# Check if MCP server is running on port 7100
check_server() {
    curl -s http://localhost:7100/health > /dev/null 2>&1
}

if check_server; then
    echo "Agent Inspector is already running."
    exit 0
fi

echo "Starting Agent Inspector server..."

# Start in background, redirect output to log file
nohup agent-inspector anthropic > /tmp/agent-inspector.log 2>&1 &
SERVER_PID=$!

# Wait for server to be ready (max 30 seconds)
echo "Waiting for server to start..."
for i in {1..30}; do
    if check_server; then
        echo "Agent Inspector is ready! (PID: $SERVER_PID)"
        echo "Dashboard: http://localhost:7100"
        echo "MCP Server: http://localhost:7100/mcp"
        echo "Proxy: http://localhost:4000"
        exit 0
    fi
    sleep 1
done

echo "WARNING: Agent Inspector failed to start within 30 seconds."
echo "Please check the log: /tmp/agent-inspector.log"
echo "Or start manually: agent-inspector anthropic"
exit 1
