#!/usr/bin/env bash
set -euo pipefail

echo "=== Arena Benchmark Runner ==="

# --- 1. Check Python version ---
PYTHON=${PYTHON:-python3}
PY_VERSION=$($PYTHON -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')
echo "Using Python $PY_VERSION ($PYTHON)"

if $PYTHON -c 'import sys; exit(0 if sys.version_info >= (3, 11) else 1)' 2>/dev/null; then
    :
else
    echo "ERROR: Python 3.11+ required (got $PY_VERSION)"
    exit 1
fi

# --- 2. Create venv if needed ---
if [ ! -d ".venv" ]; then
    echo "Creating virtual environment..."
    $PYTHON -m venv .venv
fi
source .venv/bin/activate

# --- 3. Install dependencies ---
echo "Installing dependencies..."
pip install -q -e ".[dev]"

# --- 4. Load environment variables ---
if [ -f .env ]; then
    set -a; source .env; set +a
    echo "Loaded .env"
else
    echo "WARNING: No .env file found."
    echo "Copy .env.example to .env and fill in API keys."
    exit 1
fi

# --- 5. Verify MCP server starts ---
echo "Verifying MCP server..."
timeout 5 $PYTHON -c "
from arena.mcp_server import mcp
print('MCP server OK: ' + mcp.name)
" || { echo "ERROR: MCP server failed to load"; exit 1; }

# --- 6. Check API keys ---
MISSING=0
[ -z "${ANTHROPIC_API_KEY:-}" ] && \
    echo "WARNING: ANTHROPIC_API_KEY not set" && MISSING=1
[ -z "${AWS_ACCESS_KEY_ID:-}" ] && \
    echo "WARNING: AWS credentials not set" && MISSING=1
[ -z "${GOOGLE_API_KEY:-}" ] && \
    echo "WARNING: GOOGLE_API_KEY not set" && MISSING=1

if [ "$MISSING" -eq 1 ]; then
    echo "(Frameworks with missing keys will be skipped)"
fi

# --- 7. Run the benchmark ---
echo ""
echo "Running benchmark..."
$PYTHON -m arena.runner

echo ""
echo "Done! Check arena/results/ for outputs."
