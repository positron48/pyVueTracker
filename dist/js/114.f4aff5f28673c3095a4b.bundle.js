"use strict";(self.webpackChunktracker=self.webpackChunktracker||[]).push([[114],{5389:function(_,v,n){var t=n(4991),i=n.n(t),s=n(6314),r=n.n(s)()(i());r.push([_.id,"","",{version:3,sources:[],names:[],mappings:"",sourceRoot:""}]),v.A=r},6114:function(_,v,n){n.r(v),n.d(v,{default:function(){return e}});var t=function(){return this._self._c,this._m(0)};t._withStripped=!0;var i=n(5072),s=n.n(i),r=n(5389),e=(s()(r.A,{insert:"head",singleton:!1}),r.A.locals,(0,n(4486).A)({data:function(){return{}}},t,[function(){var _=this,v=_._self._c;return v("div",[v("div",{staticClass:"md-layout md-gutter md-alignment-top-center"},[v("div",{staticClass:"md-layout-item md-large-size-80 md-xlarge-size-80 md-medium-size-90 md-small-size-100"},[v("h2",[_._v("Добавление задач")]),_._v(" "),v("p",[_._v("\n      При добавлении задачи можно (и нужно) сразу указать название задачи и проект, если задача заведена в редмайне,\n      то первым пишется ее номер.\n      ")]),_._v(" "),v("p",[_._v("\n      Синтаксис поля ввода задачи следующий: "),v("br"),_._v(" "),v("i",[_._v("[время выполнения] [номер задачи в редмайн] краткое описания задачи [@проект][#тег][, комментарий]")])]),_._v(" "),v("p",[_._v("\n      Детальнее по полям:\n      "),v("ul",[v("li",[v("b",[_._v("время выполнения")]),_._v(" - указывается время выполнения задачи, в различных форматах:"),v("br"),_._v(" "),v("b",[v("i",[_._v("-10")])]),_._v(" работа над задачей началась 10 минут назад"),v("br"),_._v(" "),v("b",[v("i",[_._v("11:50")])]),_._v(" работа над задачей началась в 11:50"),v("br"),_._v(" "),v("b",[v("i",[_._v("11:50-12:20")])]),_._v(" работа над задачей началась в 11:50 и завершилась в 12:20\n        ")]),_._v(" "),v("li",[v("b",[_._v("номер задачи в редмайн")]),_._v(" - нужно указывать, если нужно выгружать часы по этой задаче в редмайн\n        ")]),_._v(" "),v("li",[v("b",[_._v("краткое описания задачи")]),_._v(" - краткое описание, чтобы не забыть о чем задача\n        ")]),_._v(" "),v("li",[v("b",[_._v("[@проект]")]),_._v(" - название проекта, в рамках которого делается задача. Может быть произвольным, при экспорте\n           можно будет сопоставить с трекерами вручную, если название не совпадает с названием на трекере."),v("br"),_._v('\n           Если не указать проект, будет автоматически проставлен "untitled" (без названия)\n        ')]),_._v(" "),v("li",[v("b",[_._v("#тег")]),_._v(" - поле используется только в статистике, помечая задачи тем или иным тегом можно будет увидеть,\n           сколько по времени занимала та или иная деятельность, например, #разработка #инкубатор #обучение.\n           Тегов может быть несколько\n        ")]),_._v(" "),v("li",[v("b",[_._v("комментарий")]),_._v(" - комментарий, описывающий конкретную часть задачи, над которой идет работа\n           в настоящее время. Будет выгружен в комментарий редмайна и evo соответственно."),v("br"),_._v("\n           Обязателен, если задача отсутствует в редмайне, но можно указать на этапе экспорта\n        ")])])]),_._v(" "),v("p",[_._v("\n        Таким образом, корректные примеры указания задач могут выглядеть следующим образом:"),v("br"),_._v(" "),v("ul",[v("li",[_._v("55123 таймтрекер@инкубатор #разработка, написание руководства пользователя")]),_._v(" "),v("li",[_._v("-30 поддержка столплит@столплит #поддержка, прогрузка данных по заказам из 1с")]),_._v(" "),v("li",[_._v("11:20-12:50 митап@развитие интаро")]),_._v(" "),v("li",[_._v("заполню потом")])])]),_._v(" "),v("p",[_._v('\n        Пользуясь клавишей Tab можно подставлять в строку символы "@/#/,", переключая таким образом вводимое поле.\n        Shift+Tab переключает символы в обратном порядке\n      ')]),_._v(" "),v("br"),v("br"),_._v(" "),v("h2",[_._v("Интерфейс")]),_._v(" "),v("p",[_._v("Основной интерфейс выглядит следующим образом:")]),_._v(" "),v("img",{staticClass:"center",attrs:{src:"/static/screen_main_top.png"}}),_._v(" "),v("img",{staticClass:"center",attrs:{src:"/static/screen_main_bottom.png"}}),_._v(" "),v("p",[_._v("\n      По блокам сверху вниз:\n      "),v("ul",[v("li",[_._v("текущая задача")]),_._v(" "),v("li",[_._v("поле ввода новой задачи")]),_._v(" "),v("li",[_._v("\n          график распределения задач по часам. По оси Х сутки, разбитые по часам, по оси Y количество времени,\n          затраченное в конкретный час. Например 16 это время с 16:00 до 17:00, потрачено полчаса\n        ")]),_._v(" "),v("li",[_._v("список задач за текущий день")]),_._v(" "),v("li",[_._v("диаграмма распределения часов по задачам")]),_._v(" "),v("li",[_._v("диаграмма распределения часов по проектам")]),_._v(" "),v("li",[_._v("диаграмма распределения часов по тегам")])])]),_._v(" "),v("br"),v("br"),_._v(" "),v("h2",[_._v("Настройки")]),_._v(" "),v("p",[_._v("Для работы выгрузки часов в внешние трекеры вам нужно авторизоваться на этих трекерах.")]),_._v(" "),v("p",[_._v('\n        Чтобы авторизоваться, перейдите в меню "Настройки", нажмите на ссылку "Получить токен", введите свой логин и\n        пароль'),v("sup",[_._v("*")]),_._v(' от соответствующего трекера и кликните по кнопке "Сохранить". В итоге в табличке отобразится ваш токен.\n      ')]),_._v(" "),v("p",[_._v('\n        Для evo требуется также указать сотрудника, которому будут проставляться выгружаемые часы.\n        Нужно кликнуть на ссылку "Указать пользователя" и выбрать себя из списка.\n      ')]),_._v(" "),v("img",{staticClass:"center",attrs:{src:"/static/screen_settings.png"}}),_._v(" "),v("p",[_._v("На этой же странице можно добавить еще один трекер, если для вашей работы необходимо проставлять часы в нескольких")]),_._v(" "),v("p",{staticStyle:{"font-color":"gray"}},[_._v("\n        *логин и пароль используются исключительно для получения токена авторизации и не хранятся на сервере.\n      ")]),_._v(" "),v("br"),v("br"),_._v(" "),v("h2",[_._v("Экспорт задач")]),_._v(" "),v("p",[_._v("Для выгрузки задач нужно перейти в раздел экспорт, где отобразятся сгруппированные задачи за день.")]),v("p"),v("p",[_._v("У всех элементов интерфейса, которые требуют пояснения, при наведении появляется подсказка.")]),_._v(" "),v("p",[_._v("\n      У каждой задачи в крайнем правом столбце есть список трекеров, привязанных к задаче.\n      Цвет отражает статус трекера:\n      "),v("ul",[v("li",[_._v("\n          синий - задача готова к выгрузке на указанный трекер, при наведении отображается название проекта на трекере\n        ")]),_._v(" "),v("li",[_._v("\n          серый - не найдено соответствие проекта, нужно указать вручную, если нужно выгрузить часы на этот трекер\n           (указывается 1 раз для проекта)\n         ")]),_._v(" "),v("li",[_._v("\n          красный - задача сопоставлена, но по какой-то причине не может быть выгружена\n          (не получен токен авторизации в настройках, не указан номер задачи для редмайн, задача с таким номером\n          не существует или для ее просмотра недостаточно прав)\n         ")]),_._v(" "),v("li",[_._v("\n          желтый - задача готова к выгрузке на указанный трекер, но по ней есть предупреждение (проект задачи не\n          совпадает с сопоставленным, так бывает, когда в редмайне один проект разбит на несколько, а в эво один)\n        ")]),_._v(" "),v("li",[_._v("\n          зеленый - задача успешно выгружена на трекер\n        ")]),_._v(" "),v("li",[_._v("\n          черный - при выгрузке на трекер произошла ошибка\n        ")])])]),_._v(" "),v("p",[_._v("\n        Непосредственно на этапе экспорта можно отредактировать все данные по задачам\n        (дату, номер задачи, комментарий, часы), такие изменения повлияют только на выгрузку часов и нигде не будут учтены.\n      ")]),_._v(" "),v("p",[_._v("\n        Галочкой можно отметить, нужно ли выгружать задачу на тот или иной трекер.\n      ")]),_._v(" "),v("img",{staticClass:"center",attrs:{src:"/static/screen_export.png"}})])])])}],!1,null,null,null).exports)}}]);