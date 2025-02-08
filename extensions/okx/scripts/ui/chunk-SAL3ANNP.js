import{a as T,l as E}from"./chunk-DS7KEGTF.js";import{p as l,q as m}from"./chunk-4HJMB7P7.js";import{c as p,d,g as c}from"./chunk-D2RJYC6D.js";import{a as L}from"./chunk-YYAHGUV5.js";import{e as i}from"./chunk-DKCCIZ3Q.js";import{a as y}from"./chunk-DAL2TMJA.js";import{f as o,m as a,o as s}from"./chunk-JEQEC2HU.js";a();s();var f=o(T()),u=o(L());var C=o(y());var _=()=>{let e=(0,u.useHistory)(),t=E();return(0,C.useCallback)(async r=>{let g=await c.hasConnectedLedger(),{walletName:h}=t(r),n=`${m}?${f.default.stringify({type:i.addChain,walletId:r})}`;g?e.push(n):d.openModal(p.hardWareNotConnected,{walletName:h,onButtonClick:()=>{globalThis.platform.openExtensionInBrowser(l)},onExtButtonClick:()=>{globalThis.platform.openExtensionInBrowser(`${n}&hideBack=1`)}})},[e,t])};export{_ as a};

window.inOKXExtension = true;
window.inMiniApp = false;
window.ASSETS_BUILD_TYPE = "publish";

//# sourceMappingURL=chunk-SAL3ANNP.js.map
