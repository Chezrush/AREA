#!/usr/bin/env bash
#
# Reproducible 3-language benchmark (Go / Rust / Python) for the AREA back-end
# technology selection. Builds each service, runs an identical k6 load profile
# against it on the same machine, and records throughput, latency and memory.
#
# Usage:  ./run.sh [go rust python]   (default: all three)
#
set -u

HERE="$(cd "$(dirname "$0")" && pwd)"
NET="area-bench-net"
HOST_PORT=18080
RESULTS="$HERE/results"
LOAD="$HERE/load"

NPROC="$(docker run --rm alpine nproc 2>/dev/null || echo 4)"
echo ">> Containers will see NPROC=$NPROC cores"

mkdir -p "$RESULTS"
docker network rm "$NET" >/dev/null 2>&1 || true
docker network create "$NET" >/dev/null

SERVICES=("${@:-go rust python}")
# shellcheck disable=SC2206
SERVICES=(${SERVICES[@]})

build_and_run() {
    local lang="$1"
    local ctx="$HERE/services/$lang"
    local img="area-bench-$lang"
    local cname="svc-$lang"
    local extra_env=()

    if [ "$lang" = "python" ] || [ "$lang" = "ts" ]; then
        extra_env=(-e "WEB_CONCURRENCY=$NPROC")
    fi

    echo ""
    echo "============================================================"
    echo ">> [$lang] building image..."
    echo "============================================================"
    if ! docker build -t "$img" "$ctx"; then
        echo "!! [$lang] build FAILED"; return 1
    fi

    docker rm -f "$cname" >/dev/null 2>&1 || true
    echo ">> [$lang] starting container..."
    docker run -d --name "$cname" --network "$NET" \
        -p "$HOST_PORT:8080" ${extra_env[@]+"${extra_env[@]}"} "$img" >/dev/null

    # Wait for health
    echo -n ">> [$lang] waiting for health"
    local ok=0
    for _ in $(seq 1 60); do
        if curl -fs "http://localhost:$HOST_PORT/health" >/dev/null 2>&1; then ok=1; break; fi
        echo -n "."; sleep 1
    done
    echo ""
    if [ "$ok" -ne 1 ]; then
        echo "!! [$lang] service never became healthy"; docker logs "$cname" | tail -20
        docker rm -f "$cname" >/dev/null 2>&1; return 1
    fi

    # Background memory sampler -> max MiB
    local memfile; memfile="$(mktemp)"
    ( while true; do
        docker stats --no-stream --format '{{.MemUsage}}' "$cname" 2>/dev/null \
          | awk '{print $1}' | sed 's/MiB//; s/GiB/*1024/' | bc 2>/dev/null >> "$memfile"
        sleep 2
      done ) &
    local sampler=$!

    echo ">> [$lang] running k6..."
    docker run --rm --network "$NET" \
        -v "$LOAD:/load:ro" -v "$RESULTS:/results" \
        -e "SERVICE_URL=http://$cname:8080/similarity" \
        -e "SERVICE=$lang" \
        grafana/k6:latest run /load/script.js

    kill "$sampler" >/dev/null 2>&1 || true
    local maxmem; maxmem="$(sort -n "$memfile" 2>/dev/null | tail -1)"
    echo "{\"max_mem_mib\": ${maxmem:-0}}" > "$RESULTS/$lang.mem.json"
    echo ">> [$lang] peak memory: ${maxmem:-?} MiB"
    rm -f "$memfile"

    docker rm -f "$cname" >/dev/null 2>&1 || true
}

for s in "${SERVICES[@]}"; do
    build_and_run "$s" || echo "!! [$s] skipped due to error"
done

docker network rm "$NET" >/dev/null 2>&1 || true
echo ""
echo ">> Done. Raw summaries in $RESULTS/"
