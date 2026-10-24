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
