param(
    [int]$FirstReplicate = 2,
    [int]$LastReplicate = 5
)

$ErrorActionPreference = "Stop"

if (-not $env:CODING_KID_BENCH_API_KEY) {
    throw "CODING_KID_BENCH_API_KEY is required"
}
if (-not $env:CODING_KID_BENCH_MODEL_URL) {
    throw "CODING_KID_BENCH_MODEL_URL is required"
}
if ($FirstReplicate -lt 2 -or $LastReplicate -gt 5 -or $FirstReplicate -gt $LastReplicate) {
    throw "Replicate range must be within 2..5"
}

$runnerRoot = $PSScriptRoot
$env:CODING_KID_BENCH_USE_BOOTSTRAP = "0"
$env:CODING_KID_BENCH_INITIAL_CONCURRENCY = "8"
$env:CODING_KID_BENCH_MAX_CONCURRENCY = "12"
$env:CODING_KID_BENCH_ADOPT_INTERRUPTED = "0"
$env:CODING_KID_BENCH_RESET_HARNESS_REPAIRS = "0"
$env:CODING_KID_BENCH_RESOLVE_IP = ""

foreach ($replicate in $FirstReplicate..$LastReplicate) {
    $env:CODING_KID_BENCH_REPLICATE = "$replicate"
    $env:CODING_KID_BENCH_RUN_ID = "terminal-bench-2.1-k5-luna-max-v16-fix4-r$replicate"
    $env:CODING_KID_BENCH_TRIAL_PREFIX = "k${replicate}v16f4"

    & python (Join-Path $runnerRoot "scheduler.py")
    if ($LASTEXITCODE -ne 0) {
        throw "Replicate $replicate stopped with scheduler exit code $LASTEXITCODE"
    }
}
