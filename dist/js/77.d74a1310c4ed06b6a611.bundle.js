"use strict";(self.webpackChunktracker=self.webpackChunktracker||[]).push([[77,417],{2866:function(t,e,n){n.d(e,{n:function(){return c}});var r=n(2284),a=(n(2675),n(9463),n(2010),n(6099),n(3362),n(2505)),o=n.n(a),i=n(14),u=n(1347),s=o().create({baseURL:"https://time.skillum.ru",headers:{"Content-type":"application/x-www-form-urlencoded"}});s.interceptors.response.use((function(t){return"object"===(0,r.A)(t.data)&&null!==t.data&&"token"in t.data&&(localStorage.setItem("token",t.data.token),delete t.data.token),t}),(function(t){return void 0!==t.response&&"status"in t.response&&401===t.response.status&&(0,i.W5)()&&((0,i.ri)(),location.reload()),Promise.reject(t)})),s.interceptors.request.use((function(t){return t.headers.token=(0,i.gf)(),t}));var c={auth:function(t,e,n){var r={login:t,password:e,action:n};return s.post("/api/auth",(0,u.u4)(r))},getTasks:function(t,e){var n=(0,u.Yq)(t),r=new Date(e.getTime());r.setDate(e.getDate()+1);var a="/api/tasks?interval="+n+"-"+(0,u.Yq)(r);return s.get(a)},getGroupedTasks:function(t,e){var n="/api/grouped_tasks?interval="+(0,u.Yq)(t)+"-"+(0,u.Yq)(e);return s.get(n)},getCurrentTask:function(){return s.get("/api/current")},getCompletitions:function(t){return t?s.get("/api/completitions?text="+t):s.get("/api/completitions")},getTrackers:function(){return s.get("/api/trackers")},getProjects:function(t){return s.get("/api/projects",{params:{projects:t}})},getUserProjects:function(){return s.get("/api/user_projects")},getUserTags:function(){return s.get("/api/user_tags")},getTrackerProjects:function(t){return s.get("/api/trackerProjects",{params:{id:t}})},getEvoUsers:function(){return s.get("/api/evoUsers")},addTask:function(t){return s.post("/api/task",(0,u.u4)({name:t}))},getToken:function(t,e,n){return s.post("/api/getToken",(0,u.u4)({id:t,login:e,password:n}))},getSettings:function(){return s.get("/api/settings")},saveSettings:function(t){return s.post("/api/settings",(0,u.u4)(t))},stopTask:function(t){return s.post("/api/task/stop",(0,u.u4)({id:t}))},resumeTask:function(t){return s.post("/api/task/resume",(0,u.u4)({id:t}))},updateTask:function(t){return s.post("/api/task/edit",(0,u.u4)({id:t.id,name:t.name,category:t.category,date:t.date,start_time:t.start_time,end_time:t.end_time,description:t.description,tags:t.tags}))},deleteTask:function(t){return s.post("/api/task/delete",(0,u.u4)({id:t}))},saveTracker:function(t){return s.post("/api/tracker",(0,u.u4)({id:t.id,title:t.title,type:t.type,api_url:t.api_url}))},linkProject:function(t,e,n){return s.post("/api/linkProject",(0,u.u4)({projectId:t,trackerId:e,trackerProjectId:null!==n?n.value:0,trackerProjectTitle:null!==n?n.label:0}))},saveEvoUser:function(t){return s.post("/api/evoUser",(0,u.u4)({id:t.value}))},deleteTracker:function(t){return s.post("/api/tracker/delete",(0,u.u4)({id:t.id}))},getTrackerTask:function(t,e){return s.get("/api/trackerTask",{params:{trackerId:t,taskId:e}})},getVersion:function(t){return s.get("/api/version?version="+t)},exportTask:function(t){return s.post("/api/task/export",(0,u.u4)(t))}};e.A=c},14:function(t,e,n){function r(){var t=localStorage.getItem("token");return null!==t&&""!==t}function a(){localStorage.removeItem("token")}function o(){return localStorage.getItem("token")}n.d(e,{W5:function(){return r},gf:function(){return o},ri:function(){return a}})},1347:function(t,e,n){function r(t){return Object.keys(t).reduce((function(e,n){return e.push(n+"="+encodeURIComponent(t[n])),e}),[]).join("&")}function a(t,e){if(null===t||""===t)return[];var n=[],r=t.split(" "),a=" ";return r.forEach((function(t,o){if(a.length>0){var i=a+" "+t;if(!(i.length>e))return o===r.length-1?void n.push(i):void(a=i);n.push(a),a=""}o!==r.length-1&&t.length<e?a=t:n.push(t)})),n}function o(t,e){return("0"+t.getDate()).slice(-2)+"."+("0"+(t.getMonth()+1)).slice(-2)+(void 0===e?"."+t.getFullYear():"")}function i(t){var e=Math.floor(t),n=Math.floor(60*(t-e));return n<10&&(n="0"+n),e+":"+n}n.d(e,{Yq:function(){return o},ad:function(){return i},u4:function(){return r},wR:function(){return a}}),n(8598),n(4782),n(9432),n(6099),n(3500)},2738:function(t,e,n){var r=n(4991),a=n.n(r),o=n(6314),i=n.n(o)()(a());i.push([t.id,"","",{version:3,sources:[],names:[],mappings:"",sourceRoot:""}]),e.A=i},7798:function(t,e,n){n.r(e),n.d(e,{default:function(){return u}});var r=function(){var t=this,e=t._self._c;return e("transition",{attrs:{name:"modal"}},[e("div",{directives:[{name:"show",rawName:"v-show",value:t.show,expression:"show"}],staticClass:"modal-mask"},[e("div",{staticClass:"modal-container"},[t._t("default")],2)])])};r._withStripped=!0;var a=n(5072),o=n.n(a),i=n(2738),u=(o()(i.A,{insert:"head",singleton:!1}),i.A.locals,(0,n(4486).A)({template:"#new-post-modal-template",props:["show"],data:function(){return{title:"",body:""}},methods:{close:function(){this.$emit("close"),this.title="",this.body=""},savePost:function(){this.close()}}},r,[],!1,null,null,null).exports)},7829:function(t,e,n){var r=n(8183).charAt;t.exports=function(t,e,n){return e+(n?r(t,e).length:1)}},9228:function(t,e,n){n(7495);var r=n(9565),a=n(6840),o=n(7323),i=n(9039),u=n(8227),s=n(6699),c=u("species"),l=RegExp.prototype;t.exports=function(t,e,n,p){var f=u(t),d=!i((function(){var e={};return e[f]=function(){return 7},7!==""[t](e)})),g=d&&!i((function(){var e=!1,n=/a/;return"split"===t&&((n={}).constructor={},n.constructor[c]=function(){return n},n.flags="",n[f]=/./[f]),n.exec=function(){return e=!0,null},n[f](""),!e}));if(!d||!g||n){var v=/./[f],x=e(f,""[t],(function(t,e,n,a,i){var u=e.exec;return u===o||u===l.exec?d&&!i?{done:!0,value:r(v,e,n,a)}:{done:!0,value:r(t,n,e,a)}:{done:!1}}));a(String.prototype,t,x[0]),a(l,f,x[1])}p&&s(l[f],"sham",!0)}},2478:function(t,e,n){var r=n(9504),a=n(8981),o=Math.floor,i=r("".charAt),u=r("".replace),s=r("".slice),c=/\$([$&'`]|\d{1,2}|<[^>]*>)/g,l=/\$([$&'`]|\d{1,2})/g;t.exports=function(t,e,n,r,p,f){var d=n+t.length,g=r.length,v=l;return void 0!==p&&(p=a(p),v=c),u(f,v,(function(a,u){var c;switch(i(u,0)){case"$":return"$";case"&":return t;case"`":return s(e,0,n);case"'":return s(e,d);case"<":c=p[s(u,1,-1)];break;default:var l=+u;if(0===l)return a;if(l>g){var f=o(l/10);return 0===f?a:f<=g?void 0===r[f-1]?i(u,1):r[f-1]+i(u,1):a}c=r[l-1]}return void 0===c?"":c}))}},6682:function(t,e,n){var r=n(9565),a=n(8551),o=n(4901),i=n(4576),u=n(7323),s=TypeError;t.exports=function(t,e){var n=t.exec;if(o(n)){var c=r(n,t,e);return null!==c&&a(c),c}if("RegExp"===i(t))return r(u,t,e);throw new s("RegExp#exec called on incompatible receiver")}},7323:function(t,e,n){var r,a,o=n(9565),i=n(9504),u=n(655),s=n(7979),c=n(8429),l=n(5745),p=n(2360),f=n(1181).get,d=n(3635),g=n(8814),v=l("native-string-replace",String.prototype.replace),x=RegExp.prototype.exec,h=x,k=i("".charAt),m=i("".indexOf),I=i("".replace),T=i("".slice),w=(a=/b*/g,o(x,r=/a/,"a"),o(x,a,"a"),0!==r.lastIndex||0!==a.lastIndex),y=c.BROKEN_CARET,b=void 0!==/()??/.exec("")[1];(w||b||y||d||g)&&(h=function(t){var e,n,r,a,i,c,l,d=this,g=f(d),E=u(t),R=g.raw;if(R)return R.lastIndex=d.lastIndex,e=o(h,R,E),d.lastIndex=R.lastIndex,e;var _=g.groups,j=y&&d.sticky,$=o(s,d),S=d.source,A=0,C=E;if(j&&($=I($,"y",""),-1===m($,"g")&&($+="g"),C=T(E,d.lastIndex),d.lastIndex>0&&(!d.multiline||d.multiline&&"\n"!==k(E,d.lastIndex-1))&&(S="(?: "+S+")",C=" "+C,A++),n=new RegExp("^(?:"+S+")",$)),b&&(n=new RegExp("^"+S+"$(?!\\s)",$)),w&&(r=d.lastIndex),a=o(x,j?n:d,C),j?a?(a.input=T(a.input,A),a[0]=T(a[0],A),a.index=d.lastIndex,d.lastIndex+=a[0].length):d.lastIndex=0:w&&a&&(d.lastIndex=d.global?a.index+a[0].length:r),b&&a&&a.length>1&&o(v,a[0],n,(function(){for(i=1;i<arguments.length-2;i++)void 0===arguments[i]&&(a[i]=void 0)})),a&&_)for(a.groups=c=p(null),i=0;i<_.length;i++)c[(l=_[i])[0]]=a[l[1]];return a}),t.exports=h},7979:function(t,e,n){var r=n(8551);t.exports=function(){var t=r(this),e="";return t.hasIndices&&(e+="d"),t.global&&(e+="g"),t.ignoreCase&&(e+="i"),t.multiline&&(e+="m"),t.dotAll&&(e+="s"),t.unicode&&(e+="u"),t.unicodeSets&&(e+="v"),t.sticky&&(e+="y"),e}},8429:function(t,e,n){var r=n(9039),a=n(4475).RegExp,o=r((function(){var t=a("a","y");return t.lastIndex=2,null!==t.exec("abcd")})),i=o||r((function(){return!a("a","y").sticky})),u=o||r((function(){var t=a("^r","gy");return t.lastIndex=2,null!==t.exec("str")}));t.exports={BROKEN_CARET:u,MISSED_STICKY:i,UNSUPPORTED_Y:o}},3635:function(t,e,n){var r=n(9039),a=n(4475).RegExp;t.exports=r((function(){var t=a(".","s");return!(t.dotAll&&t.test("\n")&&"s"===t.flags)}))},8814:function(t,e,n){var r=n(9039),a=n(4475).RegExp;t.exports=r((function(){var t=a("(?<a>b)","g");return"b"!==t.exec("b").groups.a||"bc"!=="b".replace(t,"$<a>c")}))},7495:function(t,e,n){var r=n(6518),a=n(7323);r({target:"RegExp",proto:!0,forced:/./.exec!==a},{exec:a})},5440:function(t,e,n){var r=n(8745),a=n(9565),o=n(9504),i=n(9228),u=n(9039),s=n(8551),c=n(4901),l=n(4117),p=n(1291),f=n(8014),d=n(655),g=n(7750),v=n(7829),x=n(5966),h=n(2478),k=n(6682),m=n(8227)("replace"),I=Math.max,T=Math.min,w=o([].concat),y=o([].push),b=o("".indexOf),E=o("".slice),R="$0"==="a".replace(/./,"$0"),_=!!/./[m]&&""===/./[m]("a","$0");i("replace",(function(t,e,n){var o=_?"$":"$0";return[function(t,n){var r=g(this),o=l(t)?void 0:x(t,m);return o?a(o,t,r,n):a(e,d(r),t,n)},function(t,a){var i=s(this),u=d(t);if("string"==typeof a&&-1===b(a,o)&&-1===b(a,"$<")){var l=n(e,i,u,a);if(l.done)return l.value}var g=c(a);g||(a=d(a));var x,m=i.global;m&&(x=i.unicode,i.lastIndex=0);for(var R,_=[];null!==(R=k(i,u))&&(y(_,R),m);)""===d(R[0])&&(i.lastIndex=v(u,f(i.lastIndex),x));for(var j,$="",S=0,A=0;A<_.length;A++){for(var C,P=d((R=_[A])[0]),U=I(T(p(R.index),u.length),0),Y=[],M=1;M<R.length;M++)y(Y,void 0===(j=R[M])?j:String(j));var q=R.groups;if(g){var D=w([P],Y,U,u);void 0!==q&&y(D,q),C=d(r(a,void 0,D))}else C=h(P,u,U,Y,q,a);U>=S&&($+=E(u,S,U)+C,S=U+P.length)}return $+E(u,S)}]}),!!u((function(){var t=/./;return t.exec=function(){var t=[];return t.groups={a:"7"},t},"7"!=="".replace(t,"$<a>")}))||!R||_)}}]);