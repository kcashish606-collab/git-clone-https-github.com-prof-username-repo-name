// Usage: node videos/render.js <folder> <prefix: T|M>   e.g. node videos/render.js videos/02-tibet-no-fly T
const {chromium}=require('playwright');const path=require('path');
(async()=>{const [,,dir,pre]=process.argv;const b=await chromium.launch();const p=await b.newPage({viewport:{width:1280,height:720}});
for(const n of [1,2,3]){await p.goto('file://'+path.resolve(dir,'thumbnails/thumbnail-source.html')+'?v='+pre+n);await p.waitForTimeout(300);
await p.locator('#c').screenshot({path:path.join(dir,'thumbnails','thumbnail-'+n+'.png')});}await b.close();})();
