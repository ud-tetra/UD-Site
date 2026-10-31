# Unified Dynamics — Public Research Atlas mirror

This repository preserves the public atlas, downloadable research artifacts,
original project source, and standalone LAMP deployment package.

**Current mirror:** Sites version **60**, source commit
`0337cb240a042c2dcabfb83b4d5564483d6c458b` (24 October 2026).
The authoritative public site is
[Unified Dynamics — Public Research Atlas](https://unified-dynamics-public.ben-w-mayes.chatgpt.site/).

The mirror contains **1,105 website files, including 50 HTML pages**, and all
**1,224 tracked upstream source files** through a lossless path mapping. There
are 36 PDFs and 46 existing ZIP downloads inside the website tree. The additional
standalone LAMP ZIP is preserved separately. No research content is rewritten
to create the mirror, and the original claim and provenance labels remain intact.

| Directory | Contents |
| --- | --- |
| [`site/`](site/) | Exact published `dist/` tree: pages, assets, data, papers, and downloads |
| [`source/`](source/) | All remaining upstream project files, including original generators/checks |
| [`releases/lamp/`](releases/lamp/) | Complete standalone LAMP deployment ZIP |
| [`deploy/`](deploy/) | Apache configuration and hosting instructions |
| [`manifests/`](manifests/) | Current pointer and immutable per-version provenance/hash manifests |
| [`reports/`](reports/) | Import and validation receipts |
| [`tools/`](tools/) | Repeatable import, validation, and deployment preparation |
| [`.github/workflows/`](.github/workflows/) | Push/PR validation and optional Pages deployment |

Start with the [mirror/sync plan](docs/MIRROR-SYNC-PLAN.md) and
[deployment instructions](deploy/README.md). The website is static: no database,
PHP, Node server, or visitor account is required. Python and Node are used only
by maintainers for preparation and verification.

## Validate a checkout

```bash
python3 tools/verify_mirror.py
```

Use Python 3.9+ and Node.js. Validation checks every managed file's SHA-256,
release ZIP integrity, local HTML links and anchors, JSON data, JavaScript syntax,
and literal browser data-fetch targets. It does not independently reprove the
scientific claims or execute historical imported research scripts.

## Prepare a standalone Apache deployment

```bash
python3 tools/prepare_deployment.py --apache --origin https://research.example.org
python3 tools/verify_mirror.py --web-root build/public_html
```

Upload the contents of `build/public_html/` to the domain document root. For a
subdirectory, add `--base-path /UD` and validate with `--base-path /UD`.
Generated files stay outside the exact mirror, under ignored `build/`.

## GitHub Pages

The optional **Publish GitHub Pages** workflow builds a separate `/UD-Site/`
deployment, validates it, and publishes only the website tree. It is manually
triggered; this repository's existence alone does not establish a live Pages URL.
Enable **Settings → Pages → Build and deployment → GitHub Actions**, then run the
workflow on `main`. See [deployment instructions](deploy/README.md#github-pages).

## Scope and provenance

The mirror is one-way: committed public Sites source → this repository. Source
changes originate upstream and arrive as a new declared version. The source path
mapping is `dist/X` → `site/X` and other paths → `source/<original path>`.
To reconstruct the original tree offline, copy `source/` into a separate working
directory and copy `site/` into its `dist/` subdirectory. Git history and missing
historical originals are not invented. External citations remain external.

This is a research publication mirror. Constructor checks, independent review,
and empirical evidence retain separate meanings. **Physical promotion: 0.**


## Program-wide predictive discovery policy - proposal 31 October 2026

[Canonical policy v1.0](https://github.com/ud-tetra/UD/blob/ff89221626d3258dc458f01408f1fac80a072530/docs/UD_PREDICTIVE_DISCOVERY_PROTOCOL_v1.0.md) is staged for review (SHA-256 `d5e5f079996863ae156a3d35e1cf8ba5135c2f7b8699bd9f9a4b492828351310`), and [this repository's adoption note](governance/UD_PREDICTIVE_DISCOVERY_ADOPTION_v1.0.md) governs the proposed README/boot changes. Exploratory FIT and novel observable candidates are allowed in source research, but no mathematical match becomes a physical prediction without independent bridge testing. This is a documentation-only GitHub PR: **the one-way managed site/source mirror, published Sites revision 60, and LAMP exports are unchanged.** Physical promotion 0.


## UD proof-first research rule (2026-10-31)

Read governance/UD_PROOF_FIRST_ADOPTION_v1.0.md before treating research claims as public scientific results. Mathematical proof statements, assumptions, no-go scope and verification records define progress; software/site release counts are not physical evidence. The managed site/source mirror remains unchanged by these governance edits. Physical promotion 0.
