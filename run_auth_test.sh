#!/bin/bash

echo "📦 Setting PYTHONPATH and running FitTrack authentication tests..."

# Set PYTHONPATH to project root (where `app` lives)
export PYTHONPATH=$(dirname "$0")

# Run tests using Python 3.10
python3.10 -m pytest -v tests/test_auth.py

if [ $? -eq 0 ]; then
    echo "✅ All authentication tests passed successfully."
else
    echo "❌ Some authentication tests failed. Please review the output above."
fi
