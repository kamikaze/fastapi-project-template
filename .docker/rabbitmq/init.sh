#!/bin/bash
set -euo pipefail

rabbitmq-server &

echo "Waiting for RabbitMQ to be fully started..."

# ✅ Correct readiness check
until rabbitmqctl await_startup
do
  sleep 1
done

echo "RabbitMQ fully started. Importing definitions..."

rabbitmqctl import_definitions /etc/rabbitmq/definitions.json

echo "Definitions imported successfully."

wait
