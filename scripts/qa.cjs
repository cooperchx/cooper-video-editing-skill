const {chromium}=require('playwright');const fs=require('fs'),path=require('path'),assert=require('assert/strict');
(async()=>{
 const root=path.resolve(__dirname,'..');const browser=await chromium.launch({headless:true,executablePath:process.env.CHROME_PATH||undefined,args:['--allow-file-access-from-files']});
 const report={themes:2,scenes:30,errors:[],checks:[]};
 try{
  const page=await browser.newPage({viewport:{width:1280,height:1000}});page.on('pageerror',e=>report.errors.push(e.message));
  await page.goto(process.env.PREVIEW_URL||'file://'+path.join(root,'docs/index.html'));await page.evaluate(()=>motionLibrary.ready);
  assert.equal(await page.evaluate(()=>document.fonts.check('40px YanSong','动画风格')),true);
  for(const theme of ['blue','teal'])for(let id=1;id<=30;id++){
   await page.evaluate(({id,theme})=>{motionLibrary.setTheme(theme);motionLibrary.select(id,{autoplay:false});motionLibrary.seek(2)},{id,theme});
   const state=await page.evaluate(()=>motionLibrary.getState());assert.equal(state.scene,id);assert.equal(state.palette,theme);
   for(const t of [0,2,4.5])await page.evaluate(t=>motionLibrary.seek(t),t);
   if([2,8,18,24,25,30].includes(id)){
    await page.evaluate(()=>motionLibrary.seek(2));await page.evaluate(()=>new Promise(r=>requestAnimationFrame(()=>requestAnimationFrame(r))));const domA=await page.locator('#scene-root').innerHTML();const a=await page.locator('#viewer').screenshot();await page.evaluate(()=>{motionLibrary.seek(.3);motionLibrary.seek(2)});await page.evaluate(()=>new Promise(r=>requestAnimationFrame(()=>requestAnimationFrame(r))));assert.equal(await page.locator('#scene-root').innerHTML(),domA,`DOM state differs ${theme}/${id}`);const b=await page.locator('#viewer').screenshot();if(!a.equals(b)){
     const metric=await page.evaluate(async ([a,b])=>{const images=await Promise.all([a,b].map(src=>new Promise((resolve,reject)=>{const i=new Image();i.onload=()=>resolve(i);i.onerror=reject;i.src=src})));const canvas=document.createElement('canvas');canvas.width=images[0].width;canvas.height=images[0].height;const ctx=canvas.getContext('2d');const data=images.map(i=>{ctx.clearRect(0,0,canvas.width,canvas.height);ctx.drawImage(i,0,0);return ctx.getImageData(0,0,canvas.width,canvas.height).data});let changed=0,error=0;for(let i=0;i<data[0].length;i+=4){let d=0;for(let j=0;j<3;j++)d+=Math.abs(data[0][i+j]-data[1][i+j]);if(d>15)changed++;error+=d;}return{changedRatio:changed/(canvas.width*canvas.height),meanChannelError:error/(canvas.width*canvas.height*3)};},['data:image/png;base64,'+a.toString('base64'),'data:image/png;base64,'+b.toString('base64')]);
     assert(metric.changedRatio<.001&&metric.meanChannelError<.15,`seek raster discrepancy ${theme}/${id}: ${JSON.stringify(metric)}`);(report.rasterToleranceCases ||= []).push({theme,id,...metric});
    }
   }
  }
  report.checks.push('60 theme-scene combinations at entry, hold and late frames','12 seek comparisons; exact DOM state; raster tolerance <0.1% significant pixels and <0.15 mean channel error','font loads');
  for(const [id,selector,value] of [[25,'#liquid-value','72%'],[26,'#ring-value','78%'],[30,'#aggregate-value','50']]){
   await page.evaluate(id=>{motionLibrary.select(id,{autoplay:false});motionLibrary.seek(5)},id);assert.equal(await page.locator(selector).textContent(),value);
  }
  report.checks.push('liquid/ring/aggregate final values');
  await page.evaluate(()=>{motionLibrary.select(2,{autoplay:false});motionLibrary.configure({title:'测试标题',sub:'可编辑说明'});motionLibrary.seek(2)});assert((await page.locator('#scene-root').innerText()).includes('测试标题'));report.checks.push('editable text');
  await page.setViewportSize({width:390,height:844});assert(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1));report.checks.push('mobile viewport no horizontal overflow');
  await page.goto((process.env.PREVIEW_URL||'file://'+path.join(root,'docs/index.html')).replace(/index.html.*$/,'guide.html'));
  await page.waitForLoadState('load');assert.equal(await page.locator('img').count(),63);report.checks.push('documentation contains 63 GIF examples');
  assert.equal(report.errors.length,0,report.errors.join('\n'));
 }finally{await browser.close();fs.writeFileSync(path.join(root,'assets/browser-qa.json'),JSON.stringify(report,null,2)+'\n');console.log(JSON.stringify(report));}
})().catch(e=>{console.error(e);process.exitCode=1});
