import{Za as u,x as h}from"./chunk-ZTS7374H.js";import{f as p,m as i,o as l}from"./chunk-JEQEC2HU.js";i();l();var f=p(h());function A(e){return e.metamask.addressBookList||[]}function g(e){return e.metamask.recentlyAddresses||{}}var I=(0,f.createSelector)(u,(e,t)=>{let{selectedWallet:r,keyringIdentities:s}=e.keyring;return{selectedWallet:r,keyringIdentities:s,chainId:t}},(e,{selectedWallet:t,keyringIdentities:r,chainId:s})=>{let m=(e||[]).find(n=>+n.chainId==+s)?.localType,d=[],c="";return r.forEach(n=>{n.walletIdentities.forEach(a=>{let o=a.account[m];a.walletId===t&&(c=o),o&&d.push(o)})}),{currentAddress:c,allAddress:d}});export{A as a,g as b,I as c};

window.inOKXExtension = true;
window.inMiniApp = false;
window.ASSETS_BUILD_TYPE = "publish";

//# sourceMappingURL=chunk-6NFIXY6G.js.map
