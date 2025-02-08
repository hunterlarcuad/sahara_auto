import{b as c}from"./chunk-LZKLGZM5.js";import{h as u}from"./chunk-DS7KEGTF.js";import{o as k}from"./chunk-XHNZXPBB.js";import{Qc as m,Vc as W,Wc as a,Xc as _,lb as n,vb as C}from"./chunk-IS2B3ORW.js";import{j as i,pa as L}from"./chunk-BJO2AFCW.js";import{M as b,n as f}from"./chunk-OIAB2YVD.js";import{a as E}from"./chunk-DAL2TMJA.js";import{f as r,m as o,o as s}from"./chunk-JEQEC2HU.js";o();s();var l=r(E()),p=r(k());L();b();C();_();W();var T="update_defi_list",M=()=>{let d=u(),I=n(),t=(0,p.useRequest)(async()=>{let D=await m(a.getDefiList,{accountId:d});return i(D,["data","platformListByAccountId","0","platformListVoList"],[]).filter(g=>I.find(h=>Number(h.netWorkId)===g.chainId))},{manual:!0}),e=c("invest-DeFi",{onError:t.refresh,pollingInterval:30*1e3});return(0,l.useEffect)(()=>{e&&t.refresh()},[e]),f.listen(T,t.refresh,!1),t};export{T as a,M as b};

window.inOKXExtension = true;
window.inMiniApp = false;
window.ASSETS_BUILD_TYPE = "publish";

//# sourceMappingURL=chunk-RUGU7MNC.js.map
