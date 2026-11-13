// 上傳 YouTube 的分步工具（照 ~/ai-workshop-backend/scripts/yt-upload.mjs 的做法，直接操作已登入的 Studio 分頁）。
// node site/yt_step.mjs start <檔案>   開上傳對話框並送檔，印出分頁 id
// node site/yt_step.mjs ev <分頁id> '<JS 運算式>'   在那個分頁執行並印結果
const sleep = ms => new Promise(r => setTimeout(r, ms));
async function attach(id) {
  const t = (await (await fetch('http://localhost:9333/json')).json()).find(x => x.id === id);
  const ws = new WebSocket(t.webSocketDebuggerUrl); let n = 0; const pend = new Map();
  ws.onmessage = e => { const m = JSON.parse(e.data); if (m.id && pend.has(m.id)) { pend.get(m.id)(m); pend.delete(m.id); } };
  await new Promise(r => ws.onopen = r);
  const send = (method, params = {}, ms = 120000) => new Promise((res, rej) => { const i = ++n; pend.set(i, res); ws.send(JSON.stringify({ id: i, method, params })); setTimeout(() => rej(new Error('timeout ' + method)), ms); });
  const ev = async (expression, ms) => { const r = await send('Runtime.evaluate', { expression, returnByValue: true, awaitPromise: true }, ms); return r.result?.exceptionDetails ? '例外：' + JSON.stringify(r.result.exceptionDetails.exception?.description || r.result.exceptionDetails.text) : r.result?.result?.value; };
  await send('Page.bringToFront').catch(() => {}); await send('Emulation.setFocusEmulationEnabled', { enabled: true }).catch(() => {});
  return { send, ev, close: () => ws.close() };
}
const [cmd, a, b] = process.argv.slice(2);
if (cmd === 'start') {
  const t = await (await fetch('http://localhost:9333/json/new?' + encodeURI('https://studio.youtube.com/channel/UCOfFvRR1-TtYlok8FrwuE0A/videos/upload'), { method: 'PUT' })).json();
  const c = await attach(t.id); await sleep(12000);
  await c.ev(`(async()=>{(document.querySelector('#create-icon')||document.querySelector('button[aria-label=建立]')).click(); await new Promise(r=>setTimeout(r,1000)); document.querySelector('#text-item-0').click()})()`);
  await sleep(3000);
  const { root } = (await c.send('DOM.getDocument', { depth: -1, pierce: true })).result;
  const { nodeId } = (await c.send('DOM.querySelector', { nodeId: root.nodeId, selector: 'input[type=file]' })).result;
  await c.send('DOM.setFileInputFiles', { nodeId, files: [a] });
  await sleep(6000);
  console.log('分頁', t.id, '對話框', await c.ev(`!!document.querySelector('ytcp-uploads-dialog')`)); c.close();
} else if (cmd === 'ev') { const c = await attach(a); console.log(await c.ev(b, 120000)); c.close(); }
process.exit(0);
