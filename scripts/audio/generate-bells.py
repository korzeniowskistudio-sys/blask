import os,getpass,json,urllib.request,urllib.error
from pathlib import Path
out=Path(__file__).resolve().parents[2] / 'design' / 'audio';out.mkdir(parents=True,exist_ok=True)
key=os.environ.get('ELEVENLABS_API_KEY') or getpass.getpass('API credential (hidden): ')
jobs=[
('bicycle-bell-single.mp3','One isolated strike of a small brass bicycle bell, a clear warm high ding with a short natural metallic decay. Close realistic outdoor recording. Exactly one ding, no second strike, no voices, music or background noise.',1.5,False),
('bicycle-bell-classic.mp3','One brief activation of a classic mechanical bicycle bell: a distinctive lower pitched bright brrring with a gently rattling metallic decay, clearly different from a single high ding. Realistic outdoor recording, isolated, no additional rings, voices, music or traffic.',2,False),
('distant-dog-bark.mp3','One isolated natural dog bark from far down a residential street, about fifty meters away. Muted and softly reflected by distant buildings, unobtrusive outdoor sound. Just one short bark then decay, no growling, no repeated barking, no voices, music or other animals.',2,False)
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
