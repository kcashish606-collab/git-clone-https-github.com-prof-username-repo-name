// Usage: node videos/04-paper-boat/video/render.js [out.mp4] [voice.wav]
// Renders story.html to 1920x1080 30fps H.264. With a voice track, muxes it in; otherwise adds a silent track.
const {chromium}=require('playwright');const path=require('path');const {spawn}=require('child_process');
(async()=>{const out=process.argv[2]||path.join(__dirname,'the-paper-boat-1080p.mp4'),voice=process.argv[3],fps=30;
const b=await chromium.launch();const p=await b.newPage({viewport:{width:1920,height:1080}});
await p.goto('file://'+path.join(__dirname,'story.html'));await p.waitForTimeout(500);
const N=Math.round(await p.evaluate('DUR')*fps);
const aud=voice?['-i',voice]:['-f','lavfi','-i','anullsrc=r=44100:cl=stereo'];
const ff=spawn('ffmpeg',['-y','-loglevel','error','-f','image2pipe','-framerate',String(fps),'-i','-',...aud,'-map','0:v','-map','1:a',
 '-c:v','libx264','-pix_fmt','yuv420p','-preset','medium','-crf','20','-c:a','aac','-b:a','192k','-shortest','-movflags','+faststart',out],{stdio:['pipe','inherit','inherit']});
for(let i=0;i<N;i++){await p.evaluate(t=>render(t),i/fps);const buf=await p.screenshot({type:'jpeg',quality:90});
 if(!ff.stdin.write(buf))await new Promise(r=>ff.stdin.once('drain',r));if(i%900===0)console.log('frame',i,'/',N);}
ff.stdin.end();await new Promise(r=>ff.on('close',r));await b.close();console.log('wrote',out);})();
