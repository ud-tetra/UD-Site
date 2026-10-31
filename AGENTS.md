# UD-Site mirror rules

This repository mirrors the Unified Dynamics public atlas. `site/` and `source/`
are managed imports from a committed Sites source checkout, mapped by the current
manifest. Do not edit scientific content in the mirror. Correct it upstream and
sync a new declared version. Preserve original claim labels and download bytes.

Read `docs/MIRROR-SYNC-PLAN.md` before a sync. Use `tools/sync_from_source.py` in
dry-run mode, then apply, validate, and inspect the diff. Removed upstream paths
require the explicit `--allow-removals` flag. Preserve prior immutable manifests
and release archives. Never import credentials, private notes, local caches, Git
metadata, or environment files. Keep deployments in ignored `build/` directories.

Run `python3 tools/verify_mirror.py` before pushing. Node.js must be available for
JavaScript syntax validation. Do not run historical scientific build scripts as
part of a mirror update. An automated mirror check is not independent review of
the research. Physical promotion remains 0.


## Predictive-discovery governance proposal (2026-10-31)

Read `BOOTLOADER.md` and `governance/UD_PREDICTIVE_DISCOVERY_ADOPTION_v1.0.md` before proposing observables. Permit labeled discovery FIT and candidate hypotheses; do not promote physical identifications without a source-complete observable and independent test. These are repository-level governance documents outside the managed `site/` and `source/` trees; do not edit or resync those without an upstream Sites source receipt. Effective adoption awaits PR review/merge; physical promotion 0.


## UD proof-first research rule (2026-10-31)

Read governance/UD_PROOF_FIRST_ADOPTION_v1.0.md before treating research claims as public scientific results. Mathematical proof statements, assumptions, no-go scope and verification records define progress; software/site release counts are not physical evidence. The managed site/source mirror remains unchanged by these governance edits. Physical promotion 0.
