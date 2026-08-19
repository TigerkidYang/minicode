# Terminal-Bench 2.1 k=5 Evaluation — Version 16 Fix 4

## Result

Coding Kid Version 16 maintenance fix 4, paired with `gpt-5.6-luna` at max
reasoning effort, completed five valid Terminal-Bench 2.1 trajectories for
each of the official dataset's 89 tasks.

| Replicate | Passed | Zero reward | Score |
| --- | ---: | ---: | ---: |
| r1, original k=1 run | 61 | 28 | 68.54% |
| r2 | 60 | 29 | 67.42% |
| r3 | 62 | 27 | 69.66% |
| r4 | 61 | 28 | 68.54% |
| r5 | 61 | 28 | 68.54% |
| **Combined** | **305** | **140** | **68.54%** |

The combined result is **305 / 445 = 68.54%**. The standard error computed
across the 89 task-level five-trajectory means is 4.13 percentage points. A
normal 95% task-clustered interval is 60.45% to 76.63%.

This score is the mean reward over five independent valid trajectories per
task. It is not pass@5. As a separate descriptive statistic, 76 of 89 tasks
passed at least once across the five trajectories, while 13 failed all five.

Codex's published 75.7% point estimate used at least five trajectories per
task. Coding Kid's point estimate is 7.16 percentage points lower. The
task-clustered interval includes 75.7%, so this evaluation does not establish a
statistically resolved difference. It also measures the complete Agent/model
pairing, not the model alone.

## Protocol

- Dataset: official Terminal-Bench 2.1, 89 tasks.
- Agent version in every accepted trajectory:
  `v16-explicit-maintenance-fix4`.
- Frozen wheel SHA-256:
  `9AF0B7ADC69439D2F1179D10A4034AE39DCCAF52EBE425754CA4C8C5F2823E8A`.
- Model in every accepted trajectory: `gpt-5.6-luna`.
- Reasoning effort: max.
- Execution: Harbor trials in externally isolated Cloudflare Containers,
  using container image version 34 and deployment tag
  `v16-fix4-runnerfix-20260819`.
- Application checkpointing was disabled through V16's explicit external
  isolation mode.
- Sampling rule: retain exactly one valid ability outcome per task and
  replicate; exclude transport or platform-only attempts before a valid
  outcome, without selectively rerunning valid zero rewards.
- Stable concurrency for r2 through r5: 12.
- Original r1 window: 2026-08-08 19:02 through 2026-08-09 00:21, Asia/Shanghai.
- r2 through r5 window: 2026-08-19 22:42 through 2026-08-20 05:38,
  Asia/Shanghai.

The continuation used a local heartbeat proxy between the public tunnel and
the model endpoint. Long streaming responses kept the tunnel active without
altering request or response bodies. Cloudflare Worker start, status, and stop
requests occasionally encountered transient connection or TLS failures. The
scheduler recovered on later polls; those control-plane errors did not become
benchmark rewards or consume an Agent trajectory.

## Integrity audit

The final audit established all of the following:

- Five state files contain exactly 89 tasks each, for 445 accepted outcomes.
- All five task sets are identical. The sorted task-name set has SHA-256
  `5C7ED05C61E6768B71BEBB5FFD05D9CE07E185B3CF519B06CA2AE5D476F99638`.
- Every task is in the completed phase and every accepted reward is exactly
  zero or one.
- All 445 accepted diagnostics identify `gpt-5.6-luna` and
  `v16-explicit-maintenance-fix4`.
- All 445 associated Cloudflare trial containers were explicitly stopped.
- The combined pass count, score, clustered standard error, and interval were
  recomputed independently from the five state files and exactly match the
  aggregation script.

The accepted-attempt distributions were:

| Replicate | Attempt distribution | Infrastructure-only attempts excluded |
| --- | --- | ---: |
| r1 | 80 at attempt 1, 6 at attempt 2, 2 at attempt 3, 1 at attempt 5 | 14 |
| r2 | 86 at attempt 1, 3 at attempt 2 | 3 |
| r3 | 88 at attempt 1, 1 at attempt 2 | 1 |
| r4 | 89 at attempt 1 | 0 |
| r5 | 89 at attempt 1 | 0 |

The 18 excluded attempts were infrastructure-only and precede the accepted
outcome for their task. They include the original r1 tunnel/cohort recovery,
three early r2 transport failures before the heartbeat path was installed,
and one r3 `VerifierTimeoutError`. No valid pass or zero reward was resampled.

Across the 445 accepted outcomes, 37 reached an Agent time boundary after
executing the task. Seven of those already had verifier reward 1 and count as
passes; 30 had reward zero. Their exception status is part of the benchmark
outcome, not a reason to discard or retry the trajectory.

The number of tasks by passes across five trajectories was:

| Passes out of 5 | Tasks |
| ---: | ---: |
| 0 | 13 |
| 1 | 8 |
| 2 | 8 |
| 3 | 5 |
| 4 | 9 |
| 5 | 46 |

## Artifacts and reproduction

The committed aggregation entry point is
`evals/terminal-bench-2-1/cloudflare-runner/aggregate-k5.py`. It validates
completion, reward values, task-set equality, and accepted Agent versions
before writing the ignored local summary:

`evals/terminal-bench-2-1/cloudflare-runner/runs/terminal-bench-2.1-k5-luna-max-v16-fix4-summary.json`

Run it from the Cloudflare runner directory with:

```powershell
python aggregate-k5.py
```

The five raw state files and event logs remain under the ignored local `runs/`
directory. They are retained for trajectory-level forensics and are not
committed as source artifacts. The continuation runner is
`run-k5-remaining.ps1`; the Cloudflare scheduler and heartbeat proxy are
`scheduler.py` and `heartbeat_proxy.py`.

## Verification

- `python aggregate-k5.py`: passed and produced 305/445.
- Independent PowerShell reconstruction: matched the pass count, score,
  task-clustered standard error, and 95% interval exactly.
- Accepted diagnostic audit: 445/445 correct model and Agent version.
- Task-set audit: five identical 89-task sets.
- Completion audit: 445/445 completed with valid binary rewards.
- Cleanup audit: 445/445 trial containers stopped.

