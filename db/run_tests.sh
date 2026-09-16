#!/usr/bin/env bash
# M0 exit test -- runs entirely inside an ephemeral Postgres container.
# No host Postgres, no drivers, nothing to install but Docker.
#
#   ./db/run_tests.sh
#
# Exit 0 = tenant isolation holds. Non-zero = do not ship.

set -euo pipefail

CONTAINER="truelearn-dbtest-$$"
IMAGE="postgres:16-alpine"
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Preserve the real exit status through the trap. Without the explicit `exit $status`,
# the `|| true` below becomes the script's status and a failed run reports success --
# observed 2026-09-16: `docker run` died with "unexpected EOF" and this script exited 0.
# A test harness that cannot fail is worse than no test harness.
cleanup() {
  local status=$?
  docker rm -f "$CONTAINER" >/dev/null 2>&1 || true
  exit $status
}
trap cleanup EXIT

# Pull separately, with retries, so a flaky network is distinguishable from a real test
# failure. Conflating the two is how a broken run gets read as a broken product.
if ! docker image inspect "$IMAGE" >/dev/null 2>&1; then
  echo "pulling $IMAGE ..."
  for attempt in 1 2 3; do
    if docker pull "$IMAGE"; then break; fi
    echo "  pull attempt $attempt failed; retrying..."
    [ "$attempt" = 3 ] && { echo "ERROR: could not pull $IMAGE"; exit 2; }
    sleep 5
  done
fi

echo "starting $IMAGE ..."
docker run -d --name "$CONTAINER" \
  -e POSTGRES_PASSWORD=test -e POSTGRES_DB=truelearn \
  "$IMAGE" >/dev/null

# Wait for readiness rather than sleeping a guessed number of seconds.
for _ in $(seq 1 60); do
  if docker exec "$CONTAINER" pg_isready -U postgres -d truelearn >/dev/null 2>&1; then
    break
  fi
  sleep 0.5
done
docker exec "$CONTAINER" pg_isready -U postgres -d truelearn >/dev/null

run_sql() {
  docker exec -i "$CONTAINER" psql -v ON_ERROR_STOP=1 -U postgres -d truelearn -q < "$1"
}

echo "applying 001_schema.sql ..."
run_sql "$HERE/001_schema.sql"

echo "running 002_isolation_test.sql ..."
run_sql "$HERE/002_isolation_test.sql"
