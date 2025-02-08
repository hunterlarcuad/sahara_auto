import{j as r,k as s}from"./chunk-3MOQA4IF.js";import{b as d}from"./chunk-3SFQGMQT.js";import{f as u,m as e,o as i}from"./chunk-JEQEC2HU.js";e();i();var c=u(d());var y={inputs:[{internalType:"bytes",name:"_data",type:"bytes"}],name:"getL1Fee",outputs:[{internalType:"uint256",name:"",type:"uint256"}],stateMutability:"view",type:"function"},E=async t=>{let{Common:a,Hardfork:n,Chain:o}=await r(),m=a.forCustomChain(o.Mainnet,{chainId:10,networkId:10,defaultHardfork:n.SpuriousDragon}),{TransactionFactory:p}=await s();return p.fromTxData(t,{common:m})},D=async t=>{let n=(await E(t)).serialize();return c.default.encodeMethod(y,[n])};export{D as a};

window.inOKXExtension = true;
window.inMiniApp = false;
window.ASSETS_BUILD_TYPE = "publish";

//# sourceMappingURL=chunk-LLR77RUB.js.map
