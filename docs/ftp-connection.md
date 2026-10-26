# Blask FTPS connection in GitHub

Configured 26 October 2026 for `korzeniowskistudio-sys/blask`.

## Encrypted repository secrets

The following GitHub Actions repository secrets have been provisioned:

| Secret | Purpose |
| --- | --- |
| `BLASK_FTP_HOST` | IQHost FTP hostname |
| `BLASK_FTP_PORT` | FTP control port |
| `BLASK_FTP_USERNAME` | Existing approved FTP account |
| `BLASK_FTP_PASSWORD` | Saved account password |
| `BLASK_FTP_REMOTE_DIR` | Exact Blask document root |

Manage these in repository Settings → Secrets and variables → Actions. GitHub does not return stored secret values. They are available to authorized Actions jobs through the `secrets` context, not automatically to a Codex cloud checkout, Codespaces, or an ordinary local shell.

Example environment bindings for a future authorized workflow step:

```yaml
env:
  BLASK_FTP_HOST: ${{ secrets.BLASK_FTP_HOST }}
  BLASK_FTP_PORT: ${{ secrets.BLASK_FTP_PORT }}
  BLASK_FTP_USERNAME: ${{ secrets.BLASK_FTP_USERNAME }}
  BLASK_FTP_PASSWORD: ${{ secrets.BLASK_FTP_PASSWORD }}
  BLASK_FTP_REMOTE_DIR: ${{ secrets.BLASK_FTP_REMOTE_DIR }}
```

## Connection requirements

- Explicit FTPS on port 21, not implicit FTPS or SFTP.
- Require TLS, certificate and hostname validation, and a protected data channel (`PROT P`). Use passive mode.
- Host: `host92093.iqhs.pl`; account: `raf@host92093.iqhs.pl`.
- The FTP-visible upload root is `/domains/blask.korzeniowski.net/public_html`.
- Do not substitute `/home/host92093/...` for the verified FTP-visible path.
- The account also accesses other sites. Every upload must stay within the exact Blask root. Never deploy the whole repository, mirror/delete unrelated files, or change Dorado or shared hosting configuration.
- Never echo credentials, include them in command arguments, publish them to browser code, or commit them. Read the password from the job environment inside the FTP client.

## Verification and scope

Local read-only explicit-TLS login and CWD to the exact Blask root succeeded on 26 October 2026. Secret names were confirmed through the GitHub API after storage. No GitHub Actions FTP connection has been run, and passive data transfer from GitHub has not been verified.

This configuration does not create an automatic deployment workflow or publish any site files. A future deployment requires a selected, validated public build and an explicitly authorized workflow. Read `hosting-handover.md` for the hosting history.
