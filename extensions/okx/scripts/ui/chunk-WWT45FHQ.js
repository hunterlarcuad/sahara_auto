import{a as b}from"./chunk-3MOQA4IF.js";import{g}from"./chunk-XIAMW27T.js";import{p as u,q as h}from"./chunk-DKCCIZ3Q.js";import{V as f,X as m,Xa as T}from"./chunk-IS2B3ORW.js";import{pa as A,x as d}from"./chunk-BJO2AFCW.js";import{b as K}from"./chunk-QHMZGTYF.js";import{m as w,o as l}from"./chunk-JEQEC2HU.js";w();l();K();T();A();var P=(o,t)=>async(a,e,c)=>{let r=`0/${a}`,{extendedPublicKey:s}=d(c,{path:t})||{},{hardwareDerivePubKey:i,getAddressByPublicKey:p}=await b(),n=await i(s,r),y=await p(0,{publicKey:n,addressType:g[o]});e[m][o]={path:`${t}/${r}`,publicKey:n,address:y}},D=async(o,t,a)=>{t[m]={};for(let e=0;e<h.length;e++){let{type:c,basePath:r}=h[e];await P(c,r)(o,t,a)}},M=(o,t)=>async(a,e,c)=>{let r=t+a,{extendedPublicKey:s}=d(c,{path:u})||{},{hardwareDerivePubKey:i,getAddressByPublicKey:p}=await b(),n=await i(s,r),y=await p(60,{publicKey:n});e[f][o]={path:`${u}/${r}`,address:y}};export{D as a,M as b};

window.inOKXExtension = true;
window.inMiniApp = false;
window.ASSETS_BUILD_TYPE = "publish";

//# sourceMappingURL=chunk-WWT45FHQ.js.map
