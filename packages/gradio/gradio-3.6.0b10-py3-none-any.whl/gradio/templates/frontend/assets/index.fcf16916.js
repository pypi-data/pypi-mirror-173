import{S as k,i as w,s as M,e as B,b as f,Y as C,d as v,f as T,w as h,n as S,E as j,c,m as _,j as d,k as g,o as b,P as E,Q as H,a as L,R as q,T as D,J}from"./index.06d85743.js";import{B as P}from"./Block.324ba9b6.js";import"./styles.ed3b21b5.js";function Q(i){let e;return{c(){e=B("div"),f(e,"id",i[0]),f(e,"class","output-markdown gr-prose min-h-[4rem]"),C(e,"max-width","100%"),v(e,"hidden",!i[1])},m(n,t){T(n,e,t),e.innerHTML=i[2]},p(n,[t]){t&4&&(e.innerHTML=n[2]),t&1&&f(e,"id",n[0]),t&2&&v(e,"hidden",!n[1])},i:h,o:h,d(n){n&&S(e)}}}function R(i,e,n){let{elem_id:t=""}=e,{visible:s=!0}=e,{value:r}=e;const o=j();return i.$$set=a=>{"elem_id"in a&&n(0,t=a.elem_id),"visible"in a&&n(1,s=a.visible),"value"in a&&n(2,r=a.value)},i.$$.update=()=>{i.$$.dirty&4&&o("change")},[t,s,r]}class Y extends k{constructor(e){super(),w(this,e,R,Q,M,{elem_id:0,visible:1,value:2})}}function z(i){let e,n,t,s;const r=[i[3],{variant:"center"}];let o={};for(let a=0;a<r.length;a+=1)o=E(o,r[a]);return e=new H({props:o}),t=new Y({props:{value:i[2],elem_id:i[0],visible:i[1]}}),t.$on("change",i[5]),{c(){c(e.$$.fragment),n=L(),c(t.$$.fragment)},m(a,u){_(e,a,u),T(a,n,u),_(t,a,u),s=!0},p(a,u){const m=u&8?q(r,[D(a[3]),r[1]]):{};e.$set(m);const l={};u&4&&(l.value=a[2]),u&1&&(l.elem_id=a[0]),u&2&&(l.visible=a[1]),t.$set(l)},i(a){s||(d(e.$$.fragment,a),d(t.$$.fragment,a),s=!0)},o(a){g(e.$$.fragment,a),g(t.$$.fragment,a),s=!1},d(a){b(e,a),a&&S(n),b(t,a)}}}function A(i){let e,n;return e=new P({props:{visible:i[1],elem_id:i[0],disable:!0,$$slots:{default:[z]},$$scope:{ctx:i}}}),{c(){c(e.$$.fragment)},m(t,s){_(e,t,s),n=!0},p(t,[s]){const r={};s&2&&(r.visible=t[1]),s&1&&(r.elem_id=t[0]),s&143&&(r.$$scope={dirty:s,ctx:t}),e.$set(r)},i(t){n||(d(e.$$.fragment,t),n=!0)},o(t){g(e.$$.fragment,t),n=!1},d(t){b(e,t)}}}function F(i,e,n){let{label:t}=e,{elem_id:s=""}=e,{visible:r=!0}=e,{value:o=""}=e,{loading_status:a}=e;const u=j();function m(l){J.call(this,i,l)}return i.$$set=l=>{"label"in l&&n(4,t=l.label),"elem_id"in l&&n(0,s=l.elem_id),"visible"in l&&n(1,r=l.visible),"value"in l&&n(2,o=l.value),"loading_status"in l&&n(3,a=l.loading_status)},i.$$.update=()=>{i.$$.dirty&16&&u("change")},[s,r,o,a,t,m]}class G extends k{constructor(e){super(),w(this,e,F,A,M,{label:4,elem_id:0,visible:1,value:2,loading_status:3})}}var O=G;const U=["static"];export{O as Component,U as modes};
