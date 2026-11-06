# Performance & Reliability Code Review

Read this procedure at feature-cycle's review gate, after functional success and before temporary test cleanup and the final commit. When functional execution is blocked, a preliminary static review is useful but does not complete that gate.

## Scope and evidence

Review the entire feature against its recorded baseline, not just the latest commit or unstaged diff. Include new production files, staged and unstaged changes, and directly related callers/dependencies needed to establish execution frequency, ownership, and lifecycle. Exclude unrelated work. Follow the target project's actual Unity/package versions and architecture.

Use an independent reviewer with separate context when available and authorized; otherwise make an explicit second pass over the diff and related code. Do not require a new tool, dependency, or review skill.

Classify a finding as confirmed only when a concrete execution/ownership path or reproducible observation supports it. Explain assumptions and distinguish evidence from inference. A suspicious API or syntax alone is not enough. For uncertain impact, record a hypothesis and a measurement/reproduction plan, not a confirmed defect.

Do not claim zero GC allocations without profiling the relevant scenario or a reliable analysis of the specific complete execution path, including relevant callees. State the scope and limits of such analysis; it does not establish whole-frame or whole-game allocation freedom. Static evidence of an allocation does not by itself establish a measurable frame-time regression.

## Applicable categories

Inspect only categories relevant to the feature. Record a brief reason for omitted categories.

### A. GC and memory

- Repeated managed allocations on demonstrated hot paths, including boxing, captured closures, delegate creation, LINQ, temporary collections, strings, and arrays. Check actual frequency and compiler/runtime behavior before declaring an allocation.
- Unbounded caches, buffers, retained object graphs, and pooling capacity/ownership.
- Resource release on success, failure, cancellation, scene changes, and teardown: Addressables handles, native allocations, textures, meshes, materials, and other owned resources.
- Balance acquisition/release according to the actual API's ownership contract; do not release a shared handle or dispose memory while another owner/job still uses it.

### B. CPU performance

- Redundant work in `Update`, `FixedUpdate`, `LateUpdate`, and `ITickable`, plus frequently invoked callbacks.
- Repeated expensive Unity API calls, searches, queries, computations, and avoidable `Instantiate`/`Destroy` churn.
- Algorithmic complexity and scaling at realistic feature sizes.
- Safe caching that preserves invalidation, object lifetime, and behavior. Do not add pooling/caches without evidence; they can increase retention and complexity.

### C. Unity lifecycle and reliability

- Event subscription/unsubscription symmetry across enable/disable, destruction, scene changes, and reinitialization.
- `OnEnable`, `OnDisable`, `OnDestroy`, and async work that outlives its owner.
- Cancellation propagation (UniTask when adopted), completion after disposal, reentrancy, overlapping requests, and async races.
- Service reinitialization, resource cleanup on scene transitions, and Zenject binding/initialization/tick/disposal lifetimes when Zenject is present.
- Optional or destroyed Unity objects and genuine teardown states; do not add silent guards that conceal required wiring failures.

### D. UI and rendering

- Redundant UI writes, layout/graphic rebuilds, Canvas updates, and equivalent UI Toolkit invalidation.
- Overdraw and transparency risk in the affected rendering path; treat visual suspicion as a profiling hypothesis unless supported by stronger evidence.
- Potentially expensive shader operations, sampling, variant/pass changes, and pipeline/version compatibility.
- Material/resource changes, unintended material instances, batching/instancing implications, and ownership/release.
- Base recommendations on the active pipeline and target hardware. Compilation checks do not prove GPU cost; identify needed Frame Debugger or device profiling.

## Severity and finding format

Severity expresses impact and urgency, not confidence:

| Priority | Meaning |
| --- | --- |
| P0 | Critical blocker such as broadly triggered crashes, data loss, or resource exhaustion that makes the feature unusable. |
| P1 | Significant correctness, lifecycle, or performance defect on a supported scenario; must be fixed before ready-for-review status. |
| P2 | Bounded defect or evidenced inefficiency with lower urgency. Fix within scope when safe; otherwise document the concrete reason it remains and any acceptance impact. |

For every finding, record:

- Priority and confirmation state; file path and precise line, symbol, or code location.
- Problem and triggering conditions, including execution frequency or lifecycle sequence.
- Expected consequences and affected scenario, with measurements when available.
- Confidence and supporting evidence, distinguishing observed, source-proven, and inferred claims.
- A concrete fix or, for an unconfirmed risk, the next experiment needed to decide.
- Resolution and the affected tests/review rerun after a fix.

Do not invent a severity-worthy defect merely to populate the report. Put unconfirmed risks in a separate list even when their possible impact is high.

## Fix, recheck, and stop

1. Fix confirmed findings inside the feature's scope, preserving required behavior and resource ownership. Do not impose architecture patterns, pursue subjective Clean Code, or optimize cold paths without justification.
2. Add or extend a targeted temporary behavioral check, or use a concrete integration reproduction, that exercises each review-discovered defect's trigger. Show pre-fix failure where feasible and post-fix success; do not merely rerun checks that missed the trigger or write tests that mirror implementation. Rerun affected tests and relevant integration checks. Retain temporary tests while needed. If the trigger cannot be exercised, record the fix's verification as incomplete; static reasoning alone does not establish a successful runtime recheck.
3. Re-review changed areas and their affected callers/owners, including regressions introduced by the fix. Record what was resolved and what remains.
4. Allow at most three correction/recheck attempts per finding in this invocation unless the user specifies a different limit. Stop earlier if there is no progress. Reassess the cause before retrying an unsuccessful correction; do not reset the counter by relabeling the same unresolved issue. At the limit, stop automatic correction and report the unresolved finding and its impact on readiness. Unconfirmed hypotheses remain risks; do not make speculative changes to exhaust the budget.

Any unresolved confirmed P0/P1 finding blocks readiness. An out-of-scope confirmed problem should be reported without expanding the patch; if it prevents the feature meeting its criteria, report the feature blocked. A deferred P2 needs a reason and must not violate acceptance criteria.

Lack of profiling alone does not block a feature that does not require a performance measurement. It limits the claim to code-review evidence and leaves concrete manual follow-up. If acceptance requires a metric or device scenario, missing that evidence means verification is incomplete.

After this cycle, return to the skill for cleanup and final-tree verification. Production edits made during final verification must receive affected functional checks and review again. The skill's `Status.md` is the single report; do not create another review report by default.
