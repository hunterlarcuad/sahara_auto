import{d as o,f as A}from"./chunk-B26CCOB3.js";import{Qc as a,Tc as n,Vc as x,Wc as c,Xc as y}from"./chunk-IS2B3ORW.js";import{m as s,o as u}from"./chunk-JEQEC2HU.js";s();u();x();y();A();var l=async(t={})=>{let{data:e}=await a(c.queryAccountExist,t);return e},q=async t=>{let{data:e}=await a(c.queryAccountInfo,t);return e},w=async(t,e)=>{let r=await o().getSignRequestHeaders({walletId:e});return await n(c.createWaxAccount,t,{headers:r})||{}},g=async(t,e)=>{let r=await o().getSignRequestHeaders({walletId:e});return await n(c.createFreeWaxAccount,t,{headers:r})||{}},W=async t=>{let{data:e}=await a(c.queryAccountStatus,t);return e||{}},h=async t=>{let{data:e}=await a(c.checkAccountPattern,t);return e??!1};export{l as a,q as b,w as c,g as d,W as e,h as f};

window.inOKXExtension = true;
window.inMiniApp = false;
window.ASSETS_BUILD_TYPE = "publish";

//# sourceMappingURL=chunk-4KRBAMDM.js.map
