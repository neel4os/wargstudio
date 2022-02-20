set -xv
set -euo pipefail

# export KIND_IMAGE_NAME=${KIND_IMAGE_NAME:-""}
export KIND_NODE_READY_TIMEOUT=${KIND_NODE_READY_TIMEOUT:-"10m"}
export REGISTRY_NAME=${REGISTRY_NAME:-"kind-registry"}
export REGISTRY_PORT=${REGISTRY_PORT:-"5001"}