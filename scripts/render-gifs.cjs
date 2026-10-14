const {chromium}=require('playwright');
const fs=require('node:fs');const path=require('node:path');const os=require('node:os');const {spawnSync}=require('node:child_process');
const root=path.resolve(__dirname,'..');
const options=Object.fromEntries(process.argv.slice(2).map(a=>{const [k,v]=a.replace(/^--/,'').split('=');return[k,v]}));
const ids=(options.ids||Array.from({length:30},(_,i)=>i+1).join(',')).split(',').map(Number);
const themes=(options.themes||'blue,teal').split(',');const fps=Number(options.fps||10);const width=Number(options.width||640);const height=width*9/16;
const encode=(dir,target)=>{const r=spawnSync('ffmpeg',['-hide_banner','-loglevel','error','-y','-framerate',String(fps),'-i',path.join(dir,'%04d.png'),'-filter_complex','[0:v]split[a][b];[a]palettegen=max_colors=96:stats_mode=diff[p];[b][p]paletteuse=dither=sierra2_4a','-loop','0',target],{encoding:'utf8'});if(r.status!==0)throw Error(r.stderr);};
(async()=>{
 const browser=await chromium.launch({headless:true,executablePath:process.env.CHROME_PATH||undefined,args:['--allow-file-access-from-files']});
 const page=await browser.newPage({viewport:{width,height},deviceScaleFactor:1});const errors=[];page.on('pageerror',e=>errors.push(e.message));
 await page.goto(options.url||'file://'+path.join(root,'docs/index.html')+'?embed=1');
 await page.evaluate(()=>motionLibrary.ready);await page.evaluate(()=>motionLibrary.seek(0));
 const output=path.resolve(options.out||path.join(root,'docs/assets/gifs'));fs.mkdirSync(output,{recursive:true});
 const report=[];
 for(const theme of themes)for(const id of ids){
  const duration=await page.evaluate(({id,theme})=>{motionLibrary.setTheme(theme);motionLibrary.select(id,{autoplay:false});motionLibrary.seek(0);return motionLibrary.scenes.find(s=>s.id===id).duration;},{id,theme});
  await page.evaluate(()=>document.fonts.ready);
  const dir=fs.mkdtempSync(path.join(os.tmpdir(),'cooper-gif-'));const frames=Math.ceil(duration*fps);
  try{for(let f=0;f<frames;f++){await page.evaluate(t=>motionLibrary.seek(t),f/fps);await page.screenshot({path:path.join(dir,String(f).padStart(4,'0')+'.png')});}
   const name=`${theme}-${String(id).padStart(2,'0')}.gif`;encode(dir,path.join(output,name));report.push({id,theme,frames,fps,duration,name,bytes:fs.statSync(path.join(output,name)).size});console.log(`${name}: ${frames} frames`);
  }finally{fs.rmSync(dir,{recursive:true,force:true});}
 }
 await browser.close();const reportPath=path.join(root,'assets/gif-render-report.json');const previous=fs.existsSync(reportPath)?JSON.parse(fs.readFileSync(reportPath,'utf8')).items:[];const merged=new Map(previous.map(item=>[item.theme+'/'+item.id,item]));for(const item of report)merged.set(item.theme+'/'+item.id,item);fs.writeFileSync(reportPath,JSON.stringify({resolution:[width,height],errors,publicMedia:'Original synthetic illustrations',items:[...merged.values()].sort((a,b)=>a.theme.localeCompare(b.theme)||a.id-b.id)},null,2)+'\n');if(errors.length)throw Error(errors.join('\n'));
})().catch(e=>{console.error(e);process.exitCode=1});
