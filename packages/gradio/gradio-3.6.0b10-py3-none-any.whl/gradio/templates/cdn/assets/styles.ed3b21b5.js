const u=(e,o)=>d[o](e[o]);function b(e,o){const r=o.reduce((a,t)=>(e[t]===void 0||!d[t]?a[t]=" ":a[t]=` ${u(e,t)} `,a),{});return r.classes=` ${Object.values(r).join(" ").replace(/\s+/g," ").trim()} `,r}const d={container(e){return e?"":"!p-0 !m-0 !border-0 !shadow-none !overflow-visible !bg-transparent"},label_container(e){return e?"":"!border-0 !shadow-none !overflow-visible !bg-transparent"},grid(e){let o=["","sm:","md:","lg:","xl:","2xl:"],r=Array.isArray(e)?e:[e];return[0,0,0,0,0,0].map((a,t)=>`${o[t]}grid-cols-${r?.[t]||r?.[r?.length-1]}`).join(" ")},height(e){return e==="auto"?"auto":""},full_width(e){return e?"w-full grow":"grow-0"},equal_height(e){return e?"items-stretch":"unequal-height"},visible(e){return e?"":"!hidden"},item_container(e){return e?"":"!border-none"}},n=(e,o="")=>{let r=[],a={};if(o==="")a=e;else for(const t in e)if(t.startsWith(o+"_")){const l=t.substring(t.indexOf("_")+1);a[l]=e[t]}if(a.hasOwnProperty("margin")){Array.isArray(a.margin)||(a.margin=a.margin?[!0,!0,!0,!0]:[!1,!1,!1,!1]);let t=["t","r","b","l"];a.margin.forEach((l,s)=>{l||r.push(`!m${t[s]}-0`)})}if(a.hasOwnProperty("border")){Array.isArray(a.border)||(a.border=a.border?[!0,!0,!0,!0]:[!1,!1,!1,!1]);let t=["t","r","b","l"];a.border.forEach((l,s)=>{l||r.push(`!border-${t[s]}-0`)})}switch(a.rounded){case!0:r.push("!rounded-lg");break;case!1:r.push("!rounded-none");break}switch(a.full_width){case!0:r.push("w-full");break;case!1:r.push("!grow-0");break}switch(a.text_color){case"red":r.push("!text-red-500","dark:text-red-100");break;case"yellow":r.push("!text-yellow-500","dark:text-yellow-100");break;case"green":r.push("!text-green-500","dark:text-green-100");break;case"blue":r.push("!text-blue-500","dark:text-blue-100");break;case"purple":r.push("!text-purple-500","dark:text-purple-100");break;case"black":r.push("!text-gray-700","dark:text-gray-50");break}switch(a.bg_color){case"red":r.push("!bg-red-100 !from-red-100 !to-red-200 !border-red-300","dark:!bg-red-700 dark:!from-red-700 dark:!to-red-800 dark:!border-red-900");break;case"yellow":r.push("!bg-yellow-100 !from-yellow-100 !to-yellow-200 !border-yellow-300","dark:!bg-yellow-700 dark:!from-yellow-700 dark:!to-yellow-800 dark:!border-yellow-900");break;case"green":r.push("!bg-green-100 !from-green-100 !to-green-200 !border-green-300","dark:!bg-green-700 dark:!from-green-700 dark:!to-green-800 dark:!border-green-900  !text-gray-800");break;case"blue":r.push("!bg-blue-100 !from-blue-100 !to-blue-200 !border-blue-300","dark:!bg-blue-700 dark:!from-blue-700 dark:!to-blue-800 dark:!border-blue-900");break;case"purple":r.push("!bg-purple-100 !from-purple-100 !to-purple-200 !border-purple-300","dark:!bg-purple-700 dark:!from-purple-700 dark:!to-purple-800 dark:!border-purple-900");break;case"black":r.push("!bg-gray-100 !from-gray-100 !to-gray-200 !border-gray-300","dark:!bg-gray-700 dark:!from-gray-700 dark:!to-gray-800 dark:!border-gray-900");case"pink":r.push("!bg-pink-100 !from-pink-100 !to-pink-200 !border-pink-300","dark:!bg-pink-700 dark:!from-pink-700 dark:!to-pink-800 dark:!border-pink-900 !text-gray-800");break}return" "+r.join(" ")};export{n as c,b as g};
