from pathlib import Path
import subprocess,json,re
root=Path(__file__).resolve().parents[2] / 'design' / 'audio'
def run(args):subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y']+args,check=True)
def event(name,target,filters):
 src=root/name
 r=subprocess.run(['ffmpeg','-hide_banner','-i',str(src),'-af',filters+',volumedetect','-f','null','-'],capture_output=True,text=True,check=True)
 peak=float(re.search(r'max_volume: ([\-\d.]+) dB',r.stderr).group(1))
 dst=Path('/tmp')/('blask-'+src.stem+'.wav')
 run(['-i',str(src),'-af',filters+f',volume={target-peak}dB','-ar','44100','-ac','2','-c:a','pcm_s24le',str(dst)])
 return dst
bell1=event('bicycle-bell-single.mp3',-14,'afade=t=in:d=0.008,afade=t=out:st=1.2:d=0.3')
bell2=event('bicycle-bell-classic.mp3',-15,'afade=t=in:d=0.008,afade=t=out:st=1.7:d=0.3')
dog=event('distant-dog-bark.mp3',-27,'highpass=f=180,lowpass=f=2200,afade=t=in:d=0.02,afade=t=out:st=1.5:d=0.5')
master=root/'blask-rider-rain-loop-v3.wav'
run(['-i',str(root/'blask-rider-rain-loop-v2.wav'),'-i',str(bell1),'-i',str(bell2),'-i',str(dog),'-filter_complex','[1:a]adelay=22000:all=1[b1];[2:a]adelay=96000:all=1[b2];[3:a]adelay=54000:all=1[d];[0:a][b1][b2][d]amix=inputs=4:duration=first:normalize=0[out]','-map','[out]','-c:a','pcm_s24le',str(master)])
for ext,codec,rate in [('mp3','libmp3lame','160k'),('opus','libopus','96k')]:run(['-i',str(master),'-c:a',codec,'-b:a',rate,str(root/f'blask-rider-rain-loop-v3.{ext}')])
r=subprocess.run(['ffmpeg','-hide_banner','-i',str(master),'-af','loudnorm=I=-23:TP=-2:LRA=11:print_format=json','-f','null','-'],capture_output=True,text=True,check=True)
m=json.loads(r.stderr[r.stderr.rfind('{'):r.stderr.rfind('}')+1])
probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration:stream=channels,sample_rate','-of','json',str(master)]))
assert float(probe['format']['duration'])==120
assert float(m['input_tp'])<0
report={'events':[{'time_seconds':22,'sound':'single brass bicycle bell'},{'time_seconds':54,'sound':'one distant dog bark'},{'time_seconds':96,'sound':'classic mechanical bicycle bell'}],'loudness':m,'format':probe,'notes':'Existing v2 bed preserved, no processing across loop boundary. Each generated event placed once; event content requires listening review.'}
(root/'audio-validation-v3.json').write_text(json.dumps(report,indent=2))
print(json.dumps(report,indent=2))
