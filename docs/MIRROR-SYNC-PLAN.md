# Mirror and synchronization plan

## Authority and direction

The public Sites project `appgprj_6acee9ef84dc81918f8143dc74e64657` is the upstream
publication source. `ud-tetra/UD-Site` is its independent GitHub mirror and
standalone deployment repository. This does not replace `ud-tetra/UD`, the broader
research repository, or the historical research portal.

Sync direction is **committed public Sites checkout → UD-Site**. Do not make
scientific amendments in the mirror. Make and publish them upstream first, then
import their declared version. An existing external-host copy is updated by
deploying a freshly generated build or the matching LAMP package.

## Initial baseline

| Field | Value |
| --- | --- |
| Sites version | 60 |
| Source commit | `0337cb240a042c2dcabfb83b4d5564483d6c458b` |
| Publication date | 24 October 2026 |
| Exact upstream tracked files | 1,224 |
| Published web files | 1,105 |
| HTML pages | 50 |
| LAMP package bytes | 90,522,398 |
| LAMP package SHA-256 | `9c59889ac92e113f95878faa1434e122dfe07a2d9a4720c99038b220e0d6a4e6` |

The baseline imports all upstream tracked files and the exact LAMP ZIP produced
for this publication. Existing website downloads stay at their original paths.
The only path changes are the lossless mapping of upstream `dist/` to `site/`,
and the remaining upstream files to `source/`.

## Repeatable procedure

1. Read repository instructions and the current pointer in
   `manifests/current.json`. Start from an updated `main` or a feature branch.
2. Retrieve the public Sites project's current metadata and saved version. Open
   its source through the Sites workflow, and check out the exact source commit
   associated with the selected saved version. Do not infer a version from a
   repository timestamp or from the HTML edition labels.
3. Confirm the upstream checkout has no uncommitted tracked changes. Review the
   tracked-file inventory for public scope. Only committed files are imported;
   untracked notebooks, caches, credentials, and environment files are excluded.
4. Produce the matching standalone LAMP package if this milestone includes one.
   Its embedded export manifest must match the selected version, source commit,
   and web-file hashes. Do not reuse an older archive for a newer source version.
5. Dry-run the importer from this repository's root:

   ```bash
   python3 tools/sync_from_source.py \
     --source /absolute/path/to/committed-sites-checkout \
     --site-version 60 \
     --lamp-archive /absolute/path/to/Unified-Dynamics-Public-Atlas-LAMP-v60-2026-10-24.zip
   ```

   Change version/archive arguments to the actual selected milestone. The
   archive flag is optional for milestones without a new LAMP package. For an
   identical repeat of a previously imported version, use the same archive
   argument originally recorded for that version.
6. Inspect the planned additions, changes, and removals. Repeat with `--apply` to
   copy the selected source into the managed trees and record immutable hashes.
   Path removals require `--allow-removals`; inspect them before using that flag.
   Prior version manifests and release archives are preserved.
7. Run `python3 tools/verify_mirror.py`. For a deployment, prepare a fresh ignored
   build with `tools/prepare_deployment.py` and validate that layout too.
8. Inspect `git diff --stat`, `git diff --check`, the manifest, and the receipt.
   Commit the complete import and its plan/validation updates together. Push
   normally, without force. Use a pull request if branch rules or review policy
   require it; never bypass required checks.
9. Read back the remote commit and manifest. Verify the remote `site/` and
   `source/` tree against the local commit. Check GitHub Actions results when
   available. Record any incomplete CI or deployment state explicitly.
10. Deploy the selected build to LAMP, or run the optional Pages workflow after
    Pages is enabled. A successful Git push is not proof of a successful webhost
    deployment.

## Layout and ownership

- Managed imports: `site/`, `source/`, `manifests/releases/sites-vN.json`.
- Current publication pointer: `manifests/current.json`.
- Immutable downloadable exports: `releases/lamp/`.
- Maintainer-owned files: this plan, root README/AGENTS, tools, deployment config,
  workflows, and mirror verification reports.
- Disposable generated files: `build/` and `reports/local-*.json`, ignored by Git.

The importer refuses version rollback and changing the contents of an existing
version manifest. Reimporting the identical version is idempotent. An authorized
content correction needs a new source version. Ordinary Git history retains
previous changed/deleted files, while old version manifests identify their hashes.

## Validation boundary

Validation covers exact byte preservation, inventory completeness, archive CRC,
local page links and anchors, JSON parsing, JavaScript syntax, and local browser
data inputs. A generated subdirectory deployment changes HTML navigation, the
shared JavaScript fetch/link mapper, sitemap/robots, and deployment-only marker
files; scientific downloads and JSON records remain unchanged.

The original LAMP export includes a browser smoke-test receipt for `/UD/`.
Apache configuration was not executed in the export environment. Scientific
proofs are not rerun by mirror CI. Missing source labels, historical statements,
and independent-review status remain those of the original publication.

## Cadence and release handling

Sync at published milestone increments or on explicit request. No unattended
polling, scheduled source pull, or recurring automation is installed by this
initial sync. Push/PR CI validates only commits already submitted to this repo.

Keep the initial exact LAMP ZIP in `releases/lamp/`. As the release collection
grows, use GitHub Release assets for large future packages and retain immutable
checksums/asset references in version manifests; adapt the importer/validator
together before changing that storage policy. Do not silently remove old exports.

## Recovery

If validation fails, keep the failed change off the publication branch, identify
the mismatch, and repeat the import from the selected source commit. Restore a
past publication by reverting the complete mirror commit through the normal Git
workflow. Historical version manifests remain immutable. Never force-reset a
shared branch or infer missing artifacts from old generated previews.
