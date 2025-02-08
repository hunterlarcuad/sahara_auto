import{a as u}from"./chunk-O4FKU574.js";import{a as h}from"./chunk-RUGU7MNC.js";import{b as l}from"./chunk-OFUXQTAD.js";import{a as m}from"./chunk-CBDQQ72I.js";import{b as i}from"./chunk-A2W6OJDL.js";import{c as t}from"./chunk-HBMVMNWX.js";import{pa as F,r as f}from"./chunk-BJO2AFCW.js";import{M as N,n as p}from"./chunk-OIAB2YVD.js";import{a as I}from"./chunk-DAL2TMJA.js";import{f as w,m as e,o as r}from"./chunk-JEQEC2HU.js";e();r();var n=w(I());F();N();e();r();var o={refreshWrapper:"_refreshWrapper_ec3nw_1",refresh:"_refresh_ec3nw_1",loading:"_loading_ec3nw_27",rotate:"_rotate_ec3nw_1"};var z=({className:g="",handleRefresh:s,status:a})=>{let d=u(),_=async()=>{p.trigger(h)},{successHaptic:y,impactHaptic:x}=m(),L=f(async()=>{s("loading"),x();try{await Promise.all([l(),d(),_()]),s("success"),y()}catch{s("error")}},800,{leading:!0});return a==="hidden"?null:n.default.createElement(t.FlexBox,{align:t.ALIGN.center,justify:t.ALIGN.center,className:`${o.refreshWrapper} ${g}`,onClick:c=>{c.stopPropagation(),a!=="loading"&&L()}},n.default.createElement(i,{size:i.SIZE.xs,icon:"okx-wallet-plugin-refresh",className:`${o.refresh} ${a==="loading"&&o.loading}`}))};export{z as a};

window.inOKXExtension = true;
window.inMiniApp = false;
window.ASSETS_BUILD_TYPE = "publish";

//# sourceMappingURL=chunk-AGWI7YU5.js.map
