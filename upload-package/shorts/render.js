// Usage: node upload-package/shorts/render.js <1|2> [fps]   -> short-<n>.mp4 (1080x1920, silent AAC track)
const {chromium}=require('playwright');const path=require('path');const {spawn}=require('child_process');
(async()=>{const n=process.argv[2]||'1',fps=+(process.argv[3]||30);
const b=await chromium.launch();const p=await b.newPage({viewport:{width:1080,height:1920}});
await p.goto('file://'+path.resolve(__dirname,'shorts-source.html')+'?s='+n);await p.waitForTimeout(500);
const dur=await p.evaluate('DUR'),N=Math.round(dur*fps);const out=path.join(__dirname,`short-${n}.mp4`);
const ff=spawn('ffmpeg',['-y','-loglevel','error','-f','image2pipe','-framerate',String(fps),'-i','-','-f','lavfi','-i','anullsrc=r=44100:cl=stereo',
 '-c:v','libx264','-pix_fmt','yuv420p','-preset','medium','-crf','20','-c:a','aac','-shortest','-movflags','+faststart',out],{stdio:['pipe','inherit','inherit']});
for(let i=0;i<N;i++){await p.evaluate(t=>render(t),i/fps);const buf=await p.screenshot({type:'jpeg',quality:92});
 if(!ff.stdin.write(buf))await new Promise(r=>ff.stdin.once('drain',r));}
ff.stdin.end();await new Promise(r=>ff.on('close',r));await b.close();console.log('wrote',out,N,'frames');})();
