"""Create a three-minute evolving rider scene from retained, licensed sources.

Requires Python, NumPy and FFmpeg. No generation service or credentials used.
"""
from pathlib import Path
import json
import subprocess
import tempfile

import numpy as np

ROOT = Path(__file__).resolve().parents[2] / "design" / "audio"
SR = 48000
DURATION = 180
N = SR * DURATION
EVENTS = []


def run(args, **kwargs):
    return subprocess.run(args, check=True, **kwargs)


def decode(name, tempo=1.0, filters=""):
    chain = f"atempo={tempo}" + ("," + filters if filters else "")
    raw = subprocess.check_output([
        "ffmpeg", "-v", "error", "-i", str(ROOT / name),
        "-af", chain, "-ar", str(SR), "-ac", "2", "-f", "f32le", "-",
    ])
    return np.frombuffer(raw, dtype="<f4").reshape(-1, 2).copy()


def rms_level(data, db):
    return data * (10 ** (db / 20) / max(float(np.sqrt(np.mean(data ** 2))), 1e-9))


def fade(data, seconds):
    data = data.copy()
    count = min(int(seconds * SR), len(data) // 2)
    envelope = np.linspace(0, 1, count, dtype=np.float32)
    data[:count] *= envelope[:, None]
    data[-count:] *= envelope[::-1, None]
    return data


def add_ring(mix, data, start):
    start = round(start * SR) % N
    first = min(len(data), N - start)
    mix[start:start + first] += data[:first]
    if first < len(data):
        mix[:len(data) - first] += data[first:]


def measure(path):
    result = run([
        "ffmpeg", "-hide_banner", "-i", str(path), "-af",
        "loudnorm=I=-23:TP=-2:LRA=11:print_format=json", "-f", "null", "-",
    ], capture_output=True, text=True)
    return json.loads(result.stderr[result.stderr.rfind("{"):result.stderr.rfind("}") + 1])


def event(mix, source, start, peak_db, pan_start, pan_end=None, tempo=1.0, filters=""):
    data = decode(source, tempo, filters)
    mono = np.mean(data, axis=1)
    mono *= 10 ** (peak_db / 20) / max(float(np.max(np.abs(mono))), 1e-9)
    position = np.linspace(pan_start, pan_start if pan_end is None else pan_end, len(mono))
    stereo = np.column_stack((mono * np.cos(position * np.pi / 2), mono * np.sin(position * np.pi / 2)))
    add_ring(mix, fade(stereo, .025), start)
    EVENTS.append({"time_seconds": start, "source": source, "peak_before_master_dbfs": peak_db,
                   "pan_start": pan_start, "pan_end": pan_end, "tempo": tempo})


def main():
    mix = np.zeros((N, 2), dtype=np.float32)
    # Eighteen-second takes overlap by three seconds, including across the loop seam.
    # Bike level falls markedly at stops; street sound rises through the gaps.
    scenes = [
        ("Setting off", "rider-pedalling-01.mp3", -28, "street-01.mp3", -37, 1.00),
        ("Pedalling builds", "rider-pedalling-02.mp3", -25, "street-02.mp3", -34, 1.06),
        ("Busy wet street", "rider-pedalling-01.mp3", -28, "street-04.mp3", -29, 1.03),
        ("Coasting", "rider-freewheel-01.mp3", -24, "street-05.mp3", -36, .97),
        ("Slowing at a crossing", "rider-freewheel-01.mp3", -35, "street-02.mp3", -31, .94),
        ("Rain comes forward", None, None, "street-01.mp3", -29, 1.00),
        ("Back on the pedals", "rider-pedalling-02.mp3", -25, "street-05.mp3", -37, 1.02),
        ("Traffic moves past", "rider-pedalling-01.mp3", -29, "street-04.mp3", -29, 1.08),
        ("A quieter corner", "rider-freewheel-01.mp3", -31, "street-01.mp3", -36, .96),
        ("Freewheel close up", "rider-freewheel-01.mp3", -24, "street-05.mp3", -38, 1.05),
        ("A passing cyclist", "rider-pedalling-02.mp3", -26, "street-02.mp3", -33, 1.04),
        ("Settling into the ride", "rider-pedalling-01.mp3", -28, "street-01.mp3", -37, 1.00),
    ]
    report_scenes = []
    for i, (label, bike, bike_db, street, street_db, tempo) in enumerate(scenes):
        length = 18 * SR
        # Different offsets and tempos prevent the same short passage recurring unchanged.
        offset = [0, 4, 2, 6, 1, 7, 3, 5, 2, 4, 1, 0][i] * SR
        background = decode(street)
        take = background[offset:offset + length]
        assert len(take) == length
        layer = rms_level(take, street_db)
        if bike:
            foreground = decode(bike, tempo)
            offset_bike = min(offset, len(foreground) - length)
            take = foreground[offset_bike:offset_bike + length]
            assert len(take) == length
            layer += rms_level(take, bike_db)
        add_ring(mix, fade(layer, 3), i * 15)
        report_scenes.append({"start_seconds": i * 15, "description": label,
                              "bike_source": bike, "bike_rms_dbfs": bike_db,
                              "street_source": street, "street_rms_dbfs": street_db})

    for t, peak, pan, tempo in [(9.2, -20, .46, 1), (34.6, -22, .53, 1.08),
                                (58.8, -23, .48, .96), (93.1, -19, .52, 1.04),
                                (112.4, -22, .44, 1.10), (145.8, -21, .55, .94),
                                (168.3, -23, .48, 1.02)]:
        event(mix, "rider-gear-change.mp3", t, peak, pan, tempo=tempo)
    for t, peak, tempo in [(43.2, -23, 1.04), (69.5, -20, .94), (127.4, -25, 1.10)]:
        event(mix, "rider-braking.mp3", t, peak, .5, tempo=tempo)
    event(mix, "bicycle-bell-single.mp3", 24.1, -17, .20, .62)
    event(mix, "bicycle-bell-classic.mp3", 86.3, -20, .82, .42, tempo=.96)
    event(mix, "bicycle-bell-single.mp3", 150.7, -21, .83, .18, tempo=1.07)
    event(mix, "bicycle-bell-classic.mp3", 157.2, -24, .25, .08, tempo=1.04)
    event(mix, "distant-dog-bark.mp3", 119.4, -29, .82,
          filters="highpass=f=200,lowpass=f=2400")
    event(mix, "distant-dog-bark.mp3", 133.8, -34, .18, tempo=1.08,
          filters="highpass=f=250,lowpass=f=1700")

    # Broad wet-road swells move across the stereo field, rather than sitting
    # at a constant background level for the full three minutes.
    for t, source, offset, reverse in [(16.5, "street-04.mp3", 8, False),
                                        (51.0, "street-02.mp3", 12, True),
                                        (105.5, "street-05.mp3", 4, False),
                                        (161.4, "street-04.mp3", 16, True)]:
        data = decode(source, filters="highpass=f=100,lowpass=f=7500")[offset * SR:(offset + 7) * SR]
        mono = np.mean(rms_level(data, -30), axis=1)
        envelope = np.sin(np.linspace(0, np.pi, len(mono))) ** 1.5
        pos = np.linspace(.05, .95, len(mono))
        if reverse:
            pos = pos[::-1]
        moving = np.column_stack((mono * envelope * np.cos(pos * np.pi / 2),
                                  mono * envelope * np.sin(pos * np.pi / 2)))
        add_ring(mix, moving, t)
        EVENTS.append({"time_seconds": t, "sound": "moving wet-street swell", "source": source})

    with tempfile.TemporaryDirectory(prefix="blask-v4-") as tmp:
        raw = Path(tmp) / "mix.f32"
        raw.write_bytes(mix.astype("<f4").tobytes())
        raw_wav = Path(tmp) / "mix.wav"
        run(["ffmpeg", "-v", "error", "-y", "-f", "f32le", "-ar", str(SR),
             "-ac", "2", "-i", str(raw), "-c:a", "pcm_s24le", str(raw_wav)])
        stats = measure(raw_wav)
        # Constant gain preserves natural dynamics and the loop boundary.
        gain = min(-23 - float(stats["input_i"]), -2.5 - float(stats["input_tp"]))
        master = ROOT / "blask-rider-rain-loop-v4.wav"
        run(["ffmpeg", "-v", "error", "-y", "-i", str(raw_wav),
             "-af", f"volume={gain}dB", "-c:a", "pcm_s24le", str(master)])
    formats = {}
    for ext, codec, rate in [("mp3", "libmp3lame", "192k"), ("opus", "libopus", "112k")]:
        dest = ROOT / f"blask-rider-rain-loop-v4.{ext}"
        run(["ffmpeg", "-v", "error", "-y", "-i", str(master), "-c:a", codec, "-b:a", rate, str(dest)])
        formats[ext] = json.loads(subprocess.check_output([
            "ffprobe", "-v", "error", "-show_entries", "format=duration,size:stream=sample_rate,channels", "-of", "json", str(dest)
        ]))
    final = measure(master)
    assert abs(float(final["input_i"]) + 23) < .3
    assert float(final["input_tp"]) <= -2
    pcm = np.frombuffer(subprocess.check_output([
        "ffmpeg", "-v", "error", "-i", str(master), "-f", "f32le", "-acodec", "pcm_f32le", "-"
    ]), dtype="<f4").reshape(-1, 2)
    assert len(pcm) == N
    windows = pcm.reshape(-1, SR // 10, 2)
    window_rms = np.sqrt(np.mean(windows ** 2, axis=(1, 2)))
    assert np.all(window_rms > 1e-6), "Silent splice gap"
    seam_jump = float(np.max(np.abs(pcm[0] - pcm[-1])))
    ordinary_steps = np.max(np.abs(np.diff(pcm, axis=0)), axis=1)
    percentile = float(np.percentile(ordinary_steps, 99.9))
    assert seam_jump < max(percentile * 2, .002), "Abnormal loop-boundary step"
    report = {"version": 4, "duration_seconds": DURATION, "sample_rate": SR, "channels": 2,
              "source": "New edit of existing ElevenLabs recordings; no new API generation",
              "scenes": report_scenes, "events": sorted(EVENTS, key=lambda e: e["time_seconds"]),
              "master_gain_db": gain, "loudness": final, "web_formats": formats,
              "minimum_100ms_rms": float(window_rms.min()), "loop_boundary_step": seam_jump,
              "ordinary_step_99_9_percentile": percentile,
              "review_status": "Technical checks complete; user listening review pending"}
    (ROOT / "audio-validation-v4.json").write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps({"duration": DURATION, "scenes": len(scenes), "events": len(EVENTS),
                      "loudness": final, "loop_boundary_step": seam_jump}, indent=2))


if __name__ == "__main__":
    main()
