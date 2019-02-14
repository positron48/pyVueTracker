webpackJsonp([4],{"b/ba":function(e,t){},niH5:function(e,t,r){"use strict";Object.defineProperty(t,"__esModule",{value:!0});var a=r("VTQS"),o={data:function(){return{trackers:[],evoUsers:[],evoUser:"",projects:null,loginToken:"",passwordToken:"",currentTracker:{id:0,title:"",api_url:"",type:"redmine"},showTracker:!1,showUser:!1,showToken:!1}},methods:{getTrackers:function(){var e=this;a.b.getTrackers().then(function(t){e.trackers=t.data.trackers}).catch(function(e){console.log(["getTasks error",e])})},getEvoUsers:function(){var e=this;a.b.getEvoUsers().then(function(t){e.evoUsers=t.data.users}).catch(function(e){console.log(["getEvoUsers error",e])})},showTrackerModal:function(){this.showTracker=!0},closeTrackerModal:function(){this.showTracker=!1},deleteTracker:function(e){var t=this;confirm("вы действительно хотите удалить трекер из списка?")&&a.b.deleteTracker(this.currentTracker).then(function(e){t.getTrackers(),t.showTracker=!1}).catch(function(e){console.log(["getToken error",e])})},saveTracker:function(){var e=this;a.b.saveTracker(this.currentTracker).then(function(t){e.getTrackers(),e.showTracker=!1}).catch(function(e){console.log(["getToken error",e])})},saveEvoUser:function(){var e=this;a.b.saveEvoUser(this.evoUser).then(function(t){e.getTrackers(),e.showUser=!1}).catch(function(e){console.log(["saveTrackerUser error",e])})},addTracker:function(){this.currentTracker={id:0,title:"",api_url:"",type:"redmine"},this.showTrackerModal()},editTracker:function(e){this.currentTracker=e,this.showTrackerModal()},showTokenModal:function(e){this.loginToken="",this.passwordToken="",this.currentTracker=e,this.showToken=!0},showUserModal:function(e){"evo"===e.type&&(this.currentTracker=e,this.showUser=!0)},closeTokenModal:function(){this.showToken=!1},closeUserModal:function(){this.showUser=!1},getToken:function(){var e=this;a.b.getToken(this.currentTracker.id,this.loginToken,this.passwordToken).then(function(t){void 0!==t.data.external_token&&""!==t.data.external_token?(e.getTrackers(),"evo"===e.currentTracker.type&&e.getEvoUsers(),e.showToken=!1):alert("Токен не получен")}).catch(function(e){console.log(["getToken error",e])})}},components:{Modal:r("/o5o").default},mounted:function(){this.getTrackers(),this.getEvoUsers()}},n={render:function(){var e=this,t=e.$createElement,r=e._self._c||t;return r("div",[r("div",{staticClass:"md-layout md-gutter md-alignment-top-center center"},[r("div",{staticClass:"md-layout-item md-size-80"},[r("md-list",[r("md-list-item",[e._v("\n          Трекеры\n        ")]),e._v(" "),r("md-table",[r("md-table-row",[r("md-table-head"),e._v(" "),r("md-table-head",[e._v("Название")]),e._v(" "),r("md-table-head",[e._v("Url")]),e._v(" "),r("md-table-head",[e._v("Тип")]),e._v(" "),r("md-table-head",[e._v("Токен")]),e._v(" "),r("md-table-head",[e._v("Пользователь")])],1),e._v(" "),e._l(e.trackers,function(t){return r("md-table-row",{key:t.id},[r("md-table-head",[r("div",{staticClass:"edit-icon",on:{click:function(r){e.editTracker(t)}}},[r("font-awesome-icon",{attrs:{icon:"edit"}}),e._v(" "),r("md-tooltip",{attrs:{"md-direction":"top"}},[e._v("Редактировать")])],1)]),e._v(" "),r("md-table-head",[e._v(e._s(t.title))]),e._v(" "),r("md-table-head",[e._v(e._s(t.api_url))]),e._v(" "),r("md-table-head",[e._v(e._s(t.type))]),e._v(" "),r("md-table-head",[r("a",{staticClass:"simple-link",on:{click:function(r){e.showTokenModal(t)}}},[r("md-tooltip",{attrs:{"md-direction":"top"}},[e._v("Авторизация на трекере")]),e._v(" "),t.external_api_key?r("span",[e._v(e._s(t.external_api_key))]):e._e(),e._v(" "),t.external_api_key?e._e():r("span",[e._v("Получить токен")])],1)]),e._v(" "),r("md-table-head",[t.external_api_key&&"evo"===t.type?r("a",{staticClass:"simple-link",on:{click:function(r){e.showUserModal(t)}}},[t.external_user_id||"evo"!==t.type?e._e():r("span",[e._v("Указать пользователя")]),e._v(" "),t.external_user_id?r("span",[e._v(e._s(t.external_user_id))]):e._e()]):e._e(),e._v(" "),t.external_user_id&&"redmine"===t.type?r("span",[e._v(e._s(t.external_user_id))]):e._e()])],1)})],2),e._v(" "),r("md-list-item",[r("md-button",{on:{click:function(t){e.addTracker()}}},[e._v("Добавить redmine")])],1)],1)],1),e._v(" "),r("br"),r("br"),e._v(" "),e.projects?r("div",{staticClass:"md-layout-item md-size-80"},[r("md-list",[r("md-list-item",[e._v("\n          Проекты\n        ")]),e._v(" "),r("md-table",[r("md-table-row",[r("md-table-head"),e._v(" "),r("md-table-head",[e._v("Название")]),e._v(" "),r("md-table-head",[e._v("Url")]),e._v(" "),r("md-table-head",[e._v("Тип")]),e._v(" "),r("md-table-head",[e._v("Токен")])],1),e._v(" "),e._l(e.projects,function(t){return r("md-table-row",{key:t.id},[r("md-table-head",[r("div",{on:{click:function(r){e.editProject(t.id)}}},[r("font-awesome-icon",{attrs:{icon:"edit"}})],1)]),e._v(" "),r("md-table-head",[e._v(e._s(t.title))]),e._v(" "),r("md-table-head",[e._v(e._s(t.api_url))]),e._v(" "),r("md-table-head",[e._v(e._s(t.type))]),e._v(" "),r("md-table-head",[e._v(e._s(t.external_api_key))])],1)})],2),e._v(" "),r("md-list-item",[r("md-button",[e._v("Добавить")])],1)],1)],1):e._e()]),e._v(" "),r("modal",{attrs:{show:e.showTracker},on:{close:e.closeTrackerModal}},[r("div",{staticClass:"modal-header"}),e._v(" "),r("div",{staticClass:"modal-body"},[r("input",{directives:[{name:"model",rawName:"v-model",value:e.currentTracker.id,expression:"currentTracker.id"}],attrs:{type:"hidden",name:"id"},domProps:{value:e.currentTracker.id},on:{input:function(t){t.target.composing||e.$set(e.currentTracker,"id",t.target.value)}}}),e._v(" "),r("input",{directives:[{name:"model",rawName:"v-model",value:e.currentTracker.type,expression:"currentTracker.type"}],attrs:{type:"hidden",name:"type"},domProps:{value:e.currentTracker.type},on:{input:function(t){t.target.composing||e.$set(e.currentTracker,"type",t.target.value)}}}),e._v(" "),r("md-field",[r("label",[e._v("Название")]),e._v(" "),r("md-input",{model:{value:e.currentTracker.title,callback:function(t){e.$set(e.currentTracker,"title",t)},expression:"currentTracker.title"}})],1),e._v(" "),r("md-field",[r("label",[e._v("Url")]),e._v(" "),r("md-input",{model:{value:e.currentTracker.api_url,callback:function(t){e.$set(e.currentTracker,"api_url",t)},expression:"currentTracker.api_url"}})],1)],1),e._v(" "),r("div",{staticClass:"modal-footer text-right"},[r("md-button",{staticClass:"md-primary",on:{click:e.deleteTracker}},[e._v("удалить")]),e._v(" "),r("md-button",{staticClass:"md-primary",on:{click:e.closeTrackerModal}},[e._v("отмена")]),e._v(" "),r("md-button",{staticClass:"md-accent",on:{click:e.saveTracker}},[e._v("сохранить")])],1)]),e._v(" "),r("modal",{attrs:{show:e.showToken},on:{close:e.closeTokenModal}},[r("div",{staticClass:"modal-header"},[r("h2",[e._v("Данные для авторизации в "+e._s(e.currentTracker.title))])]),e._v(" "),r("div",{staticClass:"modal-body"},[r("input",{directives:[{name:"model",rawName:"v-model",value:e.currentTracker.id,expression:"currentTracker.id"}],attrs:{type:"hidden",name:"id"},domProps:{value:e.currentTracker.id},on:{input:function(t){t.target.composing||e.$set(e.currentTracker,"id",t.target.value)}}}),e._v(" "),r("input",{directives:[{name:"model",rawName:"v-model",value:e.currentTracker.type,expression:"currentTracker.type"}],attrs:{type:"hidden",name:"type"},domProps:{value:e.currentTracker.type},on:{input:function(t){t.target.composing||e.$set(e.currentTracker,"type",t.target.value)}}}),e._v(" "),r("md-field",[r("label",[e._v("Логин")]),e._v(" "),r("md-input",{model:{value:e.loginToken,callback:function(t){e.loginToken=t},expression:"loginToken"}})],1),e._v(" "),r("md-field",[r("label",[e._v("Пароль")]),e._v(" "),r("md-input",{attrs:{type:"password"},model:{value:e.passwordToken,callback:function(t){e.passwordToken=t},expression:"passwordToken"}})],1)],1),e._v(" "),r("div",{staticClass:"modal-footer text-right"},[r("md-button",{staticClass:"md-primary",on:{click:e.closeTokenModal}},[e._v("отмена")]),e._v(" "),r("md-button",{staticClass:"md-accent",on:{click:e.getToken}},[e._v("получить")])],1)]),e._v(" "),r("modal",{attrs:{show:e.showUser}},[r("div",{staticClass:"modal-header"},[r("h2",[e._v("Выберите пользователя в "+e._s(e.currentTracker.title))])]),e._v(" "),r("div",{staticClass:"modal-body"},[r("input",{directives:[{name:"model",rawName:"v-model",value:e.currentTracker.id,expression:"currentTracker.id"}],attrs:{type:"hidden",name:"id"},domProps:{value:e.currentTracker.id},on:{input:function(t){t.target.composing||e.$set(e.currentTracker,"id",t.target.value)}}}),e._v(" "),r("v-select",{attrs:{options:e.evoUsers},model:{value:e.evoUser,callback:function(t){e.evoUser=t},expression:"evoUser"}})],1),e._v(" "),r("div",{staticClass:"modal-footer text-right"},[r("md-button",{staticClass:"md-primary",on:{click:e.closeUserModal}},[e._v("отмена")]),e._v(" "),r("md-button",{staticClass:"md-accent",on:{click:e.saveEvoUser}},[e._v("сохранить")])],1)])],1)},staticRenderFns:[]};var s=r("VU/8")(o,n,!1,function(e){r("b/ba")},"data-v-47cec2d4",null);t.default=s.exports}});
//# sourceMappingURL=4.3ce71784eb66170adee6.js.map