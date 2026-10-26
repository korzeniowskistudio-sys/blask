from pathlib import Path
import subprocess,json
root=Path(__file__).resolve().parents[2] / 'design' / 'audio'
def run(args):subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y']+args,check=True)
def measure(path):
 r=subprocess.run(['ffmpeg','-hide_banner','-i',str(path),'-af','loudnorm=I=-23:TP=-2:LRA=11:print_format=json','-f','null','-'],capture_output=True,text=True,check=True)
 return json.loads(r.stderr[r.stderr.rfind('{'):r.stderr.rfind('}')+1])
def normalize(src,dst,target):
 m=measure(src);gain=min(target-float(m['input_i']),-3-float(m['input_tp']))
 run(['-i',str(src),'-af',f'volume={gain}dB','-c:a','pcm_s24le',str(dst)])
 return {'gain_db':gain,'source_measurement':m}
def loop(names,dst):
 args=[];f=[]
 for i,name in enumerate(names):
  args+=['-i',str(root/name)];f.append(f'[{i}:a]aresample=48000,aformat=channel_layouts=stereo,atrim=duration=26,asetpts=PTS-STARTPTS[a{i}]')
 prev='a0'
 for i in range(1,5):
  name=f'j{i}';f.append(f'[{prev}][a{i}]acrossfade=d=2:c1=tri:c2=tri[{name}]');prev=name
 f.extend([f'[{prev}]asplit=3[b][t][h]','[b]atrim=start=2:end=120,asetpts=PTS-STARTPTS[body]','[t]atrim=start=120:end=122,asetpts=PTS-STARTPTS,afade=t=out:st=0:d=2[tail]','[h]atrim=start=0:end=2,asetpts=PTS-STARTPTS,afade=t=in:st=0:d=2[head]','[tail][head]amix=inputs=2:duration=shortest:normalize=0[seam]','[body][seam]concat=n=2:v=0:a=1[out]'])
 run(args+['-filter_complex',';'.join(f),'-map','[out]','-c:a','pcm_s24le',str(dst)])
# Reuse only the original sections that were not prompted to contain a bell.
loop(['street-01.mp3','street-02.mp3','street-04.mp3','street-05.mp3','street-02.mp3'],'/tmp/blask-background-v2.wav')
loop(['rider-pedalling-01.mp3','rider-freewheel-01.mp3','rider-pedalling-02.mp3','rider-pedalling-01.mp3','rider-pedalling-02.mp3'],'/tmp/blask-rider-bed.wav')
report={}
report['background']=normalize('/tmp/blask-background-v2.wav','/tmp/blask-quiet-street.wav',-35)
report['rider']=normalize('/tmp/blask-rider-bed.wav','/tmp/blask-close-bike.wav',-23)
# Keep distinct shifter and brake events audible, separate from the moving bed.
report['gear']=normalize(root/'rider-gear-change.mp3','/tmp/blask-gear.wav',-21)
report['brake']=normalize(root/'rider-braking.mp3','/tmp/blask-brake.wav',-24)
f=['[1:a]asplit=3[g1][g2][g3]','[2:a]asplit=2[b1][b2]','[g1]adelay=13700:all=1[g1d]','[g2]volume=0.85,adelay=62400:all=1[g2d]','[g3]volume=0.92,adelay=105100:all=1[g3d]','[b1]adelay=38200:all=1[b1d]','[b2]volume=0.8,adelay=89100:all=1[b2d]','[0:a][g1d][g2d][g3d][b1d][b2d]amix=inputs=6:duration=first:normalize=0[out]']
run(['-i','/tmp/blask-close-bike.wav','-i','/tmp/blask-gear.wav','-i','/tmp/blask-brake.wav','-filter_complex',';'.join(f),'-map','[out]','-c:a','pcm_s24le','/tmp/blask-rider-foreground.wav'])
run(['-i','/tmp/blask-rider-foreground.wav','-i','/tmp/blask-quiet-street.wav','-filter_complex','[0:a][1:a]amix=inputs=2:duration=first:normalize=0[out]','-map','[out]','-c:a','pcm_s24le','/tmp/blask-rider-mix.wav'])
report['master']=normalize('/tmp/blask-rider-mix.wav',root/'blask-rider-rain-loop-v2.wav',-23)
for suffix,codec,bitrate in [('mp3','libmp3lame','160k'),('opus','libopus','96k')]:
 run(['-i',str(root/'blask-rider-rain-loop-v2.wav'),'-c:a',codec,'-b:a',bitrate,str(root/f'blask-rider-rain-loop-v2.{suffix}')])
run(['-i','/tmp/blask-rider-foreground.wav','-c:a','libmp3lame','-b:a','160k',str(root/'blask-rider-foreground-only.mp3')])
report['final']=measure(root/'blask-rider-rain-loop-v2.wav')
report['duration']=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration:stream=channels,sample_rate','-of','json',str(root/'blask-rider-rain-loop-v2.wav')]))
report['note']='No new bell generated; original bell-prompted section street-03 excluded. Generated content still requires listening review.'
(root/'audio-validation-v2.json').write_text(json.dumps(report,indent=2))
print(json.dumps({'duration':report['duration'],'loudness':report['final']},indent=2))
