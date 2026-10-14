import fs from 'node:fs/promises';
import path from 'node:path';
import http from 'node:http';
import {fileURLToPath} from 'node:url';
import {createRequire} from 'node:module';
const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..'),website=path.resolve(root,'../my_web');
const require=createRequire(path.join(website,'package.json'));
const {chromium}=require('@playwright/test');
const mime={'.html':'text/html','.js':'application/javascript','.css':'text/css','.woff2':'font/woff2','.glb':'model/gltf-binary','.png':'image/png','.gif':'image/gif','.svg':'image/svg+xml'};
const server=http.createServer(async(req,res)=>{try{const url=new URL(req.url,'http://localhost'),name=decodeURIComponent(url.pathname);let file;if(name==='/')file=path.join(root,'tools/hero.html');else if(name.startsWith('/three/'))file=path.join(website,'node_modules/three',name.slice(7));else if(name.startsWith('/model/'))file=path.join(website,'public/models',name.slice(7));else if(name.startsWith('/font/'))file=path.join(website,'node_modules/@fontsource/noto-serif-sc',name.slice(6));else file=path.join(root,name);const data=await fs.readFile(file);res.setHeader('Content-Type',mime[path.extname(file)]||'application/octet-stream');res.end(data)}catch{res.statusCode=404;res.end('Not found')}});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const browser=await chromium.launch({headless:true,executablePath:process.env.CHROME_EXECUTABLE||'/Users/wander/Library/Caches/ms-playwright/chromium-1161/chrome-mac/Chromium.app/Contents/MacOS/Chromium'});
try{const page=await browser.newPage({viewport:{width:1200,height:480},deviceScaleFactor:1});page.on('pageerror',e=>console.error(e.message));await page.goto('http://127.0.0.1:'+server.address().port);await page.waitForFunction(()=>window.ready,{timeout:30000});await fs.mkdir(path.join(root,'tools/frames'),{recursive:true});await page.evaluate(()=>window.renderFrame(.2));await page.screenshot({path:path.join(root,'assets/hero.png')});const count=72;for(let i=0;i<count;i++){await page.evaluate(t=>window.renderFrame(t),i/count);await page.screenshot({path:path.join(root,'tools/frames',String(i).padStart(3,'0')+'.png')});if(i%18===0)console.log('frame '+i+'/'+count)}console.log('Banner frames rendered');}finally{await browser.close();await new Promise(r=>server.close(r))}
