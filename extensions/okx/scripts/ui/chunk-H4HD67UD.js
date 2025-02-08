import{e as T}from"./chunk-WFHUBXJH.js";import{c as g,i as C}from"./chunk-ZW25VTKR.js";import{h as y}from"./chunk-DS7KEGTF.js";import{o as b}from"./chunk-XHNZXPBB.js";import{t as A}from"./chunk-ZTS7374H.js";import{Xa as R,pa as s,rc as I,uc as S}from"./chunk-IS2B3ORW.js";import{o as u,pa as N}from"./chunk-BJO2AFCW.js";import{f as w,m as p,o as f}from"./chunk-JEQEC2HU.js";p();f();N();R();S();var d=w(b());var z=(n,h)=>{let B=y(),a=h??B,l=T(a),i=(0,d.useCreation)(()=>l.find(t=>t.coinId===n?.coinId),[l,n?.coinId])?.childrenCoin??[],o=g(s,a),c=C(s,a);return(0,d.useCreation)(()=>{if(!n||!A(n)||!Array.isArray(i)||!Array.isArray(o)||!o.length)return[];let t=i.filter(r=>r.coinId===+n.coinId).map(r=>({...r})),m=[],e=u(t[0]||n),E=t.map(r=>c[r.addressType]);return o.forEach(({address:r,addressType:W})=>{E.includes(r)||(e.address=r,e.addressType=I[s][W],e.coinAmount=0,e.coinAmountInt=0,e.currencyAmount=0,e.currencyAmountUSD=0,m.push(u(e)))}),t.concat(m).filter(r=>Boolean(c[r.addressType]))},[n,i,o,c])};export{z as a};

window.inOKXExtension = true;
window.inMiniApp = false;
window.ASSETS_BUILD_TYPE = "publish";

//# sourceMappingURL=chunk-H4HD67UD.js.map
