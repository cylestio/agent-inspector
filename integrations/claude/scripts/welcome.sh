#!/bin/bash
# Agent Inspector - Welcome Message Script
# Shows plugin information on first session start

MARKER_FILE="${HOME}/.agent-inspector-welcomed"
PLUGIN_VERSION="1.0.2"

# Check if already shown welcome this version
if [ -f "$MARKER_FILE" ]; then
    SAVED_VERSION=$(cat "$MARKER_FILE" 2>/dev/null)
    if [ "$SAVED_VERSION" = "$PLUGIN_VERSION" ]; then
        # Already welcomed for this version
        exit 0
    fi
fi

# Show welcome message
cat << 'EOF'

================================================================================
  Agent Inspector Plugin Installed!
================================================================================

  AI Agent Security Analysis - OWASP LLM Top 10

  Quick Start:
    /agent-inspector:scan     - Run security scan on your agent code
    /agent-inspector:fix      - Fix security issues
    /agent-inspector:analyze  - Dynamic runtime analysis
    /agent-inspector:report   - Generate compliance report

  Dashboard: http://localhost:7100

  Run /agent-inspector:setup for full configuration options.

================================================================================

EOF

# Mark as welcomed
echo "$PLUGIN_VERSION" > "$MARKER_FILE"
