"use strict";(self.webpackChunktracker=self.webpackChunktracker||[]).push([[232],{1688:function(t,e,n){var i=n(4991),u=n.n(i),r=n(6314),s=n.n(r)()(u());s.push([t.id,"","",{version:3,sources:[],names:[],mappings:"",sourceRoot:""}]),e.A=s},8557:function(t,e,n){n.r(e),n.d(e,{default:function(){return o}});var i=function(){var t=this,e=t._self._c;return e("div",{staticClass:"autocomplete"},[e("input",{directives:[{name:"model",rawName:"v-model",value:t.inputValue,expression:"inputValue"}],attrs:{id:"autocompletedIntput",type:"text",autocomplete:"off",placeholder:"задача@проект #тег, комментарий"},domProps:{value:t.inputValue},on:{keydown:this.onKeydown,input:[function(e){e.target.composing||(t.inputValue=e.target.value)},function(e){return t.$emit("input",e.target.value)}],focus:t.onFocus}}),t._v(" "),e("div",{staticClass:"autocomplete-items",attrs:{id:"myInputautocomplete-list"}},t._l(t.suggestions,(function(n,i){return t.showSuggestion?e("div",{key:i,class:t.currentFocus===i?"autocomplete-active":"",attrs:{"data-id":i},on:{click:function(e){return t.select(i)}}},[t._v("\n      "+t._s(n)+"\n      "),e("input",{attrs:{type:"hidden"},domProps:{value:n}})]):t._e()})),0)])};i._withStripped=!0,n(8598),n(9432),n(6099),n(7495),n(1761),n(5440),n(2762);var u={data:function(){return{showSuggestion:!1,input:document.getElementById("autocompletedIntput"),currentFocus:-1,inputValue:""}},props:{taskName:{type:String},suggestions:{type:Array}},methods:{onKeydown:function(t){if(this.showSuggestion=t.target===document.activeElement,40===t.keyCode)this.currentFocus++,this.currentFocus>=this.suggestions.length-1&&(this.currentFocus=this.suggestions.length-1);else if(38===t.keyCode)this.currentFocus--,this.currentFocus<-1&&(this.currentFocus=-1);else if(13===t.keyCode)this.currentFocus>-1&&(this.select(this.currentFocus),t.preventDefault());else if(9===t.keyCode)if(t.preventDefault(),event.shiftKey){this.inputValue=this.inputValue.trim();var e=this.inputValue[this.inputValue.length-1];","!==e||this.inputValue.match(/[#]/)?","===e&&this.inputValue.match(/[#]/)?(this.inputValue=this.inputValue.replace(/,$/,""),this.setInput(this.inputValue)):"#"!==e||this.inputValue.match(/[@]/)?"#"===e&&this.inputValue.match(/[@]/)?(this.inputValue=this.inputValue.replace(/#$/,""),this.setInput(this.inputValue)):"@"===e&&(this.inputValue=this.inputValue.replace(/@$/,""),this.setInput(this.inputValue)):(this.inputValue=this.inputValue.replace(/\s*#$/,"@"),this.setInput(this.inputValue)):(this.inputValue=this.inputValue.replace(/,$/," #"),this.setInput(this.inputValue))}else this.inputValue=this.inputValue.trim(),this.inputValue.match(/[@#,]/)?this.inputValue.match(/[#,]/)?this.inputValue.match(/,/)||("#"===this.inputValue[this.inputValue.length-1]?this.inputValue=this.inputValue.substr(0,this.inputValue.length-1).trim()+", ":this.inputValue+=", ",this.setInput(this.inputValue)):("@"===this.inputValue[this.inputValue.length-1]?this.inputValue=this.inputValue.substr(0,this.inputValue.length-1).trim()+" #":this.inputValue+=" #",this.setInput(this.inputValue)):(this.inputValue+="@",this.setInput(this.inputValue))},onFocus:function(){this.showSuggestion=!0},onClickOut:function(t){"autocompletedIntput"!==t.target.id&&(this.showSuggestion=!1)},select:function(t){this.setInput(this.suggestions[t]),this.currentFocus=-1},setInput:function(t){var e=t.replace(/\s+/g," ");this.inputValue=e,this.$emit("input",this.inputValue)},clear:function(){this.inputValue="",this.$emit("input",this.inputValue)},urlEncode:function(t){return Object.keys(t).reduce((function(e,n){return e.push(n+"="+encodeURIComponent(t[n])),e}),[]).join("&")}},mounted:function(){document.addEventListener("click",this.onClickOut)}},r=n(5072),s=n.n(r),a=n(1688),o=(s()(a.A,{insert:"head",singleton:!1}),a.A.locals,(0,n(4486).A)(u,i,[],!1,null,null,null).exports)},8232:function(t,e,n){n.r(e),n.d(e,{default:function(){return l}});var i=function(){var t=this,e=t._self._c;return e("div",[e("form",{staticClass:"md-layout md-gutter md-alignment-top-center center",attrs:{action:"",method:"post"},on:{submit:function(e){return e.preventDefault(),t.addTask()}}},[e("md-card",{staticClass:"md-layout-item md-large-size-50 md-xlarge-size-50 md-medium-size-70 md-small-size-100"},[e("md-card-content",[e("div",{staticClass:"md-layout"},[e("div",{staticClass:"md-layout-item md-size-80"},[e("Autocomplete",{ref:"autocomplete",attrs:{suggestions:t.filteredSuggestion},on:{input:function(e){return t.getCompletitions()}},model:{value:t.taskName,callback:function(e){t.taskName=e},expression:"taskName"}})],1),t._v(" "),e("div",{staticClass:"md-layout-item md-size-20"},[e("md-button",{staticClass:"md-primary",staticStyle:{"margin-top":"18px"},attrs:{type:"submit"}},[t._v("добавить")])],1)])])],1)],1),t._v(" "),e("md-dialog-alert",{attrs:{"md-active":t.showAlert,"md-content":t.alertMessage,"md-confirm-text":"Ок"},on:{"update:mdActive":function(e){t.showAlert=e},"update:md-active":function(e){t.showAlert=e}}})],1)};i._withStripped=!0,n(2675),n(9463),n(2259),n(3418),n(3792),n(4782),n(2010),n(6099),n(4864),n(7495),n(8781),n(7764),n(1761),n(5440),n(2762),n(2953);var u=n(8557),r=n(2866);function s(t,e){var n="undefined"!=typeof Symbol&&t[Symbol.iterator]||t["@@iterator"];if(!n){if(Array.isArray(t)||(n=function(t,e){if(t){if("string"==typeof t)return a(t,e);var n=Object.prototype.toString.call(t).slice(8,-1);return"Object"===n&&t.constructor&&(n=t.constructor.name),"Map"===n||"Set"===n?Array.from(t):"Arguments"===n||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(n)?a(t,e):void 0}}(t))||e&&t&&"number"==typeof t.length){n&&(t=n);var i=0,u=function(){};return{s:u,n:function(){return i>=t.length?{done:!0}:{done:!1,value:t[i++]}},e:function(t){throw t},f:u}}throw new TypeError("Invalid attempt to iterate non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}var r,s=!0,o=!1;return{s:function(){n=n.call(t)},n:function(){var t=n.next();return s=t.done,t},e:function(t){o=!0,r=t},f:function(){try{s||null==n.return||n.return()}finally{if(o)throw r}}}}function a(t,e){(null==e||e>t.length)&&(e=t.length);for(var n=0,i=new Array(e);n<e;n++)i[n]=t[n];return i}var o={data:function(){return{taskName:"",taskCompletitions:[],showSuggestion:!1,showAlert:!1,alertMessage:""}},props:{tags:{type:Array},projects:{type:Array}},components:{Autocomplete:u.default},computed:{filteredSuggestion:function(){var t,e,n,i=[],u=this.taskName.toLowerCase();if(/[@#,]/.test(u)){if(/@/.test(u)&&!/[#,]/.test(u)){e=u.replace(/^(.*@).*$/,"$1"),n=u.replace(/^.*@(.*)$/,"$1"),t=new RegExp(n,"i");var r,a=s(this.projects);try{for(a.s();!(r=a.n()).done;){var o=r.value;if(t.test(o)&&o!==n&&i.push(e+o),i.length>=10)break}}catch(t){a.e(t)}finally{a.f()}}else if(/#/.test(u)&&!/[,]/.test(u)){e=u.replace(/^(.*#).*$/,"$1"),n=u.replace(/^.*#(.*)$/,"$1"),t=new RegExp(n,"i");var l,c=s(this.tags);try{for(c.s();!(l=c.n()).done;){var p=l.value;if(t.test(p)&&p!==n&&i.push(e+p),i.length>=10)break}}catch(t){c.e(t)}finally{c.f()}}}else{var h=this.getTimeDelta(u,"",0),f=u.replace(h,"").trim().replace(/[[\]{}()*+?.,\\^$|#\s]/g,"\\$&");t=new RegExp(f,"i");var m,d=s(this.taskCompletitions);try{for(d.s();!(m=d.n()).done;){var g=m.value;if(t.test(g)&&g!==f&&(h.length>0?i.push(h+" "+g):i.push(g)),i.length>=10)break}}catch(t){d.e(t)}finally{d.f()}}return i}},methods:{getCompletitions:function(){var t=this,e=this.taskName.toLowerCase(),n=this.getTimeDelta(e,"",0),i=e.replace(n,"").trim();r.n.getCompletitions(i).then((function(e){t.taskCompletitions=e.data.values})).catch((function(t){console.log(["getCompletitions error",t])}))},addTask:function(){var t=this;r.n.addTask(this.taskName).then((function(e){e.data.status?(t.taskName="",t.$emit("add-task"),t.$refs.autocomplete.clear()):"message"in e.data&&t.alert(e.data.message)})).catch((function(t){console.log(["addTask error",t])}))},getTimeDelta:function(t,e,n){var i="",u=[new RegExp(/^-[0-9]{0,3}/),new RegExp(/^([0-1]?[0-9]|[2][0-3]):([0-5][0-9])/),new RegExp(/^([0-1]?[0-9]|[2][0-3]):([0-5][0-9])-([0-1]?[0-9]|[2][0-3]):([0-5][0-9])/)];if(0===n&&t.match(u[2]))return t.match(u[2])[0];if(t.match(u[0])?i=t.match(u[0])[0]:t.match(u[1])&&(i=t.match(u[1])[0]),""!==i&&0===n)return this.getTimeDelta(t.replace(i,"").trim(),i,1);if(""!==e&&""!==i)i=e+" "+i;else if(""!==e&&""===i)return e;return i},onFocus:function(){this.showSuggestion=!0},alert:function(t){this.alertMessage=t,this.showAlert=!0}},mounted:function(){this.getCompletitions()}},l=(0,n(4486).A)(o,i,[],!1,null,null,null).exports},7916:function(t,e,n){var i=n(6080),u=n(9565),r=n(8981),s=n(6319),a=n(4209),o=n(3517),l=n(6198),c=n(4659),p=n(81),h=n(851),f=Array;t.exports=function(t){var e=r(t),n=o(this),m=arguments.length,d=m>1?arguments[1]:void 0,g=void 0!==d;g&&(d=i(d,m>2?arguments[2]:void 0));var v,y,V,w,k,x,C=h(e),A=0;if(!C||this===f&&a(C))for(v=l(e),y=n?new this(v):f(v);v>A;A++)x=g?d(e[A],A):e[A],c(y,A,x);else for(k=(w=p(e,C)).next,y=n?new this:[];!(V=u(k,w)).done;A++)x=g?s(w,d,[V.value,A],!0):V.value,c(y,A,x);return y.length=A,y}},6319:function(t,e,n){var i=n(8551),u=n(9539);t.exports=function(t,e,n,r){try{return r?e(i(n)[0],n[1]):e(n)}catch(e){u(t,"throw",e)}}},788:function(t,e,n){var i=n(34),u=n(4576),r=n(8227)("match");t.exports=function(t){var e;return i(t)&&(void 0!==(e=t[r])?!!e:"RegExp"===u(t))}},1056:function(t,e,n){var i=n(4913).f;t.exports=function(t,e,n){n in t||i(t,n,{configurable:!0,get:function(){return e[n]},set:function(t){e[n]=t}})}},1034:function(t,e,n){var i=n(9565),u=n(9297),r=n(1625),s=n(7979),a=RegExp.prototype;t.exports=function(t){var e=t.flags;return void 0!==e||"flags"in a||u(t,"flags")||!r(a,t)?e:i(s,t)}},706:function(t,e,n){var i=n(350).PROPER,u=n(9039),r=n(7452);t.exports=function(t){return u((function(){return!!r[t]()||"​᠎"!=="​᠎"[t]()||i&&r[t].name!==t}))}},3418:function(t,e,n){var i=n(6518),u=n(7916);i({target:"Array",stat:!0,forced:!n(4428)((function(t){Array.from(t)}))},{from:u})},4864:function(t,e,n){var i=n(3724),u=n(4475),r=n(9504),s=n(2796),a=n(3167),o=n(6699),l=n(2360),c=n(8480).f,p=n(1625),h=n(788),f=n(655),m=n(1034),d=n(8429),g=n(1056),v=n(6840),y=n(9039),V=n(9297),w=n(1181).enforce,k=n(7633),x=n(8227),C=n(3635),A=n(8814),b=x("match"),S=u.RegExp,I=S.prototype,E=u.SyntaxError,R=r(I.exec),$=r("".charAt),_=r("".replace),F=r("".indexOf),N=r("".slice),T=/^\?<[^\s\d!#%&*+<=>@^][^\s!#%&*+<=>@^]*>/,D=/a/g,O=/a/g,P=new S(D)!==D,j=d.MISSED_STICKY,z=d.UNSUPPORTED_Y;if(s("RegExp",i&&(!P||j||C||A||y((function(){return O[b]=!1,S(D)!==D||S(O)===O||"/a/i"!==String(S(D,"i"))}))))){for(var M=function(t,e){var n,i,u,r,s,c,d=p(I,this),g=h(t),v=void 0===e,y=[],k=t;if(!d&&g&&v&&t.constructor===M)return t;if((g||p(I,t))&&(t=t.source,v&&(e=m(k))),t=void 0===t?"":f(t),e=void 0===e?"":f(e),k=t,C&&"dotAll"in D&&(i=!!e&&F(e,"s")>-1)&&(e=_(e,/s/g,"")),n=e,j&&"sticky"in D&&(u=!!e&&F(e,"y")>-1)&&z&&(e=_(e,/y/g,"")),A&&(r=function(t){for(var e,n=t.length,i=0,u="",r=[],s=l(null),a=!1,o=!1,c=0,p="";i<=n;i++){if("\\"===(e=$(t,i)))e+=$(t,++i);else if("]"===e)a=!1;else if(!a)switch(!0){case"["===e:a=!0;break;case"("===e:R(T,N(t,i+1))&&(i+=2,o=!0),u+=e,c++;continue;case">"===e&&o:if(""===p||V(s,p))throw new E("Invalid capture group name");s[p]=!0,r[r.length]=[p,c],o=!1,p="";continue}o?p+=e:u+=e}return[u,r]}(t),t=r[0],y=r[1]),s=a(S(t,e),d?this:I,M),(i||u||y.length)&&(c=w(s),i&&(c.dotAll=!0,c.raw=M(function(t){for(var e,n=t.length,i=0,u="",r=!1;i<=n;i++)"\\"!==(e=$(t,i))?r||"."!==e?("["===e?r=!0:"]"===e&&(r=!1),u+=e):u+="[\\s\\S]":u+=e+$(t,++i);return u}(t),n)),u&&(c.sticky=!0),y.length&&(c.groups=y)),t!==k)try{o(s,"source",""===k?"(?:)":k)}catch(t){}return s},K=c(S),U=0;K.length>U;)g(M,S,K[U++]);I.constructor=M,M.prototype=I,v(u,"RegExp",M,{constructor:!0})}k("RegExp")},8781:function(t,e,n){var i=n(350).PROPER,u=n(6840),r=n(8551),s=n(655),a=n(9039),o=n(1034),l="toString",c=RegExp.prototype,p=c[l],h=a((function(){return"/a/b"!==p.call({source:"a",flags:"b"})})),f=i&&p.name!==l;(h||f)&&u(c,l,(function(){var t=r(this);return"/"+s(t.source)+"/"+s(o(t))}),{unsafe:!0})},1761:function(t,e,n){var i=n(9565),u=n(9228),r=n(8551),s=n(4117),a=n(8014),o=n(655),l=n(7750),c=n(5966),p=n(7829),h=n(6682);u("match",(function(t,e,n){return[function(e){var n=l(this),u=s(e)?void 0:c(e,t);return u?i(u,e,n):new RegExp(e)[t](o(n))},function(t){var i=r(this),u=o(t),s=n(e,i,u);if(s.done)return s.value;if(!i.global)return h(i,u);var l=i.unicode;i.lastIndex=0;for(var c,f=[],m=0;null!==(c=h(i,u));){var d=o(c[0]);f[m]=d,""===d&&(i.lastIndex=p(u,a(i.lastIndex),l)),m++}return 0===m?null:f}]}))},2762:function(t,e,n){var i=n(6518),u=n(3802).trim;i({target:"String",proto:!0,forced:n(706)("trim")},{trim:function(){return u(this)}})},2259:function(t,e,n){n(511)("iterator")}}]);