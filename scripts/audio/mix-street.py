from pathlib import Path
import subprocess,json
root=Path(__file__).resolve().parents[2] / 'design' / 'audio'
def run(args):
 subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y']+args,check=True)
args=[]
for i in range(1,6):args+=['-i',str(root/f'street-{i:02}.mp3')]
f=[]
for i in range(5):f.append(f'[{i}:a]aresample=48000,aformat=channel_layouts=stereo,atrim=duration=26,asetpts=PTS-STARTPTS[a{i}]')
prev='a0'
for i in range(1,5):
 name=f'j{i}';f.append(f'[{prev}][a{i}]acrossfade=d=2:c1=tri:c2=tri[{name}]');prev=name
# 122-second assembled stream: blend its final 2 seconds into its first 2.
# Start playback after the original first 2 seconds, yielding a 120-second ring.
f.append(f'[{prev}]asplit=3[bodyin][tailin][headin]')
f.append('[bodyin]atrim=start=2:end=120,asetpts=PTS-STARTPTS[body]')
f.append('[tailin]atrim=start=120:end=122,asetpts=PTS-STARTPTS,afade=t=out:st=0:d=2[tail]')
f.append('[headin]atrim=start=0:end=2,asetpts=PTS-STARTPTS,afade=t=in:st=0:d=2[head]')
f.append('[tail][head]amix=inputs=2:duration=shortest:normalize=0[seam]')
f.append('[body][seam]concat=n=2:v=0:a=1,alimiter=limit=0.79:level=false[loop]')
run(args+['-filter_complex',';'.join(f),'-map','[loop]','-c:a','pcm_s24le','/tmp/blask-loop-raw.wav'])
# Measure then apply constant gain, preserving the loop's boundary behavior.
r=subprocess.run(['ffmpeg','-hide_banner','-i','/tmp/blask-loop-raw.wav','-af','loudnorm=I=-23:TP=-2:LRA=11:print_format=json','-f','null','-'],capture_output=True,text=True,check=True)
stats=json.loads(r.stderr[r.stderr.rfind('{'):r.stderr.rfind('}')+1]);gain=min(-23-float(stats['input_i']),-2-float(stats['input_tp']))
run(['-i','/tmp/blask-loop-raw.wav','-af',f'volume={gain}dB','-c:a','pcm_s24le',str(root/'blask-rain-street-loop.wav')])
for name,codec,bitrate in [('blask-rain-street-loop.mp3','libmp3lame','160k'),('blask-rain-street-loop.opus','libopus','96k')]:run(['-i',str(root/'blask-rain-street-loop.wav'),'-c:a',codec,'-b:a',bitrate,str(root/name)])
# Preserve the generated click's natural timing; remove only digital silence.
run(['-i',str(root/'interaction-gear-click.mp3'),'-af','silenceremove=start_periods=1:start_duration=0.005:start_threshold=-50dB,afade=t=out:st=0.42:d=0.08,volume=-6dB','-c:a','libmp3lame','-b:a','128k',str(root/'blask-interaction-click.mp3')])
report={'source':'ElevenLabs eleven_text_to_sound_v2','sections':5,'section_seconds':26,'crossfade_seconds':2,'gain_db':gain,'raw_measurement':stats,'files':{}}
for name in ['blask-rain-street-loop.wav','blask-rain-street-loop.mp3','blask-rain-street-loop.opus','blask-interaction-click.mp3']:
 data=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration,size:stream=sample_rate,channels','-of','json',str(root/name)]))
 report['files'][name]=data
(root/'audio-validation.json').write_text(json.dumps(report,indent=2))
print(json.dumps(report['files'],indent=2))
