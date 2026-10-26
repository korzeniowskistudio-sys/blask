# Blask work-in-progress page

Prepared 26 October 2026. The user requested a simple public holding page,
then confirmed the destination is **blask.korzeniowski.net**, and requested
the approved animated picture and audio as well as the original portfolio photos.

## Build

`site/` contains the complete static website. No build step or dependencies.
Preview with `python3 -m http.server 8080 --directory site`.

- Two original photos downloaded from the Reflective Larch Pattern portfolio,
  converted to WebP, and credited with a link back to the source.
- Approved reflective animation reused from the existing prototype. Its script
  is extracted into `reflection.js`, retaining the mask, sweep, timing and controls.
  An initialization guard prevents the cached image from initializing twice.
- Approved rider audio v3, Opus with MP3 fallback. Playback requires an explicit
  click and a fixed enable/mute button remains available. No audible autoplay.
- Animation starts paused for reduced-motion preferences.
- No shop, tracking, form, external font, or invented product specifications.

## Verification

Chromium checks passed at 1440, 768 and 390 pixels: all images load, no horizontal
overflow or JavaScript errors. Sound starts off, play advances the audio clock,
and mute pauses it. Animation pause and reduced-motion initial state verified.
Desktop and mobile screenshots were visually inspected.

The live hostname responded over verified HTTPS with status 200; its title was
`blask.korzeniowski.net`. This was the pre-deployment page, not the new build.

## Publication

Published on 26 October 2026 via GitHub Actions run 40349944526:
https://github.com/korzeniowskistudio-sys/blask/actions/runs/40349944526

The FTPS upload and workflow HTTPS checks passed. Independently downloaded all
seven live public files over verified HTTPS and confirmed their SHA-256 hashes
match the locally tested build exactly. The ordinary cloud shell never received
the stored FTPS credentials. The direct cloud Chromium live navigation encountered
the proxy CA trust issue; local Chromium behavior checks and independent verified
HTTPS content checks succeeded. No browser TLS validation was disabled.

The workflow `.github/workflows/deploy-blask.yml` runs on changes to public site
or deployment files on `main`, or by manual dispatch. It uses encrypted repository
secrets documented in `docs/ftp-connection.md`. It backs up an existing index,
uploads only the explicit public-file list, checks transfer sizes, then publishes
the new index last. It does not mirror or delete unrelated files.

The following is the alternative local deployment route:

Using the existing local FileZilla connection described in hosting-handover.md,
upload only the **contents** of `site/` to:

    /domains/blask.korzeniowski.net/public_html

The deployment ZIP contains that same public-file set at its root. Extract it
locally before uploading with FileZilla. Do not upload the ZIP itself, internal
notes, source recordings, validation reports, or the entire repository.
Preserve unrelated files and back up any existing index file before replacing it.
Use explicit FTPS with certificate verification and protected data channels.

After upload, check HTTPS, original photos, the animation and its pause control,
sound activation/mute, and phone layout on the live hostname.
