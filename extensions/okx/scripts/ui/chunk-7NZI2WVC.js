import{c as a}from"./chunk-HLX5DVID.js";import{m as f}from"./chunk-OZL64JKT.js";import{ac as R}from"./chunk-ZTS7374H.js";import{a as N}from"./chunk-B26CCOB3.js";import{F as m,pa as h}from"./chunk-BJO2AFCW.js";import{a as B}from"./chunk-DAL2TMJA.js";import{f as o,m as s,o as u}from"./chunk-JEQEC2HU.js";s();u();var t=o(B()),i=o(R());h();var p=o(N());var y=20*1e3,E=b=>{let k=(0,i.useDispatch)(),c=f(void 0,b),r=(0,t.useRef)(null);(0,t.useEffect)(()=>{let n=()=>{clearInterval(r.current),r.current=null},l=async()=>{try{let e=await c();if(m(e)){n();return}let d=await(0,p.default)(e.eth.getBlockNumber)();k(a(d))}catch(e){console.log(`fetch block failed 
${e}`)}};return l(),r.current=setInterval(()=>{l()},y),()=>{n()}},[c])},I=E;export{I as a};

window.inOKXExtension = true;
window.inMiniApp = false;
window.ASSETS_BUILD_TYPE = "publish";

//# sourceMappingURL=chunk-7NZI2WVC.js.map
