# Continue Blask

Handover prepared 26 October 2026 from the “Set up blask” conversation.
This repository contains the work, decisions, and next steps; it is not a full
transcript. No credentials are included.

## Continuation update — 26 October 2026

The Biruta source import is complete in
`content/sources/001-reflective-larch-pattern.md` and its JSON companion.
The user approved audio v3 and requested publication of the work-in-progress
page at **blask.korzeniowski.net**, including original photos, the approved
animation, and sound. The public build is in `site/`. Read
`docs/wip-site-handover.md` and `docs/ftp-connection.md` for deployment.
The earlier pending-import and Mac-only deployment notes below describe the
original handover; the GitHub Actions secrets are the newer deployment route.

## User's goal and current priority

Build Blask, a reflective outdoor clothing brand focused mainly on cyclists.
The eventual ambition includes a shop, but the chosen first stage is a brand
landing page and visual design. There is no completed shop or landing page yet.

The immediate unfinished request is to extract the original text from:
https://biruta.korzeniowski.net/portfolio_page/reflective-larch-pattern/
and store it as the first source data for the new website. A pending record
exists at content/sources/001-reflective-larch-pattern.json. Its text is null;
do not treat the URL slug as the verified title or invent missing copy.

## Approved visual work

Open design/reflection-study.html. It is a standalone HTML prototype with its
image embedded, no dependencies or build step. Serve the repository over HTTP
for browser testing. The image is also in design/assets/reflective-clothing-dim.png.

The user supplied a nighttime photograph of two people in reflective patterned
jackets walking a dog. An AI-edited dim version was generated; some photo details
shifted, so it is a concept asset, not a pixel-faithful replacement of the original.
The original uploaded bright photo is visible in the earlier chat but was not
available as a local source file and is not in this backup.

The prototype keeps the scene still. A canvas overlay brightens masked jacket
stripes. The approved effect is a soft light band 360 image pixels wide, sweeping
20 degrees upward from lower left to upper right, in approximately one second.
There are irregular brief pauses. The user called this version “perfect”.
Controls include pause/play and reflection intensity; reduced motion starts paused.
Future generated versions should vary width, speed, angle, and pauses subtly
around this baseline. Only speed and pauses currently vary in the implementation.
Do not silently replace the approved effect or redesign the whole photograph.

The mask is a prototype using jacket-region polygons and pixel color thresholds;
production refinement should inspect edges and avoid lighting unrelated pixels.

## Audio: use revision 3

Open design/audio/listen.html. The current mix is:
- design/audio/blask-rider-rain-loop-v3.mp3
- design/audio/blask-rider-rain-loop-v3.opus
- design/audio/blask-rider-rain-loop-v3.wav (lossless export of MP3-derived sources)

120-second stereo loop: close rider perspective with chain, pedals, freewheel,
gear changes and braking. The first street-only mix was too weak on bicycle
sounds, so the rider layer was brought forward and rain/traffic lowered.

The latest user request added two different bells and one distant dog bark:
- 0:22: brass single ding.
- 0:54: quiet distant dog bark.
- 1:36: classic mechanical bicycle bell.

The user approved the final v3 audio on 26 October 2026 in the continuation
conversation. Use v3 as the approved website ambience. Timing, duration,
loudness and peak headroom were also checked during production.
Keep the earlier versions and source clips for revisions. Do not regenerate
paid ElevenLabs assets merely to resume work. Details and measurement reports
are in design/audio/PRODUCTION.md and audio-validation*.json.

Short UI sound: design/audio/blask-interaction-click.mp3. Use sparingly on
intentional actions, not every hover or scroll. Website sound must be off until
explicitly enabled, with a persistent accessible mute control.

## Hosting and credentials

Read docs/hosting-handover.md. The subdomain blask.korzeniowski.net was created
in a separate local IQHost task. Reported verified FTPS route:
host92093.iqhs.pl:21, username raf@host92093.iqhs.pl, explicit TLS, certificate
verification, protected data channel, passive mode. Verified CWD:
/domains/blask.korzeniowski.net/public_html.

This account can access other sites. All Blask operations must remain in that
exact document root; do not modify Dorado, email, shared configuration or other
sites. No Blask deployment or independent DNS/HTTPS verification has been done.

The dedicated FTP account plan was cancelled in favor of the existing account.
A password and an ElevenLabs key were later handed over in the prior chat and
used only as needed; neither is stored here. Historical notes that say no
credential was handed over describe an earlier stage and are superseded by the
addendum in hosting-handover.md. Never request passwords in chat or copy secrets
into this repository, frontend, logs, archives or scripts. Use securely configured
bindings or the Mac's existing private credential setup. FTPS needs a compatible
credential mechanism; HTTPS proxy placeholders do not automatically work for FTP.

The IQHost skill was found in the local “Mixtapes” conversation at:
/Users/raf/.codex/skills/building-iqhost-accommodation-sites/SKILL.md
It was not available in the cloud skill catalog. Working browser route:
https://iqhost.pl/login → dashboard service → “Otwórz panel” → DirectAdmin.
The local hosting setup thread is 01a177f6-0141-7fd3-ac20-492e50fc4283.

## Network issue and resuming in a fresh cloud task

This setup chat's environment draft became stale after newer settings were
saved elsewhere. The user sees unrestricted access, but this session's runtime
reports an older restricted configuration with unknown enforcement state. The
observed Biruta request failed at proxy CONNECT with HTTP 403. Do not claim this
is a Biruta website error or keep asking the user to save the same stale draft.

Create/resume from current environment settings with a fresh draft and restore
this repository. Use cloud-environment-runtime to inspect actual readiness.
Retry the Biruta URL. The file content/sources/proposed-network-update.json is
an old proposal, NOT applied configuration; reconcile with current settings and
never replace unrestricted access with that restricted list by accident.
ElevenLabs previously worked after the user adjusted access.

Each cloud task is already isolated. Use its checkout; do not create a worktree
unless the user requests one. Do not assume this old workspace or live server
processes survive in a fresh task. GitHub or the portable backup is the source.

## Next actions

1. Verify the restored files and read this handover before starting new work.
2. Retrieve the Biruta page with verified TLS. Extract main article headings,
   paragraphs and relevant project metadata, preserving its original language
   and wording. Exclude navigation/footer boilerplate. Save readable Markdown
   and structured JSON with URL, retrieval date and attribution. Replace the
   pending record only after successful retrieval and inspection.
3. If blocked, diagnose current network policy and preserve the exact blocker.
   User-supplied HTML/text is an acceptable alternative. Never invent content.
4. Tell the user the source import is done, with a file link. This is the current
   concrete task to finish; the rest is the broader project direction.
5. For subsequent design work, use available design skills and build around the
   approved reflective sweep and rider audio. Do not invent garment specs,
   prices, safety certifications, stock, brand claims or checkout functionality.
6. When asked to publish a concrete build, validate it locally, then deploy only
   its intended public files to Blask's directory and verify HTTPS and behavior.
   Do not upload source recordings, scripts, internal notes or credentials.

## Running locally

From the repository root:

    python3 -m http.server 8080 --bind 127.0.0.1

Open /design/reflection-study.html and /design/audio/listen.html on that server.
Python's standard library is sufficient to serve these artifacts. Audio
reproduction scripts require Python 3, FFmpeg and ffprobe. Generation additionally
requires authorized ElevenLabs access; those scripts may incur usage charges.
Mixing order: mix-street.py, mix-rider.py, mix-bells.py. Existing final audio is
already included; rebuilding is not required to inspect it.

No production website, purchase flow, or hosting deployment is complete.
