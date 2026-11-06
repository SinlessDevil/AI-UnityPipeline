---
name: feature-cycle
description: Complete a Unity feature in a dedicated branch with functional tests, mandatory Performance & Reliability Code Review, scoped fixes, temporary test cleanup, and a Markdown status report. Use when asked to implement a feature through this workflow; not for a question, standalone review, documentation-only toolkit maintenance, or running existing tests alone.
---

# Feature Cycle

Implement the requested Unity feature and leave a verified branch and status report for review. Invoking this skill requests the whole workflow, including temporary tests, necessary Editor-created test resources, review, fixes, cleanup, and reporting. This overrides optional-testing defaults, not explicit current user restrictions or environment permissions.

## Context and branch

- Accept requirements from the message, established context, or referenced task. Reuse known architecture; inspect only missing context and affected code.
- Confirm this is the intended Unity project. Read its local rules, pinned Editor version, actual packages/pipeline, Git status, and branches. Do not apply this workflow's Unity execution steps to the AI-UnityPipeline toolkit itself.
- Define observable acceptance criteria and relevant verification. Make reasonable implementation decisions and record assumptions. Ask only when missing information prevents determining required behavior.
- Create `feature/<short-name>` from the specified base or actual integration branch. Use `dev` only where established; otherwise use the established alternative. Preserve unrelated work, isolating in a worktree when necessary. Inspect a same-task branch before continuing it; do not overwrite another task's branch.
- Record the starting revision and relevant pre-existing changes so review can cover the entire feature, including committed, staged, unstaged, and new files, without including unrelated work.
- Use `Docs/Features/<short-name>/Status.md` unless the project or user specifies another path. Put production code in its architectural folders. Track temporary files and test side effects so cleanup removes only this invocation's artifacts.

## Functional implementation and verification

1. Implement the agreed behavior using the target project's architecture and existing packages; avoid unrelated audits or refactoring.
2. Write temporary behavioral checks for acceptance criteria and likely regressions. Use EditMode for suitable logic; use PlayMode/Editor checks and gameplay smoke checks for input, animation, scenes, Addressables, and lifecycle behavior as applicable. Verify real composition and transitions when changing DI or states.
3. Run the pinned Unity version through available Editor/CLI/MCP controls or batch mode. Preserve an existing Editor session and unsaved work. Do not close another project to make testing easier.
4. Save fresh results and logs per run in a temporary location. For test suites, inspect XML counts, outcomes, skips, and process status; for Editor smoke checks, capture the actual actions and observations. A zero exit code alone is not evidence that checks ran.
5. Inspect compilation errors, exceptions, and unexpected runtime errors. Associate expected negative-test errors with their tests; do not globally suppress log checks. Assess relevant warnings.
6. Fix causes and rerun affected checks. Run an appropriate existing suite and integration scenario before the review gate. Do not weaken assertions, disable tests, or change expectations merely to pass; update obsolete expectations only for agreed behavior changes.

Proceed to the mandatory review gate after functional success. If execution is blocked, record failed or unrun checks and preserve the work; a useful static review may still be performed but cannot substitute for functional verification. Stop repeating a failure when no new evidence or remedy makes progress possible.

## Mandatory Performance & Reliability Code Review

Before removing temporary tests or making the final commit, read [the review procedure](references/performance-reliability-review.md) and apply it to every relevant changed production path. Review only applicable GC/memory, CPU, Unity lifecycle/reliability, and UI/rendering categories, with directly related callers and dependencies needed to understand behavior.

Prefer an available, authorized independent reviewer with separate context. Provide the feature baseline, complete diff/new files, relevant raw code, acceptance criteria, and actual test evidence; request review only, without leading it toward an intended conclusion. If independent review is unavailable or unauthorized, explicitly perform a second pass over the complete feature diff and related code yourself. Record the review method and coverage.

For confirmed in-scope findings, preserve behavior while fixing them, exercise each defect's trigger with a targeted temporary check or integration reproduction, rerun affected functional checks, and review the changed areas again. Do not remove temporary tests until this cycle is complete. Do not implement speculative optimizations to make the review look clean. Apply the procedure's three-attempt limit per finding and stop sooner without progress; record unresolved findings, unavailable validation, and blockers.

## Temporary test cleanup and final verification

- After functional success and the review/fix cycle, preserve evidence and remove only tests, helper files, Editor-created temporary resources, and their associated `.meta` files created solely for this invocation. Keep them if the user explicitly requests retention, including valuable regression tests.
- Never delete existing tests. Remove only temporary methods added to them; retain necessary expectation updates and useful harness fixes. Restore test-induced content, settings, and user progress without reverting unrelated changes.
- If blocked before these gates, preserve needed temporary checks for diagnosis and list them in the report; restore harmful test side effects regardless. Do not claim cleanup or success when it did not happen.
- After cleanup, recompile the final project and run suitable remaining tests or a smoke check. Verify production code does not depend on removed helpers and record final-tree results separately. If unavailable, mark final verification incomplete.
- If final verification exposes a defect, return to affected functional checks and review before completion. Recreate temporary checks only as needed, then clean up and verify again. Apply the same no-progress stopping rule.
- Inspect the complete final diff and file inventory for temporary artifacts, unrelated edits, and test-induced asset changes.

## Status and completion

Create or update one `Status.md` in the user's language, concise and factual:

- **Status and scope:** ready for review, partially completed, or blocked; requirements, assumptions, branch/base, and reviewed revision/diff scope.
- **Functional verification results:** Editor version, suites/scenarios actually run, pass/fail/skip counts where applicable, compilation/log results, and evidence paths. Mark unrun checks explicitly.
- **Performance review results:** reviewer or second-pass method, applicable categories and inspected paths, findings and evidence. Say "no confirmed findings in the reviewed scope" where accurate; never imply measured performance from static review.
- **Fixed P0/P1/P2 findings:** location, trigger, impact, confidence/evidence, and fix; distinguish unresolved confirmed findings from unconfirmed performance risks.
- **Recheck after fixes:** affected tests rerun, their actual results, and follow-up review outcome.
- **Cleanup and final state:** temporary artifacts removed or explicitly retained, restored side effects, and post-cleanup compilation/tests/smoke results.
- **Limits and manual actions:** unavailable Editor/profiling/device checks and concrete remaining Unity Profiler, Frame Debugger, or device scenarios. Include a metric and acceptance target when specified by the task; do not invent thresholds.

Use "ready for review" only when functional checks, mandatory review/fixes, and final-tree verification have completed with no unresolved P0/P1 findings or unmet acceptance criteria. Unconfirmed performance hypotheses alone do not fail review, unless the task requires a measurement that has not been obtained; list justified follow-up work. Record any unresolved P2 finding and why it remains. Missing mandatory execution makes the status partial or blocked, even when static review found no issue.

On success, commit only intended changes and the report on the feature branch using project conventions. If blocked, preserve work and the report without marking the feature ready. Leave the branch for review; push, PR creation, and merge require separate task authorization. The final response gives the branch, report path, verification/review outcomes, and significant limits.
