#!/usr/bin/env bash
set -euo pipefail

echo "Will launch Local registry if not exists already"

reg_name=${REGISTRY_NAME}
reg_port=${REGISTRY_PORT}
if [ "$(docker inspect -f '{{.State.Running}}' "${reg_name}" 2>/dev/null || true)" != 'true' ]; then
  docker run \
    -d --restart=always -p "127.0.0.1:${reg_port}:5000" --name "${reg_name}" \
    registry:2
fi
kind create cluster --config config.yaml
source ./local-registry.sh
kubectl get nodes
kubectl wait --for=condition="Ready" nodes --all --timeout=${KIND_NODE_READY_TIMEOUT}

