import os,getpass,json,urllib.request,urllib.error
from pathlib import Path
out=Path(__file__).resolve().parents[2] / 'design' / 'audio';out.mkdir(parents=True,exist_ok=True)
key=os.environ.get('ELEVENLABS_API_KEY') or getpass.getpass('API credential (hidden): ')
base='Realistic stereo field recording: busy rainy city street, cyclist perspective. Continuous soft rain on wet asphalt, passing cars and wet tire hiss at varied distances. Natural restrained dynamics. No music, speech, sirens, horns or thunder. '

scenes=[
'Nearby bicycle chain and smooth pedalling, two small precise gear changes. Cars pass gently through the rain. No bells.',
'A car approaches, passes with wet tire spray, and recedes. Close bicycle freewheel ticking then resumed pedalling. No bells.',
'Nearby bicycle rolls slowly, a brief realistic soft brake friction sound, one gentle bicycle bell ding midway, then pedalling resumes. Continuous rain and distant traffic.',
'Rain and varied passing traffic dominate. Intermittent close bicycle chain, pedalling, and one gear shift. No bells.',
'A bicycle passes nearby with quiet pedalling and a brief brake sound, cars recede into steady rain. No bells. Finish with rain and gentle road hiss, no abrupt ending.'
]
jobs=[(f'street-{i+1:02}.mp3',base+scene,26,True) for i,scene in enumerate(scenes)]
jobs.append(('interaction-gear-click.mp3','A single quiet crisp mechanical click of a high quality bicycle gear shifter, close dry recording, subtle tactile spring snap and very short natural decay. One isolated click, no repeating, no background noise, no voices, no music, no reverb.',0.5,False))
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
