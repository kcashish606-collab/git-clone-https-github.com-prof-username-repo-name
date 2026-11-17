// Usage: node channel-branding/render.js
const {chromium}=require('playwright');const path=require('path');
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:800,height:800}});
for(const n of [1,2,3]){await p.goto('file://'+path.resolve(__dirname,'profile-source.html')+'?v=P'+n);await p.waitForTimeout(300);
await p.locator('#c').screenshot({path:path.join(__dirname,'profile-picture-'+n+'.png')});}
// preview: how each looks as a small circle, like on YouTube
await p.setViewportSize({width:900,height:420});
const imgs=[1,2,3].map(n=>'file://'+path.join(__dirname,'profile-picture-'+n+'.png'));
await p.setContent(`<body style="margin:0;background:#0f0f0f;font:600 22px Inter;color:#fff;padding:30px">
${imgs.map((s,i)=>`<div style="display:inline-block;width:270px;text-align:center;vertical-align:top">
<img src="${s}" style="width:176px;height:176px;border-radius:50%"><br><br>
<img src="${s}" style="width:48px;height:48px;border-radius:50%;vertical-align:middle"> <img src="${s}" style="width:24px;height:24px;border-radius:50%;vertical-align:middle">
<div style="margin-top:12px">Option ${i+1}</div></div>`).join('')}</body>`);
await p.waitForTimeout(300);await p.screenshot({path:path.join(__dirname,'preview-as-circles.png')});
await b.close();})();
