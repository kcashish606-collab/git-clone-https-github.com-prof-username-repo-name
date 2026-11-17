const {chromium}=require('playwright');
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1280,height:720},deviceScaleFactor:1});
for(const v of ['A','B','C']){await p.goto('file://'+__dirname+'/thumbnail-source.html?v='+v);await p.waitForTimeout(300);
await p.locator('#c').screenshot({path:process.argv[2]+'/thumbnail-'+v+'.png'});}
await b.close();})();
