
const photo=document.querySelector('#photo'),canvas=document.querySelector('#shine'),ctx=canvas.getContext('2d'),toggle=document.querySelector('#toggle'),slider=document.querySelector('#strength');
let paused=matchMedia('(prefers-reduced-motion: reduce)').matches,time=0,last=0,groups=[];
const sweep={start:0,duration:950,pause:650};
const reflection=document.createElement("canvas"),reflectionCtx=reflection.getContext("2d");
function sync(){toggle.textContent=paused?'Play animation':'Pause animation';toggle.setAttribute('aria-pressed',String(paused))}sync();toggle.onclick=()=>{paused=!paused;sync()};
const polygons=[[[319,580],[351,566],[411,573],[441,612],[458,670],[427,705],[414,761],[351,800],[303,784],[308,684]],[[450,514],[482,503],[524,510],[551,494],[599,506],[618,556],[630,630],[606,696],[584,731],[453,743],[430,683],[443,629]]];
function inside(x,y,p){let c=false;for(let i=0,j=p.length-1;i<p.length;j=i++){let a=p[i],b=p[j];if((a[1]>y)!=(b[1]>y)&&x<(b[0]-a[0])*(y-a[1])/(b[1]-a[1])+a[0])c=!c}return c}
function init(){canvas.width=photo.naturalWidth;canvas.height=photo.naturalHeight;const w=canvas.width,h=canvas.height;ctx.drawImage(photo,0,0);const pixels=ctx.getImageData(0,0,w,h);ctx.clearRect(0,0,w,h);
for(let person=0;person<2;person++)for(let band=0;band<6;band++){const layer=document.createElement('canvas');layer.width=w;layer.height=h;const lc=layer.getContext('2d'),mask=lc.createImageData(w,h);let count=0;for(let y=490;y<805;y++)for(let x=300;x<635;x++){if(!inside(x,y,polygons[person])||Math.floor((y-(person?494:566))/52)!==band)continue;let i=(y*w+x)*4,r=pixels.data[i],g=pixels.data[i+1],b=pixels.data[i+2],bright=(r+g+b)/3,chroma=Math.max(r,g,b)-Math.min(r,g,b);const alpha=Math.max(0,Math.min(1,(bright-43)/24))*Math.max(0,Math.min(1,(25-chroma)/13));if(!alpha)continue;mask.data[i]=238;mask.data[i+1]=243;mask.data[i+2]=255;mask.data[i+3]=Math.round(alpha*245);count++}lc.putImageData(mask,0,0);groups.push({layer,count})}window.blaskReady=true;requestAnimationFrame(frame)}
function frame(now){
if(!last)last=now;
if(!paused)time+=Math.min(now-last,100);
last=now;
let elapsed=time-sweep.start;
if(elapsed>=sweep.duration+sweep.pause){
sweep.start=time;sweep.duration=850+Math.random()*250;sweep.pause=450+Math.random()*650;elapsed=0;
}
if(reflection.width!==canvas.width||reflection.height!==canvas.height){
reflection.width=canvas.width;reflection.height=canvas.height;
reflectionCtx.clearRect(0,0,reflection.width,reflection.height);
for(const g of groups)reflectionCtx.drawImage(g.layer,0,0);
}
ctx.clearRect(0,0,canvas.width,canvas.height);
if(elapsed<=sweep.duration){
const angle=20*Math.PI/180;
const directionX=Math.cos(angle),directionY=-Math.sin(angle);
const centerX=210+(elapsed/sweep.duration)*530;
const centerY=760-(centerX-210)*Math.tan(angle);
const halfWidth=180;
const beam=ctx.createLinearGradient(
centerX-halfWidth*directionX,centerY-halfWidth*directionY,
centerX+halfWidth*directionX,centerY+halfWidth*directionY);
beam.addColorStop(0,'rgba(255,255,255,0)');
beam.addColorStop(.3,'rgba(255,255,255,.3)');
beam.addColorStop(.5,'rgba(255,255,255,1)');
beam.addColorStop(.7,'rgba(255,255,255,.3)');
beam.addColorStop(1,'rgba(255,255,255,0)');
ctx.globalAlpha=slider.value/100;
ctx.drawImage(reflection,0,0);
ctx.globalAlpha=1;
ctx.globalCompositeOperation='destination-in';
ctx.fillStyle=beam;ctx.fillRect(0,0,canvas.width,canvas.height);
ctx.globalCompositeOperation='source-over';
}
requestAnimationFrame(frame);
}
let initialized=false;const initializeOnce=()=>{if(initialized)return;initialized=true;init()};photo.onload=initializeOnce;photo.onerror=()=>document.querySelector('#status').textContent='The photograph could not load. Reopen this HTML file.';if(photo.complete&&photo.naturalWidth)initializeOnce();
