import{S as j,i as B,s as E,e as g,a as q,t as J,b as d,d as S,f as D,g as m,l as K,h as N,w as T,n as H,E as P,c as h,m as k,j as v,k as w,o as C,P as Q,Q as R,H as y,N as z,R as A,T as F,K as G,J as I}from"./index.3a2fd726.js";import{B as L}from"./Block.6d18beac.js";import"./styles.ed3b21b5.js";function M(s){let e,t,a,i,c,r,f;return{c(){e=g("label"),t=g("input"),a=q(),i=g("span"),c=J(s[2]),t.disabled=s[1],t.checked=s[0],d(t,"type","checkbox"),d(t,"name","test"),d(t,"class","gr-check-radio gr-checkbox"),d(i,"class","ml-2"),d(e,"class","flex items-center text-gray-700 text-sm space-x-2 rounded-lg cursor-pointer dark:bg-transparent "),S(e,"!cursor-not-allowed",s[1])},m(u,l){D(u,e,l),m(e,t),m(e,a),m(e,i),m(i,c),r||(f=K(t,"change",s[4]),r=!0)},p(u,[l]){l&2&&(t.disabled=u[1]),l&1&&(t.checked=u[0]),l&4&&N(c,u[2]),l&2&&S(e,"!cursor-not-allowed",u[1])},i:T,o:T,d(u){u&&H(e),r=!1,f()}}}function O(s,e,t){let{value:a}=e,{disabled:i=!1}=e,{label:c}=e;const r=P();function f(l){t(0,a=l.currentTarget.checked),r("change",a)}const u=l=>f(l);return s.$$set=l=>{"value"in l&&t(0,a=l.value),"disabled"in l&&t(1,i=l.disabled),"label"in l&&t(2,c=l.label)},[a,i,c,f,u]}class U extends j{constructor(e){super(),B(this,e,O,M,E,{value:0,disabled:1,label:2})}}function V(s){let e,t,a,i,c;const r=[s[6]];let f={};for(let n=0;n<r.length;n+=1)f=Q(f,r[n]);e=new R({props:f});function u(n){s[7](n)}let l={label:s[3],disabled:s[4]==="static"};return s[0]!==void 0&&(l.value=s[0]),a=new U({props:l}),y.push(()=>z(a,"value",u)),a.$on("change",s[8]),{c(){h(e.$$.fragment),t=q(),h(a.$$.fragment)},m(n,b){k(e,n,b),D(n,t,b),k(a,n,b),c=!0},p(n,b){const o=b&64?A(r,[F(n[6])]):{};e.$set(o);const _={};b&8&&(_.label=n[3]),b&16&&(_.disabled=n[4]==="static"),!i&&b&1&&(i=!0,_.value=n[0],G(()=>i=!1)),a.$set(_)},i(n){c||(v(e.$$.fragment,n),v(a.$$.fragment,n),c=!0)},o(n){w(e.$$.fragment,n),w(a.$$.fragment,n),c=!1},d(n){C(e,n),n&&H(t),C(a,n)}}}function W(s){let e,t;return e=new L({props:{visible:s[2],elem_id:s[1],disable:typeof s[5].container=="boolean"&&!s[5].container,$$slots:{default:[V]},$$scope:{ctx:s}}}),{c(){h(e.$$.fragment)},m(a,i){k(e,a,i),t=!0},p(a,[i]){const c={};i&4&&(c.visible=a[2]),i&2&&(c.elem_id=a[1]),i&32&&(c.disable=typeof a[5].container=="boolean"&&!a[5].container),i&601&&(c.$$scope={dirty:i,ctx:a}),e.$set(c)},i(a){t||(v(e.$$.fragment,a),t=!0)},o(a){w(e.$$.fragment,a),t=!1},d(a){C(e,a)}}}function X(s,e,t){let{elem_id:a=""}=e,{visible:i=!0}=e,{value:c=!1}=e,{label:r="Checkbox"}=e,{mode:f}=e,{style:u={}}=e,{loading_status:l}=e;function n(o){c=o,t(0,c)}function b(o){I.call(this,s,o)}return s.$$set=o=>{"elem_id"in o&&t(1,a=o.elem_id),"visible"in o&&t(2,i=o.visible),"value"in o&&t(0,c=o.value),"label"in o&&t(3,r=o.label),"mode"in o&&t(4,f=o.mode),"style"in o&&t(5,u=o.style),"loading_status"in o&&t(6,l=o.loading_status)},[c,a,i,r,f,u,l,n,b]}class Y extends j{constructor(e){super(),B(this,e,X,W,E,{elem_id:1,visible:2,value:0,label:3,mode:4,style:5,loading_status:6})}}var $=Y;const ee=["static","dynamic"];export{$ as Component,ee as modes};
