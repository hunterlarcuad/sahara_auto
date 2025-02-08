import{d as a}from"./chunk-42AETIVN.js";import{m as n,o as e}from"./chunk-JEQEC2HU.js";n();e();n();e();async function o({action:t,params:i,maxSize:g=500}){try{let s=await a.log,r=await s.get(t)||{a:t,d:[]};Array.isArray(r?.d)||(r.d=[]);let c=r.d,l={t:new Date().toLocaleString(),p:i};c.unshift(l),g&&c.splice(g),await s.set(r)}catch{console.log("set data failed")}}async function y(t){return(await a.log).query(t)}var L=t=>o({action:"pv",params:t}),h=t=>o({action:"pms",params:t}),A=t=>o({action:"pc",params:t});var S=t=>o({action:"pr",params:t,maxSize:50});export{y as a,L as b,h as c,A as d,S as e};

window.inOKXExtension = true;
window.inMiniApp = false;
window.ASSETS_BUILD_TYPE = "publish";

//# sourceMappingURL=chunk-OOOTT4G3.js.map
