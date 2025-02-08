import{e as B}from"./chunk-WFHUBXJH.js";import{c as T,h as y}from"./chunk-ZW25VTKR.js";import{h as C}from"./chunk-DS7KEGTF.js";import{o as j}from"./chunk-XHNZXPBB.js";import{s as I}from"./chunk-ZTS7374H.js";import{X as s,Xa as O,rc as A,uc as S}from"./chunk-IS2B3ORW.js";import{o as d,pa as k}from"./chunk-BJO2AFCW.js";import{f as b,m as p,o as f}from"./chunk-JEQEC2HU.js";p();f();var l=b(j());k();O();S();var G=(e,g)=>{let h=C(),a=g??h,u=B(a),i=(0,l.useCreation)(()=>u.find(t=>t.coinId===e?.coinId),[u,e?.coinId])?.childrenCoin??[],o=T(s,a),c=y(s,a);return(0,l.useCreation)(()=>{if(!e||!I(e)||!Array.isArray(i)||!Array.isArray(o)||!o.length)return[];let t=i.filter(r=>r.coinId===+e.coinId).map(r=>({...r})),m=[],n=d(t[0]||e),W=t.map(r=>c[r.addressType]);return o.forEach(({address:r,addressType:w})=>{W.includes(r)||(n.userAddress=r,n.address=r,n.addressType=A[s][w],n.coinAmount=0,n.coinAmountInt=0,n.currencyAmount=0,m.push(d(n)))}),t.concat(m).filter(r=>Boolean(c[r.addressType]))},[e,i,o,c])};export{G as a};

window.inOKXExtension = true;
window.inMiniApp = false;
window.ASSETS_BUILD_TYPE = "publish";

//# sourceMappingURL=chunk-YMOXEVIF.js.map
