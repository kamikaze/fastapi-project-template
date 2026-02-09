#!/bin/sh
set -e
H2_DIR="/opt/keycloak/data/h2"
IMPORT_DIR="/opt/keycloak/data/import"
echo "Checking for H2 database files..."
if [ ! -f "$H2_DIR/keycloakdb.mv.db" ]; then
    mkdir -p $H2_DIR
    echo "No existing H2 DB. Copying from import directory..."
    cp -r "$IMPORT_DIR/"* "$H2_DIR/"
else
    echo "H2 DB already exists, skipping copy."
fi

echo "Starting Keycloak..."
exec /opt/keycloak/bin/kc.sh start-dev
