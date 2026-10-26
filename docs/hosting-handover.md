# Blask hosting handover

Recorded 26 October 2026 from the user's local IQHost setup conversation
(source thread: 01a177f6-0141-7fd3-ac20-492e50fc4283).
These are reported local-panel and local FTPS observations, not independent cloud verification.

## Provisioned subdomain

- Hostname: blask.korzeniowski.net
- Created through IQHost dashboard → service host92093.iqhs.pl → DirectAdmin → korzeniowski.net → Subdomains.
- DirectAdmin confirmed “Subdomena została utworzona” and listed the entry.
- Document root shown: /domains/blask.korzeniowski.net/public_html
- Absolute server root: /home/host92093/domains/blask.korzeniowski.net/public_html
- Server IP shown by panel: 195.117.36.230
- No Blask files uploaded. DNS and HTTPS have not been independently verified.

## Verified local file-transfer route

Updated 26 October 2026 from the same local setup conversation. The user
requested reuse of the existing FTP account; the dedicated-account plan is
cancelled. No new FTP account was created.

- FTP hostname: host92093.iqhs.pl
- Account: raf@host92093.iqhs.pl
- Port: 21
- Explicit FTP over TLS (FTPS), passive mode.
- Local read-only verification succeeded with certificate verification and a
  protected data channel. Keep certificate and hostname verification enabled.
- Verified remote command: CWD /domains/blask.korzeniowski.net/public_html
- No remote files changed during verification.
- The existing password remains exclusively in the Mac's private FileZilla
  configuration at ~/.config/filezilla/sitemanager.xml. This cloud session
  cannot read that local file. Do not copy its contents into chat, repository
  files, scripts, or logs.
- Use the verified remote path above; do not substitute the absolute server
  path or assume this account is jailed to Blask. Account isolation was not
  established by the successful CWD check.
- The separate master account host92093 is not the selected deployment account.

## Cloud credential mechanism checked

The environment configuration tools expose secret requirements with secure value
entry in environment settings. These are proxy-backed secrets for specified
HTTPS destinations. They are not documented as raw passwords available to a
local FTP client, and explicit FTPS on port 21 is not HTTPS.

Consequently, this exposed mechanism does not establish usable FTPS credential
injection. Do not configure an HTTPS proxy secret and claim FTPS is ready, and do
not place passwords in ordinary variable suggested values, chat, project files,
or deployment scripts.

At handover recording, the configuration reports no secrets or runtime variable
requirements, and no IQHOST-, BLASK-, or FTP-related exported variable names were
present. No configuration fields or secret requirements were changed.

No additional secure FTPS credential provisioning tool was found on the update.
The current deployment route is local deployment from the Mac using the
existing FileZilla account. Direct cloud FTP is not ready. If cloud deployment
is later needed, first establish a supported secure raw-credential injection
mechanism and verify FTPS network access, including passive data connections.
Do not request a password in chat.

## Deployment boundary and pending work

- All future uploads must stay within Blask's document root.
- Do not alter Dorado, other sites, shared hosting settings, or email services.
- This handover alone does not authorize publication or uploading files.
- Local read-only FTPS access and the Blask remote directory are verified as
  reported above; no further account provisioning is planned.
- Pending: DNS and HTTPS checks and separately authorized local publication of
  the selected Blask files. Limit every deployment operation to the verified
  Blask directory, regardless of other paths accessible to this account.

## Later credential handover and current status

After the earlier entries, the local setup chat delivered the existing FTP
password and ElevenLabs API key at the user's request. Neither value is saved
in this repository or portable backup. ElevenLabs was subsequently used for the
authorized audio generations. Cloud FTPS was not verified or used to deploy.
The earlier “no credentials transferred” observations are historical, not the
latest conversation state. A fresh task must use secure provisioning or the
Mac's private setup, not assume credentials are present in its environment.

## GitHub Actions credential provisioning — 26 October 2026

At the user's request, the existing FTPS connection was configured as five encrypted GitHub Actions repository secrets: `BLASK_FTP_HOST`, `BLASK_FTP_PORT`, `BLASK_FTP_USERNAME`, `BLASK_FTP_PASSWORD`, and `BLASK_FTP_REMOTE_DIR`. Presence was verified after storage. See [FTP connection instructions](ftp-connection.md). The password is not in tracked files. Actions secrets do not provision credentials into an ordinary Codex cloud session. No deployment workflow was created or run, and no website files were uploaded in this step.
