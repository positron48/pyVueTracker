"use strict";(self.webpackChunktracker=self.webpackChunktracker||[]).push([[107],{2866:function(t,e,n){n.d(e,{n:function(){return s}});var r=n(2284),a=(n(2675),n(9463),n(2010),n(6099),n(3362),n(2505)),o=n.n(a),u=n(14),i=n(1347),c=o().create({baseURL:"https://time.retailcrm.tech",headers:{"Content-type":"application/x-www-form-urlencoded"}});c.interceptors.response.use((function(t){return"object"===(0,r.A)(t.data)&&null!==t.data&&"token"in t.data&&(localStorage.setItem("token",t.data.token),delete t.data.token),t}),(function(t){return void 0!==t.response&&"status"in t.response&&401===t.response.status&&(0,u.W5)()&&((0,u.ri)(),location.reload()),Promise.reject(t)})),c.interceptors.request.use((function(t){return t.headers.token=(0,u.gf)(),t}));var s={auth:function(t,e,n){var r={login:t,password:e,action:n};return c.post("/api/auth",(0,i.u4)(r))},getTasks:function(t,e){var n=(0,i.Yq)(t),r=new Date(e.getTime());r.setDate(e.getDate()+1);var a="/api/tasks?interval="+n+"-"+(0,i.Yq)(r);return c.get(a)},getGroupedTasks:function(t,e){var n="/api/grouped_tasks?interval="+(0,i.Yq)(t)+"-"+(0,i.Yq)(e);return c.get(n)},getCurrentTask:function(){return c.get("/api/current")},getCompletitions:function(t){return t?c.get("/api/completitions?text="+t):c.get("/api/completitions")},getTrackers:function(){return c.get("/api/trackers")},getProjects:function(t){return c.get("/api/projects",{params:{projects:t}})},getUserProjects:function(){return c.get("/api/user_projects")},getUserTags:function(){return c.get("/api/user_tags")},getTrackerProjects:function(t){return c.get("/api/trackerProjects",{params:{id:t}})},getEvoUsers:function(){return c.get("/api/evoUsers")},addTask:function(t){return c.post("/api/task",(0,i.u4)({name:t}))},getToken:function(t,e,n){return c.post("/api/getToken",(0,i.u4)({id:t,login:e,password:n}))},getSettings:function(){return c.get("/api/settings")},saveSettings:function(t){return c.post("/api/settings",(0,i.u4)(t))},stopTask:function(t){return c.post("/api/task/stop",(0,i.u4)({id:t}))},resumeTask:function(t){return c.post("/api/task/resume",(0,i.u4)({id:t}))},updateTask:function(t){return c.post("/api/task/edit",(0,i.u4)({id:t.id,name:t.name,category:t.category,date:t.date,start_time:t.start_time,end_time:t.end_time,description:t.description,tags:t.tags}))},deleteTask:function(t){return c.post("/api/task/delete",(0,i.u4)({id:t}))},saveTracker:function(t){return c.post("/api/tracker",(0,i.u4)({id:t.id,title:t.title,type:t.type,api_url:t.api_url}))},linkProject:function(t,e,n){return c.post("/api/linkProject",(0,i.u4)({projectId:t,trackerId:e,trackerProjectId:null!==n?n.value:0,trackerProjectTitle:null!==n?n.label:0}))},saveEvoUser:function(t){return c.post("/api/evoUser",(0,i.u4)({id:t.value}))},deleteTracker:function(t){return c.post("/api/tracker/delete",(0,i.u4)({id:t.id}))},getTrackerTask:function(t,e){return c.get("/api/trackerTask",{params:{trackerId:t,taskId:e}})},getVersion:function(t){return c.get("/api/version?version="+t)},exportTask:function(t){return c.post("/api/task/export",(0,i.u4)(t))}};e.A=s},14:function(t,e,n){function r(){var t=localStorage.getItem("token");return null!==t&&""!==t}function a(){localStorage.removeItem("token")}function o(){return localStorage.getItem("token")}n.d(e,{W5:function(){return r},gf:function(){return o},ri:function(){return a}})},1347:function(t,e,n){function r(t){return Object.keys(t).reduce((function(e,n){return e.push(n+"="+encodeURIComponent(t[n])),e}),[]).join("&")}function a(t,e){if(null===t||""===t)return[];var n=[],r=t.split(" "),a=" ";return r.forEach((function(t,o){if(a.length>0){var u=a+" "+t;if(!(u.length>e))return o===r.length-1?void n.push(u):void(a=u);n.push(a),a=""}o!==r.length-1&&t.length<e?a=t:n.push(t)})),n}function o(t,e){return("0"+t.getDate()).slice(-2)+"."+("0"+(t.getMonth()+1)).slice(-2)+(void 0===e?"."+t.getFullYear():"")}function u(t){var e=Math.floor(t),n=Math.floor(60*(t-e));return n<10&&(n="0"+n),e+":"+n}n.d(e,{Yq:function(){return o},ad:function(){return u},u4:function(){return r},wR:function(){return a}}),n(8598),n(4782),n(9432),n(6099),n(3500)},7829:function(t,e,n){var r=n(8183).charAt;t.exports=function(t,e,n){return e+(n?r(t,e).length:1)}},9228:function(t,e,n){n(7495);var r=n(9565),a=n(6840),o=n(7323),u=n(9039),i=n(8227),c=n(6699),s=i("species"),l=RegExp.prototype;t.exports=function(t,e,n,p){var f=i(t),g=!u((function(){var e={};return e[f]=function(){return 7},7!==""[t](e)})),d=g&&!u((function(){var e=!1,n=/a/;return"split"===t&&((n={}).constructor={},n.constructor[s]=function(){return n},n.flags="",n[f]=/./[f]),n.exec=function(){return e=!0,null},n[f](""),!e}));if(!g||!d||n){var v=/./[f],x=e(f,""[t],(function(t,e,n,a,u){var i=e.exec;return i===o||i===l.exec?g&&!u?{done:!0,value:r(v,e,n,a)}:{done:!0,value:r(t,n,e,a)}:{done:!1}}));a(String.prototype,t,x[0]),a(l,f,x[1])}p&&c(l[f],"sham",!0)}},2478:function(t,e,n){var r=n(9504),a=n(8981),o=Math.floor,u=r("".charAt),i=r("".replace),c=r("".slice),s=/\$([$&'`]|\d{1,2}|<[^>]*>)/g,l=/\$([$&'`]|\d{1,2})/g;t.exports=function(t,e,n,r,p,f){var g=n+t.length,d=r.length,v=l;return void 0!==p&&(p=a(p),v=s),i(f,v,(function(a,i){var s;switch(u(i,0)){case"$":return"$";case"&":return t;case"`":return c(e,0,n);case"'":return c(e,g);case"<":s=p[c(i,1,-1)];break;default:var l=+i;if(0===l)return a;if(l>d){var f=o(l/10);return 0===f?a:f<=d?void 0===r[f-1]?u(i,1):r[f-1]+u(i,1):a}s=r[l-1]}return void 0===s?"":s}))}},3167:function(t,e,n){var r=n(4901),a=n(34),o=n(2967);t.exports=function(t,e,n){var u,i;return o&&r(u=e.constructor)&&u!==n&&a(i=u.prototype)&&i!==n.prototype&&o(t,i),t}},6682:function(t,e,n){var r=n(9565),a=n(8551),o=n(4901),u=n(4576),i=n(7323),c=TypeError;t.exports=function(t,e){var n=t.exec;if(o(n)){var s=r(n,t,e);return null!==s&&a(s),s}if("RegExp"===u(t))return r(i,t,e);throw new c("RegExp#exec called on incompatible receiver")}},7323:function(t,e,n){var r,a,o=n(9565),u=n(9504),i=n(655),c=n(7979),s=n(8429),l=n(5745),p=n(2360),f=n(1181).get,g=n(3635),d=n(8814),v=l("native-string-replace",String.prototype.replace),x=RegExp.prototype.exec,k=x,h=u("".charAt),m=u("".indexOf),I=u("".replace),T=u("".slice),y=(a=/b*/g,o(x,r=/a/,"a"),o(x,a,"a"),0!==r.lastIndex||0!==a.lastIndex),E=s.BROKEN_CARET,R=void 0!==/()??/.exec("")[1];(y||R||E||g||d)&&(k=function(t){var e,n,r,a,u,s,l,g=this,d=f(g),b=i(t),$=d.raw;if($)return $.lastIndex=g.lastIndex,e=o(k,$,b),g.lastIndex=$.lastIndex,e;var j=d.groups,w=E&&g.sticky,S=o(c,g),_=g.source,P=0,C=b;if(w&&(S=I(S,"y",""),-1===m(S,"g")&&(S+="g"),C=T(b,g.lastIndex),g.lastIndex>0&&(!g.multiline||g.multiline&&"\n"!==h(b,g.lastIndex-1))&&(_="(?: "+_+")",C=" "+C,P++),n=new RegExp("^(?:"+_+")",S)),R&&(n=new RegExp("^"+_+"$(?!\\s)",S)),y&&(r=g.lastIndex),a=o(x,w?n:g,C),w?a?(a.input=T(a.input,P),a[0]=T(a[0],P),a.index=g.lastIndex,g.lastIndex+=a[0].length):g.lastIndex=0:y&&a&&(g.lastIndex=g.global?a.index+a[0].length:r),R&&a&&a.length>1&&o(v,a[0],n,(function(){for(u=1;u<arguments.length-2;u++)void 0===arguments[u]&&(a[u]=void 0)})),a&&j)for(a.groups=s=p(null),u=0;u<j.length;u++)s[(l=j[u])[0]]=a[l[1]];return a}),t.exports=k},7979:function(t,e,n){var r=n(8551);t.exports=function(){var t=r(this),e="";return t.hasIndices&&(e+="d"),t.global&&(e+="g"),t.ignoreCase&&(e+="i"),t.multiline&&(e+="m"),t.dotAll&&(e+="s"),t.unicode&&(e+="u"),t.unicodeSets&&(e+="v"),t.sticky&&(e+="y"),e}},8429:function(t,e,n){var r=n(9039),a=n(4475).RegExp,o=r((function(){var t=a("a","y");return t.lastIndex=2,null!==t.exec("abcd")})),u=o||r((function(){return!a("a","y").sticky})),i=o||r((function(){var t=a("^r","gy");return t.lastIndex=2,null!==t.exec("str")}));t.exports={BROKEN_CARET:i,MISSED_STICKY:u,UNSUPPORTED_Y:o}},3635:function(t,e,n){var r=n(9039),a=n(4475).RegExp;t.exports=r((function(){var t=a(".","s");return!(t.dotAll&&t.test("\n")&&"s"===t.flags)}))},8814:function(t,e,n){var r=n(9039),a=n(4475).RegExp;t.exports=r((function(){var t=a("(?<a>b)","g");return"b"!==t.exec("b").groups.a||"bc"!=="b".replace(t,"$<a>c")}))},3802:function(t,e,n){var r=n(9504),a=n(7750),o=n(655),u=n(7452),i=r("".replace),c=RegExp("^["+u+"]+"),s=RegExp("(^|[^"+u+"])["+u+"]+$"),l=function(t){return function(e){var n=o(a(e));return 1&t&&(n=i(n,c,"")),2&t&&(n=i(n,s,"$1")),n}};t.exports={start:l(1),end:l(2),trim:l(3)}},7452:function(t){t.exports="\t\n\v\f\r                　\u2028\u2029\ufeff"},7495:function(t,e,n){var r=n(6518),a=n(7323);r({target:"RegExp",proto:!0,forced:/./.exec!==a},{exec:a})},5440:function(t,e,n){var r=n(8745),a=n(9565),o=n(9504),u=n(9228),i=n(9039),c=n(8551),s=n(4901),l=n(4117),p=n(1291),f=n(8014),g=n(655),d=n(7750),v=n(7829),x=n(5966),k=n(2478),h=n(6682),m=n(8227)("replace"),I=Math.max,T=Math.min,y=o([].concat),E=o([].push),R=o("".indexOf),b=o("".slice),$="$0"==="a".replace(/./,"$0"),j=!!/./[m]&&""===/./[m]("a","$0");u("replace",(function(t,e,n){var o=j?"$":"$0";return[function(t,n){var r=d(this),o=l(t)?void 0:x(t,m);return o?a(o,t,r,n):a(e,g(r),t,n)},function(t,a){var u=c(this),i=g(t);if("string"==typeof a&&-1===R(a,o)&&-1===R(a,"$<")){var l=n(e,u,i,a);if(l.done)return l.value}var d=s(a);d||(a=g(a));var x,m=u.global;m&&(x=u.unicode,u.lastIndex=0);for(var $,j=[];null!==($=h(u,i))&&(E(j,$),m);)""===g($[0])&&(u.lastIndex=v(i,f(u.lastIndex),x));for(var w,S="",_=0,P=0;P<j.length;P++){for(var C,U=g(($=j[P])[0]),A=I(T(p($.index),i.length),0),Y=[],M=1;M<$.length;M++)E(Y,void 0===(w=$[M])?w:String(w));var q=$.groups;if(d){var D=y([U],Y,A,i);void 0!==q&&E(D,q),C=g(r(a,void 0,D))}else C=k(U,i,A,Y,q,a);A>=_&&(S+=b(i,_,A)+C,_=A+U.length)}return S+b(i,_)}]}),!!i((function(){var t=/./;return t.exec=function(){var t=[];return t.groups={a:"7"},t},"7"!=="".replace(t,"$<a>")}))||!$||j)}}]);