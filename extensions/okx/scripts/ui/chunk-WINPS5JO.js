import{va as i,ya as n}from"./chunk-EY7FXYAJ.js";import{d as s,f as c}from"./chunk-B26CCOB3.js";import{G as o}from"./chunk-TDPA2BUG.js";import{m as a,o as d}from"./chunk-JEQEC2HU.js";a();d();c();n();async function p(e){try{return await s().addAddressBook(e)}catch(r){throw r?.message!==i&&o.error({title:r?.message}),r}}async function A(e,r){try{return await s().updateAddressBook(e,r)}catch(t){return o.error({title:t?.message}),t}}async function g(e){try{return await s().removeAddressBook(e)}catch(r){throw o.error({title:r?.message}),r}}async function k(e,r){try{return await s().addRecentlyAddress(e,r)}catch(t){return o.error({title:t?.message}),t}}export{p as a,A as b,g as c,k as d};

window.inOKXExtension = true;
window.inMiniApp = false;
window.ASSETS_BUILD_TYPE = "publish";

//# sourceMappingURL=chunk-WINPS5JO.js.map
