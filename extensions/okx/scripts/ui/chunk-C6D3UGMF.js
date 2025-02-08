import{Bb as p,Cb as D,dc as u,ec as k}from"./chunk-IS2B3ORW.js";import{G as g,pa as v}from"./chunk-BJO2AFCW.js";import{a as M}from"./chunk-DAL2TMJA.js";import{f as E,l as process,m as d,o as c}from"./chunk-JEQEC2HU.js";d();c();var e=E(M());v();k();D();var C=(t,a={})=>{let[s,f]=(0,e.useState)(null),[w,T]=(0,e.useState)(null),[o,y]=(0,e.useState)(a);return(0,e.useEffect)(()=>{g(a,o)||y(a)},[a]),(0,e.useEffect)(()=>{let r=document.getElementById("sandbox"),l,i=n=>{n.data.chanel===t&&T(n.data)},m=n=>{n.data.status===201&&(window.removeEventListener("message",m),clearInterval(l),window.addEventListener("message",i),f(r))},b=u();return l=setInterval(()=>{r.contentWindow?.postMessage({status:200,buildType:process.env.ASSETS_BUILD_TYPE,cdn:p(),browser:b},"*")},1e3),window.addEventListener("message",m),()=>{window.removeEventListener("message",i)}},[]),(0,e.useEffect)(()=>{t&&s&&s.contentWindow?.postMessage({chanel:t,data:o},"*")},[t,s,o]),w};export{C as a};

window.inOKXExtension = true;
window.inMiniApp = false;
window.ASSETS_BUILD_TYPE = "publish";

//# sourceMappingURL=chunk-C6D3UGMF.js.map
