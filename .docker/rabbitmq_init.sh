#!/bin/bash

docker-entrypoint.sh rabbitmq-server &

# wait for RabbitMQ server to start
until rabbitmqctl wait /var/lib/rabbitmq/mnesia/rabbit\@$(hostname).pid
do
  echo "Waiting for RabbitMQ..."
  sleep 1
done

# Create the default user and password
rabbitmqctl add_user guest guest
rabbitmqctl set_user_tags guest administrator
rabbitmqctl set_permissions -p / guest ".*" ".*" ".*"

# create queues
rabbitmqadmin -u guest -p guest declare queue name=queue_prompts durable=true

# create exchanges
rabbitmqadmin -u guest -p guest declare exchange name=prompt type=direct

# create bindings
rabbitmqadmin -u guest -p guest declare binding source=prompt destination=queue_prompts routing_key=prompt.key-1

echo "Queues, exchanges, and bindings have been set up"

while true
do
  sleep 60
done
