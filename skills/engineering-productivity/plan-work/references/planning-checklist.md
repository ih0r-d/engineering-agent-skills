# Implementation Planning Checklist

| Stage | Evidence |
| --- | --- |
| Baseline | Current behavior, relevant tests, supported environment. |
| Change | Affected entrypoints, contracts, data, configuration. |
| Sequence | Dependencies, compatibility windows, reversible steps. |
| Verification | Focused checks mapped to acceptance criteria. |
| Recovery | Stop conditions and safe recovery for risky changes. |

## Gotchas

- A database migration and application rollback may have different recovery paths.
- A passing baseline does not prove coverage of the changed contract.
- Avoid planning new infrastructure when a localized change meets requirements.
- Separate unknown implementation details from confirmed repository evidence.
