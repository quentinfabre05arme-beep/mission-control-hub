#!/bin/bash
# X Automation Runner
# Usage: ./run_automation.sh [command]

cd "$(dirname "$0")"

COMMAND=${1:-digest}

case $COMMAND in
    digest)
        python3 x_automation.py digest
        ;;
    tasks)
        python3 x_automation.py tasks
        ;;
    init)
        python3 x_automation.py init
        ;;
    cron-morning)
        # Send digest to Telegram
        python3 x_automation.py digest | telegram-send --stdin
        ;;
    cron-engagement)
        # Find engagement targets
        python3 x_automation.py tasks | jq '.engagement_tasks' | telegram-send --stdin
        ;;
    cron-metrics)
        # Track metrics
        python3 x_automation.py metrics
        ;;
    *)
        echo "Unknown command: $COMMAND"
        echo "Usage: $0 [digest|tasks|init|cron-morning|cron-engagement|cron-metrics]"
        exit 1
        ;;
esac
