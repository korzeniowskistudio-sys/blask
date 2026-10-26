import os,getpass,json,urllib.request,urllib.error
from pathlib import Path
out=Path(__file__).resolve().parents[2] / 'design' / 'audio';out.mkdir(parents=True,exist_ok=True)
key=os.environ.get('ELEVENLABS_API_KEY') or getpass.getpass('API credential (hidden): ')
jobs=[
('rider-pedalling-01.mp3','Close first-person sound from a microphone mounted on a bicycle frame while riding. Clearly audible rhythmic pedal crank rotation, detailed metal chain whirring over sprockets, subtle mechanical ticking and wet bicycle tire rolling. Bicycle drivetrain dominates, intimate and tactile. No cars, rain ambience, music, voices, bells or motor engine. Continuous natural riding.',26,True),
('rider-freewheel-01.mp3','First-person bicycle riding sound, close microphone at rear hub. Distinct rapid freewheel ratchet ticking while coasting, slowing slightly then speeding up, alternating with smooth chain whir as pedalling resumes. Light wet tire roll underneath. Clear bicycle mechanics in foreground. No traffic, rain wash, wind roar, voices, music or bells.',26,True),
('rider-pedalling-02.mp3','Close onboard bicycle recording while cycling steadily: crisp chain links running over gears, rhythmic pedal strokes and slight crank creaks, soft thin bicycle tires hissing on a wet road. A couple of distinct derailleur clacks then continuous pedalling. Intimate mechanical bicycle sounds, not a passing bicycle. No cars, voices, music, bells or loud wind.',26,True),
('rider-gear-change.mp3','Isolated close realistic bicycle gear change while pedalling: thumb shifter click, short metallic derailleur clack, chain jumps onto next sprocket then runs smoothly. Detailed dry mechanical recording, foreground, no traffic, bell, voice, music or ambience.',2,False),
('rider-braking.mp3','Close realistic bicycle braking while moving on wet pavement: brake lever squeeze and cable click, brief controlled rubber brake friction squeak, tire roll slows down. Gentle purposeful stop, not a skid or crash. Dry clear foreground effect, no traffic, voices, bells or music.',3,False)
]
for name,prompt,duration,loop in jobs:
 dest=out/name
 if dest.exists() and dest.stat().st_size>1000:
  print(name+': existing output retained',flush=True);continue
 assert len(prompt)<=450, 'Prompt exceeds API limit'
 body=json.dumps({'text':prompt,'duration_seconds':duration,'loop':loop,'prompt_influence':0.45,'model_id':'eleven_text_to_sound_v2'}).encode()
 req=urllib.request.Request('https://api.elevenlabs.io/v1/sound-generation?output_format=mp3_44100_128',data=body,headers={'xi-api-key':key,'Content-Type':'application/json'},method='POST')
 print('Generating '+name,flush=True)
 try:
  with urllib.request.urlopen(req,timeout=180) as r:
   data=r.read();content=r.headers.get('Content-Type','')
  if 'audio' not in content: raise RuntimeError('Unexpected non-audio response')
  dest.write_bytes(data)
  print('Saved '+name+' ('+str(len(data))+' bytes)',flush=True)
 except urllib.error.HTTPError as e:
  print('Generation stopped: HTTP '+str(e.code),flush=True)
  print(e.read().decode('utf-8',errors='replace').replace(key,'[redacted]')[:1500],flush=True)
  raise SystemExit(1)
key=None
print('Generation complete',flush=True)
