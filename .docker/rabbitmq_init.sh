#!/bin/bash
set -e # Exit immediately if a command exits with a non-zero status.

# Start the original entrypoint logic. This runs setup and then starts the server in the background.
# NOTE: We use the rabbitmqctl command *after* the server is fully up.

# 1. Wait for RabbitMQ server to be fully available inside the container.
# The server is started by the default Docker ENTRYPOINT (which you are overriding with this script).
# We must ensure we start the rabbitmq-server process first, or let the Docker ENTRYPOINT start it.

# **CRITICAL CHANGE:** We use `rabbitmq-server -detached` temporarily
# to run the setup commands, then stop it, and finally restart it in the foreground.
# Alternatively, use `rabbitmq-server` directly and run setup in the background.

# --- Recommended Robust Setup ---

# Run setup commands in the background and wait for the node to be ready
rabbitmq-server -detached

echo "Waiting for RabbitMQ to come online..."
until rabbitmqctl node_health_check
do
  sleep 1
done

echo "RabbitMQ node is ready. Running setup..."

# 2. Run Setup Commands
#rabbitmqctl add_user guest guest
rabbitmqctl set_user_tags guest administrator
rabbitmqctl set_permissions -p / guest ".*" ".*" ".*"

# Using rabbitmqadmin for creating entities
rabbitmqadmin declare queue name=queue_a durable=true
rabbitmqadmin declare queue name=queue_b durable=true
rabbitmqadmin declare exchange name=xchg_queues type=direct
rabbitmqadmin declare binding source=xchg_queues destination=queue_b routing_key=route_b

echo "Queues, exchanges, and bindings have been set up."

# 3. Stop the detached server
rabbitmqctl stop

# 4. CRITICAL: Restart RabbitMQ in the FOREGROUND, replacing the shell process.
echo "Restarting RabbitMQ in the foreground..."
exec rabbitmq-server
