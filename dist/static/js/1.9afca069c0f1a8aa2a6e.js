webpackJsonp([1,2,3,4,5,6,7,8],{"41YW":function(e,t){},"9YsO":function(e,t,n){"use strict";Object.defineProperty(t,"__esModule",{value:!0});var s={render:function(){this.$createElement;this._self._c;return this._m(0)},staticRenderFns:[function(){var e=this,t=e.$createElement,n=e._self._c||t;return n("div",[n("div",{staticClass:"md-layout md-gutter md-alignment-top-center"},[n("div",{staticClass:"md-layout-item md-large-size-80 md-xlarge-size-80 md-medium-size-90 md-small-size-100"},[n("h2",[e._v("Добавление задач")]),e._v(" "),n("p",[e._v("\n      При добавлении задачи можно (и нужно) сразу указать название задачи и проект, если задача заведена в редмайне,\n      то первым пишется ее номер.\n      ")]),e._v(" "),n("p",[e._v("\n      Синтаксис поля ввода задачи следующий: "),n("br"),e._v(" "),n("i",[e._v("[время выполнения] [номер задачи в редмайн] краткое описания задачи [@проект][#тег][, комментарий]")])]),e._v(" "),n("p",[e._v("\n      Детальнее по полям:\n      "),n("ul",[n("li",[n("b",[e._v("время выполнения")]),e._v(" - указывается время выполнения задачи, в различных форматах:"),n("br"),e._v(" "),n("b",[n("i",[e._v("-10")])]),e._v(" работа над задачей началась 10 минут назад"),n("br"),e._v(" "),n("b",[n("i",[e._v("11:50")])]),e._v(" работа над задачей началась в 11:50"),n("br"),e._v(" "),n("b",[n("i",[e._v("11:50-12:20")])]),e._v(" работа над задачей началась в 11:50 и завершилась в 12:20\n        ")]),e._v(" "),n("li",[n("b",[e._v("номер задачи в редмайн")]),e._v(" - нужно указывать, если нужно выгружать часы по этой задаче в редмайн\n        ")]),e._v(" "),n("li",[n("b",[e._v("краткое описания задачи")]),e._v(" - краткое описание, чтобы не забыть о чем задача\n        ")]),e._v(" "),n("li",[n("b",[e._v("[@проект]")]),e._v(" - название проекта, в рамках которого делается задача. Может быть произвольным, при экспорте\n           можно будет сопоставить с трекерами вручную, если название не совпадает с названием на трекере."),n("br"),e._v('\n           Если не указать проект, будет автоматически проставлен "untitled" (без названия)\n        ')]),e._v(" "),n("li",[n("b",[e._v("#тег")]),e._v(" - поле использвется только в статистике, помечая задачи тем или иным тегом можно будет увидеть,\n           сколько по времени занимала та или иная дестельность, например, #разработка #инкубатор #обучение.\n           Тегов может быть несколько\n        ")]),e._v(" "),n("li",[n("b",[e._v(", комментарий")]),e._v(" - комментарий, описывающий конкретную часть задачи, над которой идет работа\n           в настоящее время. Будет выгружен в комментарий редмайна и evo соответственно."),n("br"),e._v("\n           Обязателен, если задача отсутствует в редмайне, но можно указать на этапе экспорта\n        ")])])]),e._v(" "),n("p",[e._v("\n        Таким образом, корректные примеры указания задач могут выглядеть слудеющим образом:"),n("br"),e._v(" "),n("ul",[n("li",[e._v("55123 таймтрекер@инкубатор #разработка, написание руководства пользователя")]),e._v(" "),n("li",[e._v("-30 поддержка столплит@столплит #поддержка, прогрузка данных по заказам из 1с")]),e._v(" "),n("li",[e._v("11:20-12:50 митап@развитие интаро")]),e._v(" "),n("li",[e._v("заполню потом")])])]),e._v(" "),n("p",[e._v('\n        Пользуясь клавишей Tab можно подставлять в строку символы "@/#/,", переключая таким образом вводимое поле.\n        Shift+Tab переключает символы в обратном порядке\n      ')]),e._v(" "),n("br"),n("br"),e._v(" "),n("h2",[e._v("Интерфейс")]),e._v(" "),n("p",[e._v("Основной интерфейс выглядит следующим образом:")]),e._v(" "),n("img",{staticClass:"center",attrs:{src:"/static/screen_main_top.png"}}),e._v(" "),n("img",{staticClass:"center",attrs:{src:"/static/screen_main_bottom.png"}}),e._v(" "),n("p",[e._v("\n      По блокам сверху вниз:\n      "),n("ul",[n("li",[e._v("текущая задача")]),e._v(" "),n("li",[e._v("поле ввода новой задачи")]),e._v(" "),n("li",[e._v("\n          график распределения задач по часам. По оси Х сутки, разбитые по часам, по оси Y количество времени,\n          затраченное в конкретный час. Например 16 это время с 16:00 до 17:00, потрачено полчаса\n        ")]),e._v(" "),n("li",[e._v("список задач за текущий день")]),e._v(" "),n("li",[e._v("диаграмма распределения часов по задачам")]),e._v(" "),n("li",[e._v("диаграмма распределения часов по проектам")]),e._v(" "),n("li",[e._v("диаграмма распределения часов по тегам")])])]),e._v(" "),n("br"),n("br"),e._v(" "),n("h2",[e._v("Настройки")]),e._v(" "),n("p",[e._v("Для работы выгрузки часов в внешние трекеры вам нужно авторизоваться на этих трекерах.")]),e._v(" "),n("p",[e._v('\n        Чтобы авторизоваться, перейдите в меню "Настройки", нажмите на ссылку "Получить токен", введите свой логин и\n        пароль от соответствующего трекера и кликните по кнопке "Сохранить". В итоге в табличке отобразится ваш токен.\n      ')]),e._v(" "),n("p",[e._v('\n        Для evo требуется также указать сотрудника, которому будут проставляться выгружаемые часы.\n        Нужно кликнуть на ссылку "Указать пользователя" и выбрать себя из списка.\n      ')]),e._v(" "),n("img",{staticClass:"center",attrs:{src:"/static/screen_settings.png"}}),e._v(" "),n("p",[e._v("На этой же странице можно добавить еще один трекер, если для вашей работы необходимо проставлять часы в нескольких")]),e._v(" "),n("p",{staticStyle:{"font-color":"gray"}},[e._v("\n        *логин и пароль используются исключительно для получения токена авторизации и не хранятся на сервере.\n      ")]),e._v(" "),n("br"),n("br"),e._v(" "),n("h2",[e._v("Экспорт задач")]),e._v(" "),n("p",[e._v("Для выгрузки задач нужно перейти в раздел экспорт, где отобразятся сгруппированные задачи за день.")]),n("p"),n("p",[e._v("У всех элементов интерфейса, которые требуют пояснения, при наведении появляется подсказка.")]),e._v(" "),n("p",[e._v("\n      У каждой задачи в крайнем правом столбце есть список трекеров, привязанных к задаче.\n      Цвет отражает статус трекера:\n      "),n("ul",[n("li",[e._v("\n          синий - задача готова к выгрузке на указанный трекер, при наведении отображается название проекта на трекере\n        ")]),e._v(" "),n("li",[e._v("\n          серый - не найдено соответствие проекта, нужно указать вручную, если нужно выгрузить часы на этот трекер\n           (указывается 1 раз для проекта)\n         ")]),e._v(" "),n("li",[e._v("\n          красный - задача сопоставлена, но по какой-то причине не может быть выгружена\n          (не получен токен авторизации в настройках, не указан номер задачи для редмайн, задача с таким номером\n          не существует или для ее просмотра недостаточно прав)\n         ")]),e._v(" "),n("li",[e._v("\n          желтый - задача готова к выгрузке на указанный трекер, но по ней есть предупреждение (проект задачи не\n          совпадает с сопоставленным, так бывает, когда в редмайне один проект разбит на несколько, а в эво один)\n        ")]),e._v(" "),n("li",[e._v("\n          зеленый - задача успешно выгружена на трекер\n        ")]),e._v(" "),n("li",[e._v("\n          черный - при выгрузке на трекер произошла ошибка\n        ")])])]),e._v(" "),n("p",[e._v("\n        Непосредственно на этапе экспорта можно отредактировать все данные по задачам\n        (дату, номер задачи, комментарий, часы), такие изменения повлияют только на выгрузку часов и нигде не будут учтены.\n      ")]),e._v(" "),n("p",[e._v("\n        Галочкой можно отметить, нужно ли выгружать задачу на тот или иной трекер.\n      ")]),e._v(" "),n("img",{staticClass:"center",attrs:{src:"/static/screen_export.png"}})])])])}]};var a=n("VU/8")({data:function(){return{}}},s,!1,function(e){n("41YW")},null,null);t.default=a.exports},D2Oq:function(e,t){},"J+R/":function(e,t,n){"use strict";Object.defineProperty(t,"__esModule",{value:!0});var s=n("VTQS"),a=n("WdI8"),r={data:function(){return{login:"",password:"",isLogin:!1,showAlert:!1,alertMessage:""}},computed:{},methods:{auth:function(){var e=this;s.b.auth(this.login,this.password,"login").then(function(t){void 0!==t.data.message?e.alert(t.data.message):(e.isLogin=Object(a.b)(),e.$emit("login"))}).catch(function(e){console.log(["auth error",e])})},onKeyDown:function(e){13===e.keyCode&&this.auth()},alert:function(e){this.alertMessage=e,this.showAlert=!0}},mounted:function(){this.isLogin=Object(a.b)()}},i={render:function(){var e=this,t=e.$createElement,n=e._self._c||t;return n("div",[n("md-card",{staticClass:"md-layout-item md-size-20",staticStyle:{margin:"auto"}},[n("md-card-content",[n("md-field",[n("label",[e._v("Логин")]),e._v(" "),n("md-input",{attrs:{type:"text",required:""},nativeOn:{keydown:function(t){return e.onKeyDown(t)}},model:{value:e.login,callback:function(t){e.login="string"==typeof t?t.trim():t},expression:"login"}}),e._v(" "),n("md-tooltip",{attrs:{"md-direction":"right"}},[e._v("Логин redmine")])],1),e._v(" "),n("md-field",[n("label",[e._v("Пароль")]),e._v(" "),n("md-input",{attrs:{type:"password",required:""},nativeOn:{keydown:function(t){return e.onKeyDown(t)}},model:{value:e.password,callback:function(t){e.password="string"==typeof t?t.trim():t},expression:"password"}}),e._v(" "),n("md-tooltip",{attrs:{"md-direction":"right"}},[e._v("Пароль redmine")])],1),e._v(" "),n("div",{staticClass:"auth-buttons"},[n("md-button",{on:{click:function(t){e.auth()}}},[e._v("Войти")])],1)],1)],1),e._v(" "),n("md-dialog-alert",{attrs:{"md-active":e.showAlert,"md-content":e.alertMessage,"md-confirm-text":"Ок"},on:{"update:mdActive":function(t){e.showAlert=t}}})],1)},staticRenderFns:[]};var o=n("VU/8")(r,i,!1,function(e){n("D2Oq")},null,null);t.default=o.exports},YcJa:function(e,t,n){"use strict";Object.defineProperty(t,"__esModule",{value:!0});var s={render:function(){var e=this.$createElement,t=this._self._c||e;return t("div",[t("md-empty-state",{attrs:{"md-label":"404 - Страница не найдена","md-description":""}})],1)},staticRenderFns:[]},a=n("VU/8")(null,s,!1,null,null,null);t.default=a.exports},"ZBq/":function(e,t){},iWMn:function(e,t){},lO7g:function(e,t,n){"use strict";Object.defineProperty(t,"__esModule",{value:!0});var s=n("N1EC"),a=n("KYvs"),r=n("Ty68"),i=n("VTQS"),o={data:function(){return{timer:null,userProjects:[],userTags:[]}},methods:{refreshData:function(){this.$refs.taskStop.getCurrentTask(),this.$refs.taskAdd.getCompletitions(),this.$refs.tasks.refreshDate(),this.$refs.tasks.getTasks()},onStopTask:function(){this.refreshData(),this.getUserProjects(),this.getUserTags()},onAddTask:function(){this.refreshData(),this.getUserProjects(),this.getUserTags()},onEditTask:function(){this.refreshData(),this.getUserProjects(),this.getUserTags()},getUserProjects:function(){var e=this;i.a.getUserProjects().then(function(t){e.userProjects=t.data.projects}).catch(function(e){console.log(["getUserProjects error",e])})},getUserTags:function(){var e=this;i.a.getUserTags().then(function(t){e.userTags=t.data.tags}).catch(function(e){console.log(["getUserTags error",e])})}},components:{Tasks:s.default,TaskAdd:a.default,TaskStop:r.default},mounted:function(){this.timer=setInterval(this.refreshData,6e4),this.getUserProjects(),this.getUserTags()},destroyed:function(){clearInterval(this.timer)}},c={render:function(){var e=this,t=e.$createElement,n=e._self._c||t;return n("div",[e._m(0),e._v(" "),n("TaskStop",{ref:"taskStop",on:{"stop-task":e.onStopTask}}),e._v(" "),n("TaskAdd",{ref:"taskAdd",attrs:{projects:e.userProjects,tags:e.userTags},on:{"add-task":e.onAddTask}}),e._v(" "),n("Tasks",{ref:"tasks",on:{update:function(t){e.onEditTask()}}})],1)},staticRenderFns:[function(){var e=this.$createElement,t=this._self._c||e;return t("div",{staticClass:"md-layout md-gutter md-alignment-top-center"},[t("div",{staticClass:"md-layout-item md-large-size-50 md-xlarge-size-50 md-medium-size-70 md-small-size-100"})])}]},l=n("VU/8")(o,c,!1,null,null,null);t.default=l.exports},niH5:function(e,t,n){"use strict";Object.defineProperty(t,"__esModule",{value:!0});var s=n("VTQS"),a={data:function(){return{trackers:[],evoUsers:[],evoUser:"",projects:null,loginToken:"",passwordToken:"",currentTracker:{id:0,title:"",api_url:"",type:"redmine"},showTracker:!1,showUser:!1,showToken:!1,showAlert:!1,alertMessage:"",userSettings:{evo_in_name:"#redmine_name",evo_in_comment:"##redmine_id",evo_out_name:"#comments",evo_out_comment:""}}},methods:{getTrackers:function(){var e=this;s.b.getTrackers().then(function(t){e.trackers=t.data.trackers}).catch(function(e){console.log(["getTasks error",e])})},getEvoUsers:function(){var e=this;s.b.getEvoUsers().then(function(t){e.evoUsers=t.data.users}).catch(function(e){console.log(["getEvoUsers error",e])})},showTrackerModal:function(){this.showTracker=!0},closeTrackerModal:function(){this.showTracker=!1},deleteTracker:function(e){var t=this;confirm("вы действительно хотите удалить трекер из списка?")&&s.b.deleteTracker(this.currentTracker).then(function(e){t.getTrackers(),t.showTracker=!1}).catch(function(e){console.log(["getToken error",e])})},saveTracker:function(){var e=this;s.b.saveTracker(this.currentTracker).then(function(t){e.getTrackers(),e.showTracker=!1}).catch(function(e){console.log(["getToken error",e])})},saveEvoUser:function(){var e=this;s.b.saveEvoUser(this.evoUser).then(function(t){e.getTrackers(),e.showUser=!1}).catch(function(e){console.log(["saveTrackerUser error",e])})},addTracker:function(){this.currentTracker={id:0,title:"",api_url:"",type:"redmine"},this.showTrackerModal()},editTracker:function(e){this.currentTracker=e,this.showTrackerModal()},getSettings:function(){var e=this;s.b.getSettings().then(function(t){for(var n in t.data.data)e.userSettings[n]=t.data.data[n]}).catch(function(e){console.log(["getSettings error",e])})},saveSettings:function(){var e=this;if(""===this.userSettings.evo_in_name.trim()||""===this.userSettings.evo_out_name.trim())return this.alert('<span style="color: red;">Формулировка обязательна!</span>'),!1;s.b.saveSettings(this.userSettings).then(function(t){e.alert("Изменения сохранены!")}).catch(function(t){console.log(["saveSettings error",t]),e.alert("Ошибка:"+t)})},restoreSettings:function(){this.userSettings={evo_in_name:"#redmine_name",evo_in_comment:"##redmine_id",evo_out_name:"#comments",evo_out_comment:""}},showTokenModal:function(e){this.loginToken="",this.passwordToken="",this.currentTracker=e,this.showToken=!0},showUserModal:function(e){"evo"===e.type&&(this.currentTracker=e,this.showUser=!0)},closeTokenModal:function(){this.showToken=!1},closeUserModal:function(){this.showUser=!1},getToken:function(){var e=this;s.b.getToken(this.currentTracker.id,this.loginToken,this.passwordToken).then(function(t){void 0!==t.data.external_token&&null!==t.data.external_token?(e.getTrackers(),"evo"===e.currentTracker.type&&e.getEvoUsers(),e.showToken=!1):e.alert("Токен не получен")}).catch(function(e){console.log(["getToken error",e])})},alert:function(e){this.alertMessage=e,this.showAlert=!0}},components:{Modal:n("/o5o").default},mounted:function(){this.getTrackers(),this.getEvoUsers(),this.getSettings()}},r={render:function(){var e=this,t=e.$createElement,n=e._self._c||t;return n("div",[n("div",{staticClass:"md-layout md-gutter md-alignment-top-center center"},[n("div",{staticClass:"md-layout-item md-size-80"},[n("md-list",[n("md-list-item",[n("h3",[e._v("Трекеры")])]),e._v(" "),n("md-table",[n("md-table-row",[n("md-table-head"),e._v(" "),n("md-table-head",[e._v("Название")]),e._v(" "),n("md-table-head",[e._v("Url")]),e._v(" "),n("md-table-head",[e._v("Тип")]),e._v(" "),n("md-table-head",[e._v("Токен")]),e._v(" "),n("md-table-head",[e._v("Пользователь")])],1),e._v(" "),e._l(e.trackers,function(t){return n("md-table-row",{key:t.id},[n("md-table-head",[n("div",{staticClass:"edit-icon",on:{click:function(n){e.editTracker(t)}}},[n("font-awesome-icon",{attrs:{icon:"edit"}}),e._v(" "),n("md-tooltip",{attrs:{"md-direction":"top"}},[e._v("Редактировать")])],1)]),e._v(" "),n("md-table-head",[e._v(e._s(t.title))]),e._v(" "),n("md-table-head",[e._v(e._s(t.api_url))]),e._v(" "),n("md-table-head",[e._v(e._s(t.type))]),e._v(" "),n("md-table-head",[n("a",{staticClass:"simple-link",on:{click:function(n){e.showTokenModal(t)}}},[n("md-tooltip",{attrs:{"md-direction":"top"}},[e._v("Авторизация на трекере")]),e._v(" "),t.external_api_key?n("span",[e._v(e._s(t.external_api_key))]):e._e(),e._v(" "),t.external_api_key?e._e():n("span",[e._v("Получить токен")])],1)]),e._v(" "),n("md-table-head",[t.external_api_key&&"evo"===t.type?n("a",{staticClass:"simple-link",on:{click:function(n){e.showUserModal(t)}}},[t.external_user_id||"evo"!==t.type?e._e():n("span",[e._v("Указать пользователя")]),e._v(" "),t.external_user_id?n("span",[e._v(e._s(t.external_user_id))]):e._e()]):e._e(),e._v(" "),t.external_user_id&&"redmine"===t.type?n("span",[e._v(e._s(t.external_user_id))]):e._e()])],1)})],2),e._v(" "),n("md-list-item",[n("md-button",{on:{click:function(t){e.addTracker()}}},[e._v("Добавить redmine")])],1)],1)],1),e._v(" "),n("br"),n("br"),e._v(" "),e.projects?n("div",{staticClass:"md-layout-item md-size-80"},[n("md-list",[n("md-list-item",[e._v("\n          Проекты\n        ")]),e._v(" "),n("md-table",[n("md-table-row",[n("md-table-head"),e._v(" "),n("md-table-head",[e._v("Название")]),e._v(" "),n("md-table-head",[e._v("Url")]),e._v(" "),n("md-table-head",[e._v("Тип")]),e._v(" "),n("md-table-head",[e._v("Токен")])],1),e._v(" "),e._l(e.projects,function(t){return n("md-table-row",{key:t.id},[n("md-table-head",[n("div",{on:{click:function(n){e.editProject(t.id)}}},[n("font-awesome-icon",{attrs:{icon:"edit"}})],1)]),e._v(" "),n("md-table-head",[e._v(e._s(t.title))]),e._v(" "),n("md-table-head",[e._v(e._s(t.api_url))]),e._v(" "),n("md-table-head",[e._v(e._s(t.type))]),e._v(" "),n("md-table-head",[e._v(e._s(t.external_api_key))])],1)})],2),e._v(" "),n("md-list-item",[n("md-button",[e._v("Добавить")])],1)],1)],1):e._e()]),e._v(" "),n("br"),e._v(" "),n("div",{staticClass:"md-layout md-gutter md-alignment-top-center center"},[n("div",{staticClass:"md-layout-item md-size-80"},[n("md-list",[n("md-list-item",[n("h3",[e._v("Формат выгрузки часов в evolution")])]),e._v(" "),n("md-list-item",[n("b",[e._v("Есть задача в redmine")]),e._v(" "),n("md-field",[n("label",[e._v("формулировка")]),e._v(" "),n("md-input",{attrs:{required:""},model:{value:e.userSettings.evo_in_name,callback:function(t){e.$set(e.userSettings,"evo_in_name",t)},expression:"userSettings.evo_in_name"}})],1),e._v(" "),n("md-field",[n("label",[e._v("комментарий")]),e._v(" "),n("md-input",{model:{value:e.userSettings.evo_in_comment,callback:function(t){e.$set(e.userSettings,"evo_in_comment",t)},expression:"userSettings.evo_in_comment"}})],1)],1),e._v(" "),n("md-list-item",[n("b",[e._v("Нет задачи в redmine")]),e._v(" "),n("md-field",[n("label",[e._v("формулировка")]),e._v(" "),n("md-input",{attrs:{required:""},model:{value:e.userSettings.evo_out_name,callback:function(t){e.$set(e.userSettings,"evo_out_name",t)},expression:"userSettings.evo_out_name"}})],1),e._v(" "),n("md-field",[n("label",[e._v("комментарий")]),e._v(" "),n("md-input",{model:{value:e.userSettings.evo_out_comment,callback:function(t){e.$set(e.userSettings,"evo_out_comment",t)},expression:"userSettings.evo_out_comment"}})],1)],1),e._v(" "),n("md-list-item",[n("b",[e._v("Допустимые подстановки:")]),n("br"),e._v(" "),n("br"),n("i",[e._v("#redmine_name")]),e._v(" - название задачи из редмайн\n          "),n("br"),n("i",[e._v("#redmine_id")]),e._v(" - номер задачи из редмайн\n          "),n("br"),n("i",[e._v("#name")]),e._v(" - название задачи из трекера\n          "),n("br"),n("i",[e._v("#comments")]),e._v(" - комментарии к задаче из трекера\n        ")]),e._v(" "),n("md-list-item",[n("md-button",{staticClass:"md-accent",on:{click:function(t){e.saveSettings()}}},[e._v("Сохранить")]),e._v(" "),n("md-button",{on:{click:function(t){e.restoreSettings()}}},[e._v("По умолчанию")])],1)],1)],1)]),e._v(" "),n("modal",{attrs:{show:e.showTracker},on:{close:e.closeTrackerModal}},[n("div",{staticClass:"modal-header"}),e._v(" "),n("div",{staticClass:"modal-body"},[n("input",{directives:[{name:"model",rawName:"v-model",value:e.currentTracker.id,expression:"currentTracker.id"}],attrs:{type:"hidden",name:"id"},domProps:{value:e.currentTracker.id},on:{input:function(t){t.target.composing||e.$set(e.currentTracker,"id",t.target.value)}}}),e._v(" "),n("input",{directives:[{name:"model",rawName:"v-model",value:e.currentTracker.type,expression:"currentTracker.type"}],attrs:{type:"hidden",name:"type"},domProps:{value:e.currentTracker.type},on:{input:function(t){t.target.composing||e.$set(e.currentTracker,"type",t.target.value)}}}),e._v(" "),n("md-field",[n("label",[e._v("Название")]),e._v(" "),n("md-input",{model:{value:e.currentTracker.title,callback:function(t){e.$set(e.currentTracker,"title",t)},expression:"currentTracker.title"}})],1),e._v(" "),n("md-field",[n("label",[e._v("Url")]),e._v(" "),n("md-input",{model:{value:e.currentTracker.api_url,callback:function(t){e.$set(e.currentTracker,"api_url",t)},expression:"currentTracker.api_url"}})],1)],1),e._v(" "),n("div",{staticClass:"modal-footer text-right"},[n("md-button",{staticClass:"md-primary",on:{click:e.deleteTracker}},[e._v("удалить")]),e._v(" "),n("md-button",{staticClass:"md-primary",on:{click:e.closeTrackerModal}},[e._v("отмена")]),e._v(" "),n("md-button",{staticClass:"md-accent",on:{click:e.saveTracker}},[e._v("сохранить")])],1)]),e._v(" "),n("modal",{attrs:{show:e.showToken},on:{close:e.closeTokenModal}},[n("div",{staticClass:"modal-header"},[n("h2",[e._v("Данные для авторизации в "+e._s(e.currentTracker.title))])]),e._v(" "),n("div",{staticClass:"modal-body"},[n("input",{directives:[{name:"model",rawName:"v-model",value:e.currentTracker.id,expression:"currentTracker.id"}],attrs:{type:"hidden",name:"id"},domProps:{value:e.currentTracker.id},on:{input:function(t){t.target.composing||e.$set(e.currentTracker,"id",t.target.value)}}}),e._v(" "),n("input",{directives:[{name:"model",rawName:"v-model",value:e.currentTracker.type,expression:"currentTracker.type"}],attrs:{type:"hidden",name:"type"},domProps:{value:e.currentTracker.type},on:{input:function(t){t.target.composing||e.$set(e.currentTracker,"type",t.target.value)}}}),e._v(" "),n("md-field",[n("label",[e._v("Логин")]),e._v(" "),n("md-input",{model:{value:e.loginToken,callback:function(t){e.loginToken=t},expression:"loginToken"}})],1),e._v(" "),n("md-field",[n("label",[e._v("Пароль")]),e._v(" "),n("md-input",{attrs:{type:"password"},model:{value:e.passwordToken,callback:function(t){e.passwordToken=t},expression:"passwordToken"}})],1)],1),e._v(" "),n("div",{staticClass:"modal-footer text-right"},[n("md-button",{staticClass:"md-primary",on:{click:e.closeTokenModal}},[e._v("отмена")]),e._v(" "),n("md-button",{staticClass:"md-accent",on:{click:e.getToken}},[e._v("получить")])],1)]),e._v(" "),n("modal",{attrs:{show:e.showUser}},[n("div",{staticClass:"modal-header"},[n("h2",[e._v("Выберите пользователя в "+e._s(e.currentTracker.title))])]),e._v(" "),n("div",{staticClass:"modal-body"},[n("input",{directives:[{name:"model",rawName:"v-model",value:e.currentTracker.id,expression:"currentTracker.id"}],attrs:{type:"hidden",name:"id"},domProps:{value:e.currentTracker.id},on:{input:function(t){t.target.composing||e.$set(e.currentTracker,"id",t.target.value)}}}),e._v(" "),n("v-select",{attrs:{options:e.evoUsers},model:{value:e.evoUser,callback:function(t){e.evoUser=t},expression:"evoUser"}})],1),e._v(" "),n("div",{staticClass:"modal-footer text-right"},[n("md-button",{staticClass:"md-primary",on:{click:e.closeUserModal}},[e._v("отмена")]),e._v(" "),n("md-button",{staticClass:"md-accent",on:{click:e.saveEvoUser}},[e._v("сохранить")])],1)]),e._v(" "),n("md-dialog-alert",{attrs:{"md-active":e.showAlert,"md-content":e.alertMessage,"md-confirm-text":"Ок"},on:{"update:mdActive":function(t){e.showAlert=t}}})],1)},staticRenderFns:[]};var i=n("VU/8")(a,r,!1,function(e){n("iWMn")},"data-v-0019876c",null);t.default=i.exports},q3Hp:function(e,t,n){"use strict";Object.defineProperty(t,"__esModule",{value:!0});var s=n("Ppbp"),a=n.n(s),r=n("rrOh"),i={data:function(){return{selectedDate:{start:new Date,end:new Date},time:[new Date,new Date],shortcuts:[{text:"сегодня",start:new Date,end:new Date},{text:"вчера",start:new Date((new Date).setDate((new Date).getDate()-1)),end:new Date((new Date).setDate((new Date).getDate()-1))},{text:"эта неделя",start:new Date((new Date).setDate((new Date).getDate()-((new Date).getDay()||7)+1)),end:new Date((new Date).setDate((new Date).getDate()-((new Date).getDay()||7)+7))},{text:"прошлая",start:new Date((new Date).setDate((new Date).getDate()-((new Date).getDay()||7)-6)),end:new Date((new Date).setDate((new Date).getDate()-((new Date).getDay()||7)))}]}},methods:{onDateSelected:function(e){2===e.length&&null!==e[0]&&null!==e[1]&&(this.selectedDate.start=e[0],this.selectedDate.end=e[1],this.$refs.grouped_tasks.selectedDate=this.selectedDate,this.refreshData())},refreshData:function(){this.$refs.grouped_tasks.getTasks()}},components:{DatePicker:a.a,ExportTasks:r.default},mounted:function(){this.$refs.rangeDatePicker.dateRange=this.selectedDate}},o={render:function(){var e=this,t=e.$createElement,n=e._self._c||t;return n("div",[n("div",{staticClass:"md-layout md-gutter md-alignment-top-center center"},[n("div",{staticClass:"md-layout-item md-size-50"},[n("date-picker",{ref:"rangeDatePicker",attrs:{"first-day-of-week":1,confirm:"",lang:"ru",range:"",format:"DD.MM.YYYY",shortcuts:e.shortcuts},on:{change:e.onDateSelected},model:{value:e.time,callback:function(t){e.time=t},expression:"time"}})],1)]),e._v(" "),n("ExportTasks",{ref:"grouped_tasks",attrs:{initialDate:e.selectedDate},on:{update:function(t){e.refreshData()}}})],1)},staticRenderFns:[]},c=n("VU/8")(i,o,!1,null,null,null);t.default=c.exports},"s6+2":function(e,t,n){"use strict";Object.defineProperty(t,"__esModule",{value:!0});var s=n("lO7g"),a=n("yZHR"),r=n("J+R/"),i=n("q3Hp"),o=n("niH5"),c=n("9YsO"),l=n("YcJa"),d=n("WdI8"),u=n("VTQS"),v={data:function(){return{currentComponent:null,loginText:"Выйти",isLogin:!1,version:null,timer:null,dialog:{show:!1,title:"Доступна новая версия!",content:""}}},components:{Home:s.default,History:a.default,Auth:r.default,Export:i.default,Settings:o.default,Help:c.default,NotFound:l.default},methods:{updateLogin:function(){this.isLogin=Object(d.b)(),this.loginText=this.isLogin?"Выйти":"Войти";var e=location.pathname.substr(1);e=e.charAt(0).toUpperCase()+e.slice(1),this.isLogin?"Auth"===e||""===e?this.go("Home"):-1!==["Home","History","Export","Help","Settings"].indexOf(e)?this.go(e):this.go("NotFound"):"Help"===e?this.go(e):this.go("Auth")},getVersion:function(){var e=this;u.b.getVersion(this.version).then(function(t){null===e.version?e.version=t.data.version:e.version<parseFloat(t.data.version)&&(e.dialog.content="Изменения:<br>"+t.data.changes.join("<br>")+"<br><br>Обновить страницу?",e.dialog.show=!0)}).catch(function(e){console.log(["getVersion error",e])})},go:function(e){e!==this.currentComponent&&(-1!==["Auth","Help"].indexOf(e)?("Auth"===e&&this.isLogin&&(Object(d.c)(),this.isLogin=Object(d.b)(),this.loginText=this.isLogin?"Выйти":"Войти"),this.currentComponent=e,this.changeUrl(e)):this.isLogin?(this.currentComponent=e,this.changeUrl(e)):this.updateLogin())},changeUrl:function(e){window.history.replaceState?window.history.replaceState(e,e,"/"+e.toLowerCase()):window.history.pushState(e,e,"/"+e.toLowerCase())},onConfirm:function(){location.reload(!0)},onCancel:function(){this.dialog.show=!1}},mounted:function(){this.updateLogin(),this.getVersion(),this.timer=setInterval(this.getVersion,3e5)}},m={render:function(){var e=this,t=e.$createElement,n=e._self._c||t;return n("div",[n("nav",[n("div",{staticClass:"md-toolbar md-accent md-theme-demo-light md-elevation-1"},[n("div",{staticClass:"md-title main-title"},[n("a",{on:{click:function(t){e.go("Home")}}},[e._v("Time tracker")])]),e._v(" "),n("button",{staticClass:"md-button md-theme-demo-light short",attrs:{type:"button"},on:{click:function(t){e.go("Help")}}},[n("font-awesome-icon",{class:"Help"==e.currentComponent?"current":"",attrs:{icon:"question-circle"}})],1),e._v(" "),e.isLogin?n("button",{staticClass:"md-button md-theme-demo-light",attrs:{type:"button"},on:{click:function(t){e.go("Home")}}},[n("div",{staticClass:"md-ripple"},[n("div",{staticClass:"md-button-content",class:"Home"==e.currentComponent?"current":""},[e._v("Главный экран")])])]):e._e(),e._v(" "),e.isLogin?n("button",{staticClass:"md-button md-theme-demo-light",attrs:{type:"button"},on:{click:function(t){e.go("History")}}},[n("div",{staticClass:"md-ripple"},[n("div",{staticClass:"md-button-content",class:"History"==e.currentComponent?"current":""},[e._v("История")])])]):e._e(),e._v(" "),e.isLogin?n("button",{staticClass:"md-button md-theme-demo-light",attrs:{type:"button"},on:{click:function(t){e.go("Export")}}},[n("div",{staticClass:"md-ripple"},[n("div",{staticClass:"md-button-content",class:"Export"==e.currentComponent?"current":""},[e._v("Экспорт")])])]):e._e(),e._v(" "),e.isLogin?n("button",{staticClass:"md-button md-theme-demo-light",attrs:{type:"button"},on:{click:function(t){e.go("Settings")}}},[n("div",{staticClass:"md-ripple"},[n("div",{staticClass:"md-button-content",class:"Settings"==e.currentComponent?"current":""},[e._v("Настройки")])])]):e._e(),e._v(" "),n("button",{staticClass:"md-button md-theme-demo-light",attrs:{type:"button"},on:{click:function(t){e.go("Auth")}}},[n("div",{staticClass:"md-ripple"},[n("div",{staticClass:"md-button-content",class:"Auth"==e.currentComponent?"current":""},[e._v(e._s(e.loginText))])])])])]),e._v(" "),n("div",{staticClass:"container",attrs:{id:"main"}},[n(e.currentComponent,{tag:"component",on:{login:e.updateLogin}})],1),e._v(" "),n("md-dialog-confirm",{attrs:{"md-active":e.dialog.show,"md-title":e.dialog.title,"md-content":e.dialog.content,"md-confirm-text":"Да","md-cancel-text":"Обновлю позже"},on:{"update:mdActive":function(t){e.$set(e.dialog,"show",t)},"md-cancel":e.onCancel,"md-confirm":e.onConfirm}})],1)},staticRenderFns:[]};var _=n("VU/8")(v,m,!1,function(e){n("ZBq/")},null,null);t.default=_.exports},yZHR:function(e,t,n){"use strict";Object.defineProperty(t,"__esModule",{value:!0});var s=n("Ppbp"),a=n.n(s),r=n("N1EC"),i={data:function(){return{selectedDate:{start:new Date,end:new Date},time:[new Date,new Date],shortcuts:[{text:"сегодня",start:new Date,end:new Date},{text:"вчера",start:new Date((new Date).setDate((new Date).getDate()-1)),end:new Date((new Date).setDate((new Date).getDate()-1))},{text:"эта неделя",start:new Date((new Date).setDate((new Date).getDate()-((new Date).getDay()||7)+1)),end:new Date((new Date).setDate((new Date).getDate()-((new Date).getDay()||7)+7))},{text:"прошлая",start:new Date((new Date).setDate((new Date).getDate()-((new Date).getDay()||7)-6)),end:new Date((new Date).setDate((new Date).getDate()-((new Date).getDay()||7)))},{text:"месяц",start:new Date((new Date).setDate(1)),end:new Date(new Date(new Date((new Date).setDate(1)).setMonth((new Date).getMonth()+1)).setDate(0))},{text:"прошлый",start:new Date(new Date((new Date).setDate(1)).setMonth((new Date).getMonth()-1)),end:new Date(new Date((new Date).setDate(1)).setDate(0))}]}},methods:{onDateSelected:function(e){2===e.length&&null!==e[0]&&null!==e[1]&&(this.selectedDate.start=e[0],this.selectedDate.end=e[1],this.$refs.tasks.selectedDate=this.selectedDate,this.$refs.tasks.getTasks())},refreshData:function(){this.$refs.tasks.getTasks()}},components:{DatePicker:a.a,Tasks:r.default},mounted:function(){this.$refs.rangeDatePicker.dateRange=this.selectedDate}},o={render:function(){var e=this,t=e.$createElement,n=e._self._c||t;return n("div",[n("div",{staticClass:"md-layout md-gutter md-alignment-top-center center"},[n("div",{staticClass:"md-layout-item md-size-50"},[n("date-picker",{ref:"rangeDatePicker",attrs:{"first-day-of-week":1,confirm:"",lang:"ru",range:"",format:"DD.MM.YYYY",shortcuts:e.shortcuts},on:{change:e.onDateSelected},model:{value:e.time,callback:function(t){e.time=t},expression:"time"}})],1)]),e._v(" "),n("Tasks",{ref:"tasks",attrs:{initialDate:e.selectedDate},on:{update:function(t){e.refreshData()}}})],1)},staticRenderFns:[]},c=n("VU/8")(i,o,!1,null,null,null);t.default=c.exports}});
//# sourceMappingURL=1.9afca069c0f1a8aa2a6e.js.map