const w=t=>n=>{const e=t(n);return n.add(e),e},N=t=>(n,e)=>(t.set(n,e),e),f=Number.MAX_SAFE_INTEGER===void 0?9007199254740991:Number.MAX_SAFE_INTEGER,g=536870912,_=g*2,O=(t,n)=>e=>{const r=n.get(e);let s=r===void 0?e.size:r<_?r+1:0;if(!e.has(s))return t(e,s);if(e.size<g){for(;e.has(s);)s=Math.floor(Math.random()*_);return t(e,s)}if(e.size>f)throw new Error("Congratulations, you created a collection of unique numbers which uses all available integers!");for(;e.has(s);)s=Math.floor(Math.random()*f);return t(e,s)},M=new WeakMap,m=N(M),h=O(m,M),I=w(h),R=t=>typeof t.start=="function",p=new WeakMap,A=t=>({...t,connect:({call:n})=>async()=>{const{port1:e,port2:r}=new MessageChannel,s=await n("connect",{port:e},[e]);return p.set(r,s),r},disconnect:({call:n})=>async e=>{const r=p.get(e);if(r===void 0)throw new Error("The given port is not connected.");await n("disconnect",{portId:r})},isSupported:({call:n})=>()=>n("isSupported")}),E=new WeakMap,b=t=>{if(E.has(t))return E.get(t);const n=new Map;return E.set(t,n),n},W=t=>{const n=A(t);return e=>{const r=b(e);e.addEventListener("message",({data:o})=>{const{id:a}=o;if(a!==null&&r.has(a)){const{reject:u,resolve:c}=r.get(a);r.delete(a),o.error===void 0?c(o.result):u(new Error(o.error.message))}}),R(e)&&e.start();const s=(o,a=null,u=[])=>new Promise((c,l)=>{const d=h(r);r.set(d,{reject:l,resolve:c}),a===null?e.postMessage({id:d,method:o},u):e.postMessage({id:d,method:o,params:a},u)}),T=(o,a,u=[])=>{e.postMessage({id:null,method:o,params:a},u)};let i={};for(const[o,a]of Object.entries(n))i={...i,[o]:a({call:s,notify:T})};return{...i}}};export{I as a,W as c,h as g};
