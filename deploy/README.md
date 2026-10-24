# Deployment

`site/` is the preserved original release. Prepare a separate output directory
for each destination. The tools need Python 3.9+; validation also needs Node.js.
Neither is needed on the production webhost.

## Apache / LAMP shared hosting

For a domain root:

```bash
python3 tools/prepare_deployment.py --apache --origin https://research.example.org
python3 tools/verify_mirror.py --web-root build/public_html
```

Upload the **contents** of `build/public_html/` to the domain's document root.
Include `.htaccess`. Back up an existing site before replacing its files, and
enable HTTPS using your host's control panel. Typical permissions are 755 for
directories and 644 for files. No rewrites, database, PHP handler, or Node process
is needed. Local search reads the bundled JSON through the browser's HTTP fetch.

For `https://example.org/UD/`, use a fresh output directory:

```bash
python3 tools/prepare_deployment.py --output build/apache-UD --apache \
  --origin https://example.org --base-path /UD
python3 tools/verify_mirror.py --web-root build/apache-UD --base-path /UD
```

Upload that directory's contents into the host's `public_html/UD/`. The original
LAMP ZIP under `releases/lamp/` also includes a complete offline deployment kit.

Apache is not available in the preparation environment. If `.htaccess` causes a
500 response, inspect the host's error log; some hosts restrict MIME, header, or
directory-index directives. Have the host apply equivalent settings, or rename
the file temporarily to isolate the problem. `.py`, `.tex`, and `.md` research
artifacts are source-text downloads, not webhost applications.

## GitHub Pages

The manually triggered `.github/workflows/pages.yml` validates the original
mirror, prepares a `/UD-Site/` copy, validates that copy, uploads a Pages artifact,
and deploys it. It does not publish the LAMP ZIP, source code, or mirror tooling
as part of the website; those remain available in the repository.

One-time setup: in this repository's **Settings → Pages**, set the build source
to **GitHub Actions**. Then select **Actions → Publish GitHub Pages → Run
workflow**, using `main`. The workflow reports the actual deployed URL. A Pages
deployment is optional and separate from completing the repository mirror.

The default build expects the project path `/UD-Site/` under the owner's Pages
domain. For a future custom domain, update the workflow's explicit origin and
base path before deploying; no custom domain is configured by this import.

## External links and updates

External GitHub/ORCID/portal references retain their original destinations. Every
file shipped by the selected Sites release is mirrored; referenced external sites
are not recursively scraped. Standalone deployments receive updates only when
you deploy a later selected mirror version.
