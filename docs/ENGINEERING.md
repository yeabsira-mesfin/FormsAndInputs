# ProbeLab: engineering decisions

## Why a self-contained demo

A recruiter can run the application without a paid API account or external database. FastAPI owns authentication and policy enforcement; React renders typed API responses; SQLite provides transactions and queryable evidence. Model capabilities are optional and cannot extend application permissions.

## Identity and resource boundaries

Users authenticate with scrypt-hashed passwords. The browser receives a random opaque cookie; the database stores only its digest. Sessions expire after one hour and are revoked on logout or rotation. Tenant and role come from the server session rather than client parameters. Mutating requests require a same-origin custom header; only explicitly allowed origins pass.

## Evidence over claims

The dashboard benchmark evaluates deterministic policy fixtures, not a real language model. Direct and indirect injection checks measure heuristic blocking; they do not establish whether an LLM followed an attack. Five variations per template family are related samples, not independent evidence of generalization.

The held-out fixture run contains 50 attack cases and 10 legitimate cases. Its defended attack success rate is 20%, legitimate-task success is 50%, and false-positive rate is 50%. The intentionally vulnerable fixture has 100% attack success. These figures explain a deliberately limited control and must not be advertised as production or real-model security performance.

Reproduce the saved result:

```bash
python scripts/benchmark.py --gate benchmarks/policy-test.json
```

To test the actual Vaultwise API, start that project on port 8011, set `DEMO_PASSWORD` to its seeded password, then run:

```bash
python scripts/check_knowledge_api.py
```

The integration runner performs ten checks against the fixed loopback target. It does not accept arbitrary target URLs. Live LLM adversarial evaluation remains future work.

## Next engineering milestones

1. Move identity to OIDC with MFA and unique user provisioning.
2. Migrate the store to PostgreSQL with migrations and database-level tenant policies.
3. Add model-specific evaluation datasets and independent human review of generated answers.
4. Move ingestion and long jobs to durable workers with retries and idempotency keys.
5. Add structured observability, load tests, and production retention controls.

These milestones are not implemented. Describe only completed functionality when discussing the project in applications.
