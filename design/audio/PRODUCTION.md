# Blask audio production brief

## Requested deliverables

1. Approximately 120-second seamless stereo ambience loop for the website.
2. A short bicycle-inspired interaction sound.

Use ElevenLabs sound-effects generation. Generation is authorized by the user;
website deployment is not part of this request. Audio generated on 26 October 2026; see deliverables below.

## Ambience direction

Realistic street-level listening perspective on a busy city street in the rain.
Continuous soft rainfall on wet asphalt, with cars passing at varied distances:
wet tire hiss, gentle engine movement, natural left-to-right and right-to-left
stereo travel. Nearby bicycle pedalling, a quiet chain and freewheel, occasional
precise gear changes and short realistic brake sounds. One or two distant,
gentle bicycle bells across the full two minutes. Keep events natural and
irregular. No music, narration, intelligible speech, sirens, startling horns,
crashes, dramatic thunder, or exaggerated cinematic effects. Background use:
rich atmosphere, restrained peaks, and enough quiet space for the page.

Suggested sequence of compatible generated sections, all with the same rain
bed and street perspective:
- Establish rain and traffic; close pedalling with a brief gear change.
- Several wet-road car passes; light freewheel sound; no bell.
- Bicycle rolls closer, gently brakes, then resumes; one brief bell.
- Rain and traffic dominate; intermittent pedalling and gear movement.
- Soft traffic recedes; optional distant bell early in the section; finish with
  rain and tire hiss suitable for blending back to the opening.

Check the current ElevenLabs duration and model constraints before generation.
Build the full duration with overlapping sections if necessary. Use smooth
crossfades and a wraparound crossfade to avoid a seam. Do not simply repeat a
short clip with identical conspicuous bell or gear events.

## Interaction sound direction

A single close, dry bicycle gear-shifter click: crisp, softly mechanical,
slightly tactile, with a very brief natural decay. No voice, music, bell,
reverberant tail, or dramatic impact. Target 100–250 ms after trimming.
Use only on deliberate actions such as enabling sound or confirming a choice;
not on hover, scrolling, or every navigation action. Keep interaction audio
quieter than typical system alerts.

## Finishing and validation

- Listen through all generated sections and the final loop boundary.
- Verify roughly 120 seconds, no clipping, no silent splice gaps, and balanced
  stereo. Target approximately -23 LUFS for ambience and at most -2 dBTP.
- Export a lossless master plus web MP3 and Opus assets where supported.
- Include a simple audition page with a looping player and separate UI sample.
- Never autoplay audible sound. Start muted; require explicit user activation
  and provide an accessible, persistent mute control.
- Do not put API credentials in frontend code, generated files, or git.

## Generated deliverables and verification

Network access was restored on 26 October 2026. Generated five 26-second street
sections and one 0.5-second interaction click with ElevenLabs sound effects v2.
Prompts were kept within the API's 450-character limit. Source sections remain
in this directory for future editing.

- blask-rain-street-loop.wav: 120.000-second stereo master, 48 kHz, 24-bit PCM.
- blask-rain-street-loop.mp3: web MP3, 160 kbps.
- blask-rain-street-loop.opus: web Opus, 96 kbps; preferred looping source.
- blask-interaction-click.mp3: approximately 0.5-second dry mechanical click.
- listen.html: user-initiated audition controls; ambience loops with low initial volume.
- audio-validation.json: duration, stream and source loudness measurements.

The loop uses two-second section crossfades and a two-second wraparound blend.
Final loudness and true peak were measured with FFmpeg. Technical verification
does not constitute a listening review: the precise realism and prominence of
individual generated events still need user audition. No deployment performed.
The API credential was used transiently and not saved in project files.

## Revision 2 — rider perspective

User feedback: bicycle sounds were not sufficiently audible. Treat the scene
as the experience of the person riding, with the existing street audio quieter
underneath. The phrase “also no bell” was interpreted as omitting bells.

Generated three dedicated 26-second close bicycle recordings plus separate
two-second gear-change and three-second braking effects with ElevenLabs v2.
Built a 120-second foreground track and reused original street sections
01, 02, 04 and 05 as the quieter background; section 03 (bell-prompted) was
excluded. No bell was requested in the new generations.

The bicycle bed is set to -23 LUFS before mixing; the street bed is -35 LUFS.
Added gear changes at 13.7, 62.4 and 105.1 seconds; brakes at 38.2 and 89.1
seconds. Final master normalized to approximately -23 LUFS with peak headroom.

Deliverables: blask-rider-rain-loop-v2.wav/.mp3/.opus,
blask-rider-foreground-only.mp3 and updated listen.html. Version 1 retained.
Technical measurements are in audio-validation-v2.json. A listening review
is still needed to judge realism and generated event fidelity. No deployment.

## Revision 3 — two bells and a distant dog

At the user's request, generated two distinct bicycle bells and one distant
dog bark with ElevenLabs. Placed one instance of each in the retained v2 mix:
- 0:22: a high, single brass bell ding (peak set to -14 dBFS before mixing).
- 0:54: a distant dog bark (peak -27 dBFS; filtered to 180–2200 Hz).
- 1:36: a lower, rattling mechanical bell (peak -15 dBFS).

The existing rider and street bed remains unchanged. All additions occur away
from the loop boundary. Exported blask-rider-rain-loop-v3.wav/.mp3/.opus and
updated listen.html. Earlier versions retained. Technical validation is saved
in audio-validation-v3.json. The user approved the final v3 audio on
26 October 2026 in the continuation conversation. Use v3 as the approved
website ambience. No deployment performed.

## Revision 4 — three-minute changing ride

Requested 26 October 2026: a new three-minute version with more distinct changes
and greater sound variety. Created a new arrangement of the retained ElevenLabs
recordings; no new paid generations. Version 3 remains the approved homepage audio.

- 180-second, 48 kHz stereo master with twelve overlapping passages: setting off,
  building pedalling, a busy street, close freewheeling, slowing at a crossing,
  rain coming forward, restarting, passing traffic, a quieter corner, coasting,
  a passing cyclist, and settling back into the ride.
- Seven gear-change accents, three brake events, four bell events using both
  retained bell recordings, two distant dog events, and four moving wet-street
  swells. The underlying recorded clips can also contain their own events.
- Different source offsets, modest tempo changes, varying levels and stereo
  movement make recurring sources less identical. There are no newly recorded
  sound categories; this version varies the existing recordings and arrangement.
- Three-second overlaps also span the end/start boundary. No silent splice gaps
  were found, and the boundary sample step passed the ordinary-step comparison.
- Master: -23.03 LUFS, -2.50 dBTP. Web MP3: -23.24 LUFS, -2.57 dBTP.
  Web Opus: -23.03 LUFS, -2.60 dBTP. Exactly 180 seconds decoded in the master.

Deliverables: `blask-rider-rain-loop-v4.wav/.mp3/.opus`,
`audio-validation-v4.json`, and reproducible `scripts/audio/mix-varied-v4.py`
(requires NumPy and FFmpeg). WAV is a lossless export of edits to MP3-derived
sources, not an original lossless recording.

The separate public review page is `site/sound-v4.html`, with v4, six seek points,
downloads and a v3 comparison. Neither player autoplays, and starting one pauses
the other. Technical checks do not substitute for a listening review; user
approval of v4 is pending. The Blask homepage continues to use v3.
