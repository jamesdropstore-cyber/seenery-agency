/* ---------- Rundgang: ein durchgehender Kameraflug, vom Scrollen gesteuert ---------- */
const NF=/*NF*/0, AR=16/9;
const tour=$('#tour'), stg=$('.stage',tour), cv=$('#cv'), cx=cv.getContext('2d');
const s5=$('.scene.s5',tour), cam5=$('.cam',s5), mcard=$('#mcard');
const caps=$$('.cap',tour), intro=$('#intro'), ish=$('#ish'), fl=$('#fl'), nb=$$('#tnav button'), ld=$('#ld'), ldi=$('#ldi'), ldt=$('#ldt');
const N=7;
// Scroll-Einheit → Position im Film (0…1). Marken: /*MARKS*/
const TM=/*TM*/[[0,0],[7,1]];
// Handy: welcher Bildausschnitt (0 = links, 1 = rechts)
const FX=/*FX*/[[0,.5],[7,.5]];
const CH=/*CH*/[0,1,2,3,4,5.6];
const CAPW=/*CAPW*/[];
const HOLD=/*HOLD*/[3.9,4.75];
const imgs=new Array(NF), ok=new Uint8Array(NF);
let tTop=0,tLen=1,target=0,cur=0,raf=0,lastT=0,lastCh=-1,lastDraw='',dropped=false,shT=[];
const lp=(P,f)=>{if(f<=P[0][0])return P[0][1];for(let i=1;i<P.length;i++)if(f<=P[i][0]){const[a,x]=P[i-1],[b,y]=P[i];return x+(y-x)*(f-a)/(b-a)}return P[P.length-1][1]};
function measure(){tTop=tour.getBoundingClientRect().top+scrollY;tLen=Math.max(1,tour.offsetHeight-innerHeight);
  const d=Math.min(2,devicePixelRatio||1);cv.width=Math.round(cv.clientWidth*d);cv.height=Math.round(cv.clientHeight*d);lastDraw=''}
const prog=()=>clamp((scrollY-tTop)/tLen,0,1);
function pick(i){i=clamp(i,0,NF-1);if(ok[i])return i;for(let k=1;k<NF;k++){if(i-k>=0&&ok[i-k])return i-k;if(i+k<NF&&ok[i+k])return i+k}return -1}
function draw(f){
  const t=lp(TM,f)*(NF-1), i0=Math.floor(t), fr=t-i0, a=pick(i0), b=pick(i0+1); if(a<0)return;
  const W=cv.width,H=cv.height,fx=innerWidth<768?lp(FX,f):.5;
  const key=a+'_'+b+'_'+fr.toFixed(2)+'|'+W+'x'+H+'|'+fx.toFixed(3); if(key===lastDraw)return; lastDraw=key;
  const bw=Math.max(W,H*AR),bh=bw/AR,x=clamp(W/2-bw*fx,W-bw,0),y=(H-bh)/2;
  cx.globalAlpha=1;cx.drawImage(imgs[a],x,y,bw,bh);
  if(b>=0&&b!==a&&fr>.04){cx.globalAlpha=fr;cx.drawImage(imgs[b],x,y,bw,bh);cx.globalAlpha=1}
}
function vis(el,o){el.style.opacity=o.toFixed(4);el.style.visibility=o<=.001?'hidden':'visible'}
function render(p){
  const f=p*N, mob=innerWidth<768;
  draw(f);
  // Blick auf die Karte: Menütafel gestochen scharf
  const om=sn(ramp(f,HOLD[0],HOLD[0]+.14))*(1-sn(ramp(f,HOLD[1]-.14,HOLD[1])));vis(mcard,om);
  $('.in',mcard).style.transform=`translate3d(0,${((1-om)*30).toFixed(1)}px,0) scale(${(.96+.04*om).toFixed(4)})`;
  // Tresen: Burger knallen drauf, dann Zoom in den Cheeseburger
  const o5=sn(ramp(f,5.5,5.62)); vis(s5,o5);
  if(f>=5.7&&!dropped){dropped=true;s5.classList.add('drop');shT.forEach(clearTimeout);shT=[0,.17,.34,.53].map(d=>setTimeout(()=>{stg.classList.remove('shake');void stg.offsetWidth;stg.classList.add('shake')},(d+.78*.56)*1000))}
  else if(f<5.55&&dropped){dropped=false;s5.classList.remove('drop');shT.forEach(clearTimeout);stg.classList.remove('shake')}
  cam5.style.transformOrigin=mob?'44.3% 69%':'60.5% 66%';
  cam5.style.transform=`scale(${(1+(mob?1.25:1.55)*sn(ramp(f,6.25,6.95))).toFixed(4)})`;
  // Texte
  const win=(a0,a1,b0,b1)=>sm(ramp(f,a0,a1))*(b0==null?1:1-sm(ramp(f,b0,b1)));
  CAPW.forEach((w,j)=>{const a=win(...w);caps[j].style.opacity=a.toFixed(3);caps[j].style.transform=`translate3d(0,${((1-a)*18).toFixed(2)}px,0)`;caps[j].style.pointerEvents=a>.5?'auto':'none'});
  const io=1-sm(ramp(f,0,.22));intro.style.opacity=io.toFixed(3);intro.style.transform=`translate3d(0,${(-(1-io)*36).toFixed(2)}px,0)`;intro.style.pointerEvents=io<.5?'none':'';ish.style.opacity=io.toFixed(3);
  fl.style.transform=`scaleX(${p.toFixed(4)})`;
  let ch=0;CH.forEach((c,i)=>{if(f+.06>=c)ch=i});
  if(ch!==lastCh){nb.forEach((b,i)=>i===ch?b.setAttribute('aria-current','step'):b.removeAttribute('aria-current'));lastCh=ch}
}
// Glättung: Lenis macht das Scrollen weich, hier folgt der Film mit kleiner Trägheit
function tick(now){raf=0;const dt=lastT?Math.min(64,now-lastT):16.7;lastT=now;const d=target-cur,k=1-Math.pow(1-.16,dt/16.7);cur=Math.abs(d)<.0001?target:cur+d*k;if(cur===target)lastT=0;render(cur);if(cur!==target)raf=requestAnimationFrame(tick)}
const kick=()=>{if(!raf)raf=requestAnimationFrame(tick)};
function loadFrames(){
  const q=[],seen=new Set();let done=0,act=0;
  for(const step of [8,2,1])for(let i=0;i<NF;i+=step)if(!seen.has(i)){seen.add(i);q.push(i)}
  const next=()=>{while(act<6&&q.length){const i=q.shift();act++;const im=new Image();im.decoding='async';
    im.onload=im.onerror=()=>{act--;done++;if(im.naturalWidth){imgs[i]=im;ok[i]=1;lastDraw='';if(!raf)render(cur)}
      ldi.style.transform=`scaleX(${(done/NF).toFixed(3)})`;ldt.textContent=`Rundgang lädt ${Math.round(done/NF*100)} %`;if(done===NF)ld.classList.add('done');next()};
    im.src=`w/${String(i).padStart(3,'0')}.webp`}};
  next()}
let lenis=null;
if(!rm){
  measure();target=cur=prog();render(cur);loadFrames();
  try{if(window.Lenis){lenis=new Lenis({lerp:.085,smoothWheel:true});const lr=t=>{lenis.raf(t);requestAnimationFrame(lr)};requestAnimationFrame(lr)}}catch(e){lenis=null}
  addEventListener('scroll',()=>{target=prog();kick()},{passive:true});
  addEventListener('resize',()=>{measure();target=prog();render(cur)});
  const go=j=>{const y=tTop+(CH[j]+(j?.08:0))/N*tLen;lenis?lenis.scrollTo(y,{duration:1.6}):scrollTo({top:y,behavior:'smooth'})};
  nb.forEach(b=>b.addEventListener('click',()=>go(+b.dataset.c)));
  $('#go').addEventListener('click',e=>{e.preventDefault();go(1)});
}
