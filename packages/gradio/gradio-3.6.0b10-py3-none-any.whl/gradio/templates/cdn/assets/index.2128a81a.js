import{S as w,i as j,s as q,e as b,t as A,a as v,c as S,b as g,d as p,f as y,g as d,m as z,l as B,h as D,j as C,k,n as E,o as F,p as G,u as H,q as I,r as J}from"./index.3a2fd726.js";import{C as K}from"./Column.59350727.js";import"./styles.ed3b21b5.js";function L(n){let e;const s=n[6].default,l=G(s,n,n[7],null);return{c(){l&&l.c()},m(t,r){l&&l.m(t,r),e=!0},p(t,r){l&&l.p&&(!e||r&128)&&H(l,s,t,t[7],e?J(s,t[7],r,null):I(t[7]),null)},i(t){e||(C(l,t),e=!0)},o(t){k(l,t),e=!1},d(t){l&&l.d(t)}}}function M(n){let e,s,l,t,r,u,m,i,f,_,o;return i=new K({props:{visible:n[3],$$slots:{default:[L]},$$scope:{ctx:n}}}),{c(){e=b("div"),s=b("div"),l=b("span"),t=A(n[0]),r=v(),u=b("span"),u.textContent="\u25BC",m=v(),S(i.$$.fragment),g(u,"class","transition"),p(u,"rotate-90",!n[3]),g(s,"class","w-full flex justify-between cursor-pointer"),g(e,"id",n[1]),g(e,"class","p-3 border border-gray-200 dark:border-gray-700 rounded-lg flex flex-col gap-3 hover:border-gray-300 dark:hover:border-gray-600 transition"),p(e,"hidden",!n[2])},m(a,c){y(a,e,c),d(e,s),d(s,l),d(l,t),d(s,r),d(s,u),d(e,m),z(i,e,null),f=!0,_||(o=B(s,"click",n[4]),_=!0)},p(a,[c]){(!f||c&1)&&D(t,a[0]),c&8&&p(u,"rotate-90",!a[3]);const h={};c&8&&(h.visible=a[3]),c&128&&(h.$$scope={dirty:c,ctx:a}),i.$set(h),(!f||c&2)&&g(e,"id",a[1]),c&4&&p(e,"hidden",!a[2])},i(a){f||(C(i.$$.fragment,a),f=!0)},o(a){k(i.$$.fragment,a),f=!1},d(a){a&&E(e),F(i),_=!1,o()}}}function N(n,e,s){let{$$slots:l={},$$scope:t}=e,{label:r}=e,{elem_id:u}=e,{visible:m=!0}=e,{open:i=!0}=e,f=i;const _=()=>{s(3,f=!f)};return n.$$set=o=>{"label"in o&&s(0,r=o.label),"elem_id"in o&&s(1,u=o.elem_id),"visible"in o&&s(2,m=o.visible),"open"in o&&s(5,i=o.open),"$$scope"in o&&s(7,t=o.$$scope)},[r,u,m,f,_,i,l,t]}class O extends w{constructor(e){super(),j(this,e,N,M,q,{label:0,elem_id:1,visible:2,open:5})}}var T=O;const U=["static"];export{T as Component,U as modes};
