// GroupedTasks.vue
<template>
  <div>
    <div class="md-layout md-gutter md-alignment-top-center">
      <div class="md-layout-item md-large-size-80 md-xlarge-size-90 md-medium-size-100 md-small-size-100 taskItems minimal-input" v-if="tasks.length">

        <template v-for="taskGroup in groupedTasks">

          <md-list :key="taskGroup.date" class="task-group">
            <md-list-item class="task-group-date">
              {{taskGroup.date}}
            </md-list-item>
            <md-table>
              <md-table-row>
                <md-table-head class="column-task-date">
                  Дата
                </md-table-head>
                <md-table-head>Задача</md-table-head>
                <md-table-head class="column-task-number">
                  Номер задачи
                  <md-tooltip md-direction="top">Номер задачи из редмайна</md-tooltip>
                </md-table-head>
                <md-table-head>Комментарий</md-table-head>
                <md-table-head>
                  Проект
                  <md-tooltip md-direction="top">Название проекта в таймтрекере</md-tooltip>
                </md-table-head>
                <md-table-head class="column-task-time">
                  Время
                </md-table-head>
                <md-table-head>
                  Трекеры
                  <md-tooltip md-direction="top">Список трекеров, привязанных к проекту</md-tooltip>
                </md-table-head>
              </md-table-row>

              <template v-for="(task, taskKey) in taskGroup.tasks">
                <md-table-row :key="task.id">
                  <md-table-cell class="column-task-date">
                    <md-field>
                      <label></label>
                      <md-input v-model="task.date"></md-input>
                    </md-field>
                  </md-table-cell>
                  <md-table-cell class="column-task-name">
                    <md-field>
                      <label></label>
                      <md-input v-model="task.name"></md-input>
                    </md-field>
                  </md-table-cell>
                  <md-table-cell class="column-task-number">
                    <md-field>
                      <label></label>
                      <md-input v-model="task.task_id" type="number" min="1" :class="task.external_status"></md-input>
                      <md-tooltip md-direction="top" v-if="task.external_message">{{task.external_message}}</md-tooltip>
                    </md-field>
                  </md-table-cell>
                  <md-table-cell>
                    <md-field>
                      <label></label>
                      <md-textarea v-model="task.description" md-autogrow></md-textarea>
                    </md-field>
                  </md-table-cell>
                  <md-table-cell>
                      <div>{{task.category}}</div>
                  </md-table-cell>
                  <md-table-cell class="column-task-time">
                    <md-field>
                      <label></label>
                      <md-input v-model="task.delta" type="number" min="0" step="0.05"></md-input>
                      <md-tooltip md-direction="top" v-if="task.delta_full">{{task.delta_full}}</md-tooltip>
                    </md-field>
                  </md-table-cell>
                  <md-table-cell class="column-task-trackers">
                    <template v-for="tracker in task.trackers">
                      <span v-bind:key="tracker.id + '_' + task.id" :class="tracker.status">
                        <md-checkbox @change="groupTasksRecompute()" v-model="taskTrackerData[task.date][taskKey][tracker.id]['needExport']" class="tracker-checkbox" :disabled="tracker.disabled"></md-checkbox>
                        <a v-if="tracker.type !== 'jira'" class="tracker-badge" @click="linkProject(tracker.id, task.project_id)">
                          {{tracker.title}}
                        </a>
                        <span class="tracker-badge" v-if="tracker.type === 'jira'">
                          {{tracker.title}}
                        </span>
                        <md-tooltip md-direction="left">{{tracker.message}}</md-tooltip>
                      </span>
                    </template>
                  </md-table-cell>
                </md-table-row>
              </template>

            </md-table>
            <md-list-item class="task-duration-list-item">
              {{taskGroup.duration}}
            </md-list-item>
            <md-list-item v-for="(duration, title) in taskGroup.durationByTrackers" :key="taskGroup.date + title" class="task-duration-list-item tracker-durations">
              {{title}}: {{duration}}
              <span v-bind:key="title">

                <md-checkbox
                  class="tracker-check-all"
                  v-model="trackersSummary[title][taskGroup.date]['allChecked']"
                  :disabled="trackersSummary[title][taskGroup.date]['disabled']"
                  @change="changeTrackerChecked(title, taskGroup.date)"
                ></md-checkbox>

                <md-tooltip md-direction="left" v-if="!trackersSummary[title][taskGroup.date]['disabled']">Отметить все задачи трекера</md-tooltip>
              </span>
            </md-list-item>
          </md-list>
        </template>

        <md-list class="task-group" v-if="Object.keys(groupedTasks).length > 1">
          <md-list-item v-for="(tracker, key) in trackers" :key="key" class="task-duration-list-item tracker-durations">
            {{trackers[key]['title']}}: {{trackersSummary[trackers[key]['title']]['duration']}}
            <span v-bind:key="key">

              <md-checkbox
                class="tracker-check-all"
                v-model="trackersSummary[trackers[key]['title']]['allChecked']"
                :disabled="trackersSummary[trackers[key]['title']]['disabled']"
                @change="changeTrackerChecked(trackers[key]['title'], null)"
              ></md-checkbox>

              <md-tooltip md-direction="left" v-if="!trackersSummary[trackers[key]['title']]['disabled']">Отметить все задачи трекера</md-tooltip>
            </span>
          </md-list-item>
        </md-list>
      </div>
    </div>

    <div class="md-layout md-gutter md-alignment-top-center center" v-if="Object.keys(groupedTasks).length">
      <div class="md-layout-item md-size-50">
        <md-tooltip md-direction="top">Выгрузить часы в отмеченные трекеры</md-tooltip>
        <md-button class="md-raised md-accent" :disabled="exportDisabled || exportingTaskCount > 0" @click="exportTasks()">Экспортировать</md-button>
      </div>
    </div>

    <modal :show="showLink">
      <div class="modal-header">
        <h2>Укажите проект в {{currentTracker.title}}</h2>
      </div>
      <div class="modal-body">
        <input type="hidden" v-model="currentTracker.id" name="trackerId">
        <input type="hidden" v-model="currentProject" name="projectId">
        <v-select v-model="linkToProject" :options="currentTrackerProjects"/>
      </div>
      <div class="modal-footer text-right">
        <md-button class="md-primary" @click="closeLinkModal">отмена</md-button>
        <md-button class="md-accent" @click="saveLinkProject">сохранить</md-button>
      </div>
    </modal>
    <md-dialog-alert
      :md-active.sync="haveNotClosedTask"
      :md-content="dialogMessage"
      md-confirm-text="Ок" />
    <md-dialog-alert :md-active.sync="showAlert" :md-content="alertMessage" md-confirm-text="Ок" />
  </div>
</template>

<script>
import API from './api.js'
import Modal from './Modal.vue'

export default {
  data () {
    return {
      tasks: [],
      trackerTasks: {},
      projects: [],
      trackers: [],
      selectedDate: {
        start: new Date(),
        end: new Date()
      },
      show: false,
      labelWidth: 200,
      exportDisabled: true,
      loadingTaskCount: 0,
      exportingTaskCount: 0,
      taskTrackerData: {},

      currentTracker: [],
      currentProject: null,
      showLink: false,
      linkToProject: null,
      trackerProjects: {},
      currentTrackerProjects: [],

      haveNotClosedTask: false,
      dialogMessage: 'У вас есть незавершенные задачи, они не будут экспортированы',

      showAlert: false,
      alertMessage: ''
    }
  },
  props: {
    initialDate: {
      type: Object
    }
  },
  recomputed: {
    groupedTasks: function () {
      var groupedTasks = {}
      var haveTaskToExport = false
      var statusMessage = ''
      for (var i = 0; i < this.tasks.length; i++) {
        var task = this.tasks[i]

        // дни
        if (groupedTasks[task['date']] === undefined) {
          groupedTasks[task['date']] = {duration: 0, durationByTrackers: {}, tasks: [], date: task['date']}
        }
        var delta = parseFloat(task['delta'])

        task['trackers'] = []
        for (var j = 0; j < this.trackers.length; j++) {
          var tracker = {
            id: this.trackers[j]['id'],
            type: this.trackers[j]['type'],
            title: this.trackers[j]['title'],
            status: (this.projects[task['project_id']] !== undefined &&
              this.projects[task['project_id']]['tracker_projects'][this.trackers[j]['id']] !== undefined &&
              this.projects[task['project_id']]['tracker_projects'][this.trackers[j]['id']]['external_project_id'] > 0
            ) ? 'linked' : '',
            available: false
          }

          // если задача сопоставлена с редмайном, получаем ее номер
          var externalTask = this.trackerTasks[tracker.id][task['task_id']]
          if (
            task['task_id'] > 0 &&
            tracker.type === 'redmine' && tracker.status === 'linked'
          ) {
            if (externalTask === undefined) {
              this.trackerTasks[tracker.id][task['task_id']] = {}
              this.getTrackerTask(tracker.id, task['task_id'])
            } else if (externalTask['name'] !== undefined) {
              task['external_status'] = 'linked'
              task['external_name'] = externalTask['name']
              task['external_message'] = '[' + externalTask['project'] + '] ' + externalTask['tracker'] +
                ' #' + externalTask['id'] + ': ' + externalTask['name']
            }
          } else if (
            task['task_id'] > 0 &&
            tracker.type === 'jira' &&
            externalTask !== undefined &&
            externalTask['name'] !== undefined
          ) {
            tracker['status'] = 'linked'
            tracker['message'] = '[' + externalTask['project'] + '] ' +
              ' #' + externalTask['id'] + ': ' + externalTask['name']
          }

          // todo: status: ?warning? часы за этот день по проекту уже выгружались
          var exportStatus = this.getTaskExportStatus(task['date'], groupedTasks[task['date']].tasks.length, tracker.id)
          if (task['exportedTrackers'].indexOf(tracker.id) !== -1) {
            tracker['status'] = 'exported'
            tracker['message'] = 'задача была выгружена ранее'
          } else if (exportStatus === true) {
            tracker['status'] = 'exported'
            tracker['message'] = 'задача выгружена'
          } else if (exportStatus === false) {
            tracker['status'] = 'fatal'
            tracker['message'] = 'при выгрузке произошла ошибка'
            statusMessage = this.getTaskTrackerValue(task['date'], groupedTasks[task['date']].tasks.length, tracker.id, 'statusMessage')
            if (typeof statusMessage === 'string' && statusMessage.length > 0) {
              tracker['message'] = statusMessage
            }
          } else if (
            this.trackersById[tracker['id']] !== undefined &&
            this.trackersById[tracker['id']]['external_user_id'] === null
          ) {
            tracker['status'] = 'error'
            tracker['message'] = 'вы не авторизованы на трекере, зайдите в настройки'
          } else if (
            tracker['status'] === 'linked' &&
            tracker['type'] === 'redmine' &&
            !task['task_id']
          ) {
            tracker['status'] = 'error'
            tracker['message'] = 'не указан номер задачи'
          } else if (
            tracker['status'] === 'linked' &&
            tracker['type'] === 'redmine' &&
            task['task_id'] > 0 &&
            externalTask === false
          ) {
            tracker['status'] = 'error'
            tracker['message'] = 'не получены данные по задаче'
            task['external_status'] = 'error'
            task['external_message'] = 'не получены данные по задаче'
          } else if (
            tracker['status'] === 'linked' &&
            tracker['type'] === 'redmine' &&
            task['task_id'] > 0 &&
            typeof externalTask === 'object' && externalTask !== null &&
            this.projects[task['project_id']]['tracker_projects'][this.trackers[j]['id']] !== undefined &&
            externalTask['project_id'] !== this.projects[task['project_id']]['tracker_projects'][this.trackers[j]['id']]['external_project_id']
          ) {
            tracker['status'] = 'warning'
            tracker['message'] = 'проект в редмайне отличается от указанного'
          } else if (tracker['type'] !== 'jira') {
            tracker['message'] = tracker['status'] === 'linked'
              ? this.projects[task['project_id']]['tracker_projects'][this.trackers[j]['id']]['external_project_title']
              : 'проект не сопоставлен'
          } else if (tracker['type'] === 'jira' && (tracker['message'] === undefined || tracker['message'] === '')) {
            tracker['message'] = 'задача не найдена'
          }

          var needExport = this.getTaskNeedExport(task['date'], groupedTasks[task['date']].tasks.length, tracker.id)
          if (tracker['status'] === 'linked' || tracker['status'] === 'warning' || tracker['status'] === 'fatal') {
            tracker['available'] = needExport
            if (needExport === null) {
              tracker['available'] = true
            }
            tracker['disabled'] = false
          } else {
            tracker['available'] = false
            tracker['disabled'] = true
          }
          if (needExport === null && tracker['available']) {
            this.setTaskNeedExport(task['date'], groupedTasks[task['date']].tasks.length, tracker.id, tracker['available'])
          } else if (needExport === null && tracker['available'] !== true) {
            this.setTaskNeedExport(task['date'], groupedTasks[task['date']].tasks.length, tracker.id, null)
          } else if (tracker['status'] === '') {
            this.setTaskNeedExport(task['date'], groupedTasks[task['date']].tasks.length, tracker.id, null)
          }

          if (groupedTasks[task['date']]['durationByTrackers'][tracker.title] === undefined) {
            groupedTasks[task['date']]['durationByTrackers'][tracker.title] = 0
          }
          if (this.getTaskNeedExport(task['date'], groupedTasks[task['date']].tasks.length, tracker.id)) {
            groupedTasks[task['date']]['durationByTrackers'][tracker.title] += delta > 0 ? delta : 0
            groupedTasks[task['date']]['durationByTrackers'][tracker.title] =
              Math.round(groupedTasks[task['date']]['durationByTrackers'][tracker.title] * 100) / 100

            haveTaskToExport = true
          }

          task['trackers'].push(tracker)
        }

        // ставим ошибку, если для не указан номер задачи и не заполнен комментарий для эво
        for (var k = 0; k < this.trackers.length; k++) {
          var trackerTask = task['trackers'][k]
          if (
            trackerTask['status'] === 'linked' &&
            trackerTask['type'] === 'evo' &&
            (task['external_name'] === undefined || task['external_name'] === '') &&
            task['description'] === ''
          ) {
            task['trackers'][k]['status'] = 'error'
            task['trackers'][k]['message'] = 'не заполнен комментарий'
          }
        }

        groupedTasks[task['date']]['tasks'].push(task)
        groupedTasks[task['date']]['duration'] += delta > 0 ? delta : 0

        // со сложением вместе округление работать не хочет
        groupedTasks[task['date']]['duration'] = Math.round(groupedTasks[task['date']]['duration'] * 100) / 100
      }
      if (this.loadingTaskCount === 0 && haveTaskToExport === true) {
        this.exportDisabled = false
      } else if (this.loadingTaskCount === 0 && haveTaskToExport === false) {
        this.exportDisabled = true
      }
      return groupedTasks
    },
    trackersSummary: function () {
      var result = {}

      var dates = Object.keys(this.groupedTasks)
      for (var t = 0; t < this.trackers.length; t++) {
        result[this.trackers[t].title] = { allChecked: true, disabled: true, duration: 0 }
        for (var d = 0; d < dates.length; d++) {
          result[this.trackers[t].title][dates[d]] = { allChecked: true, disabled: true, duration: 0 }
        }
      }

      for (var i = 0; i < dates.length; i++) {
        var tracker = null
        for (var taskKey = 0; taskKey < this.groupedTasks[dates[i]].tasks.length; taskKey++) {
          var task = this.groupedTasks[dates[i]].tasks[taskKey]
          for (var j = 0; j < this.groupedTasks[dates[i]].tasks[taskKey].trackers.length; j++) {
            tracker = this.groupedTasks[dates[i]].tasks[taskKey].trackers[j]
            result[tracker.title][dates[i]]['allChecked'] = result[tracker.title][dates[i]]['allChecked'] && (tracker.disabled || this.taskTrackerData[task.date][taskKey][tracker.id]['needExport'])
            result[tracker.title][dates[i]]['disabled'] = result[tracker.title][dates[i]]['disabled'] && tracker.disabled

            result[tracker.title]['allChecked'] = result[tracker.title]['allChecked'] && (tracker.disabled || this.taskTrackerData[task.date][taskKey][tracker.id]['needExport'])
            result[tracker.title]['disabled'] = result[tracker.title]['disabled'] && tracker.disabled
          }
        }
        for (var k = 0; k < this.trackers.length; k++) {
          tracker = this.trackers[k]
          if (tracker.title in this.groupedTasks[dates[i]]['durationByTrackers']) {
            result[tracker.title]['duration'] += this.groupedTasks[dates[i]]['durationByTrackers'][tracker.title]
          }
        }
      }

      for (var r = 0; r < this.trackers.length; r++) {
        if (result[this.trackers[r].title].disabled) {
          result[this.trackers[r].title].allChecked = false
          for (var w = 0; w < dates.length; w++) {
            result[this.trackers[r].title][dates[w]].allChecked = false
          }
        }
      }

      return result
    }
  },
  computed: {
    trackersById: function () {
      var result = {}
      for (var i = 0; i < this.trackers.length; i++) {
        result[this.trackers[i]['id']] = this.trackers[i]
      }
      return result
    },
    projectIds: function () {
      var projectIds = []
      this.tasks.forEach(function (task, i) {
        projectIds.push(task['project_id'])
      })
      return projectIds.filter(function (el, index, arr) {
        return index === arr.indexOf(el)
      })
    }
  },
  methods: {
    getTasks () {
      API.getGroupedTasks(this.selectedDate.start, this.selectedDate.end)
        .then(response => {
          if (('status' in response.data && response.data.status) || !('status' in response.data)) {
            this.tasks = response.data.tasks
            this.dialogMessage = 'У вас есть незавершенные задачи, они не будут экспортированы:<br>' +
              response.data.not_closed_tasks.replace(/\n/, '<br>')
            this.haveNotClosedTask = response.data.not_closed_tasks !== ''

            this.getProjects()
          }
        })
        .catch(error => {
          console.log(['getTasks error', error])
        })
    },
    getProjects () {
      API.getProjects(this.projectIds)
        .then(response => {
          if (('status' in response.data && response.data.status) || !('status' in response.data)) {
            this.projects = response.data.projects
            this.groupTasksRecompute()
          }
        })
        .catch(error => {
          console.log(['getProjects error', error])
        })
    },
    getTrackers () {
      API.getTrackers()
        .then(response => {
          if (('status' in response.data && response.data.status) || !('status' in response.data)) {
            this.trackers = response.data.trackers
            for (var j = 0; j < this.trackers.length; j++) {
              this.trackerTasks[this.trackers[j]['id']] = {}
            }
            this.groupTasksRecompute()
          }
        })
        .catch(error => {
          console.log(['getTrackers error', error])
        })
    },
    convertToHours: function (timeString) {
      if (!timeString) {
        var currentDate = new Date()
        return currentDate.getHours() + currentDate.getMinutes() / 60
      } else {
        var times = timeString.split(':')
        return parseInt(times[0]) + parseInt(times[1]) / 60
      }
    },
    linkProject: function (trackerId, projectId) {
      for (var i = 0; i < this.trackers.length; i++) {
        if (trackerId === this.trackers[i]['id']) {
          this.currentTracker = this.trackers[i]
          break
        }
      }
      this.currentProject = projectId
      if (this.projects[projectId]['tracker_projects'][trackerId] !== undefined &&
        this.projects[projectId]['tracker_projects'][trackerId]['external_project_id'] > 0
      ) {
        this.linkToProject = {
          value: this.projects[projectId]['tracker_projects'][trackerId]['external_project_id'],
          label: this.projects[projectId]['tracker_projects'][trackerId]['external_project_title']
        }
      } else {
        this.linkToProject = null
      }
      this.getTrackerProjects(trackerId)
    },
    closeLinkModal: function () {
      this.showLink = false
    },
    showLinkModal: function () {
      if (this.currentTrackerProjects.length > 0) {
        this.showLink = true
      } else {
        this.alert('Список проектов пуст - трекер недоступен, либо не указаны доступы к нему в настройках.')
      }
    },
    saveLinkProject: function () {
      API.linkProject(this.currentProject, this.currentTracker.id, this.linkToProject)
        .then(response => {
          if (('status' in response.data && response.data.status) || !('status' in response.data)) {
            this.getProjects()
            this.closeLinkModal()
          }
        })
        .catch(error => {
          console.log(['linkProject error', error])
        })
    },
    getTrackerProjects: function (trackerId) {
      if (this.trackerProjects[trackerId] === undefined && this.trackersById[trackerId]['external_user_id'] !== null) {
        API.getTrackerProjects(trackerId)
          .then(response => {
            if (('status' in response.data && response.data.status) || !('status' in response.data)) {
              this.trackerProjects[trackerId] = response.data.projects
              this.currentTrackerProjects = this.trackerProjects[trackerId]
              this.showLinkModal()
            }
          })
          .catch(error => {
            console.log(['getTrackerProjects error', error])
          })
      } else {
        this.currentTrackerProjects = this.trackerProjects[trackerId]
        this.showLinkModal()
      }
    },
    getTrackerTask: function (trackerId, externalTaskId) {
      if (this.trackersById[trackerId]['external_user_id'] !== null) {
        this.loadingTaskCount++
        API.getTrackerTask(trackerId, externalTaskId)
          .then(response => {
            if (response !== undefined && (('status' in response.data && response.data.status) || !('status' in response.data))) {
              this.trackerTasks[trackerId][externalTaskId] = response.data.task
              if (response.data.jira && response.data.jira.tracker_id > 0 && response.data.jira.task) {
                this.trackerTasks[response.data.jira.tracker_id][externalTaskId] = response.data.jira.task
              }
            } else {
              this.trackerTasks[trackerId][externalTaskId] = false
            }
            this.loadingTaskCount--
            if (this.loadingTaskCount === 0) {
              this.exportDisabled = false
            }
            this.groupTasksRecompute()
          })
          .catch(error => {
            console.log(['getTrackerTask error', error])
            this.trackerTasks[trackerId][externalTaskId] = false
            this.loadingTaskCount--
            if (this.loadingTaskCount === 0) {
              this.exportDisabled = false
            }
            this.groupTasksRecompute()
          })
      } else {
        this.trackerTasks[trackerId][externalTaskId] = false
      }
    },
    exportTasks: function () {
      if (!confirm('Вы действительно хотите выгрузить часы?')) {
        return
      }
      this.exportDisabled = true

      var dates = Object.keys(this.groupedTasks)
      for (var i = 0; i < dates.length; i++) {
        for (var j = 0; j < this.groupedTasks[dates[i]].tasks.length; j++) {
          var task = this.groupedTasks[dates[i]].tasks[j]

          var exportTask = {
            id: task['id'],
            tracker_id: null,
            date: task['date'],
            name: task['name'],
            hours: task.delta,
            comment: task.description,
            project_id: 0,
            external_id: task.task_id,
            external_name: task.external_name !== undefined ? task.external_name : ''
          }

          for (var k = 0; k < task.trackers.length; k++) {
            var needExport = this.getTaskNeedExport(task['date'], j, task.trackers[k].id)
            if (needExport === true && (task.trackers[k].status === 'linked' || task.trackers[k].status === 'warning' || task.trackers[k].status === 'fatal')) {
              exportTask.tracker_id = task.trackers[k].id
              if (task.trackers[k].type === 'jira') {
                exportTask.external_id = this.trackerTasks[exportTask.tracker_id][task.task_id]['id']
              } else {
                exportTask.project_id = this.projects[task.project_id]['tracker_projects'][exportTask.tracker_id]['external_project_id']
              }

              this.exportingTaskCount++

              this.exportOneTask(exportTask, j, exportTask.tracker_id)
            }
          }
        }
      }
      this.exportDisabled = false
    },
    exportOneTask: function (exportTask, j, trackerId) {
      API.exportTask(exportTask)
        .then(response => {
          if (response !== undefined && ('status' in response.data && response.data.status)) {
            this.setTaskExportStatus(exportTask.date, j, trackerId, true)
          } else {
            if ('export_result' in response.data) {
              if (response.data.export_result === undefined) {
                this.alert('Ошибка экспорта по задаче ' + exportTask.external_id)
              } else if (response.data.export_result === 'exist') {
                this.alert('Задача ' + exportTask.external_id + ' уже экспортирована, пропускаю')
              } else if (response.data.export_result === 'partial') {
                this.alert('Экспорт задачи ' + exportTask.external_id + 'невозможен: на трекере лишнее время, добаленное в обход системы. Система пока не умеет разрешать такие ситуации, проверьте вручную')
              } else if (response.data.export_result === response.data.message) {
                // внешняя ошибка от трекера
                this.setTaskExportStatus(exportTask.date, j, trackerId, false)
                this.setTaskTrackerValue(exportTask.date, j, trackerId, 'statusMessage', response.data.message)
              }
            }
            this.setTaskExportStatus(exportTask.date, j, trackerId, false)
          }
          this.exportingTaskCount--
          this.groupTasksRecompute()
        })
        .catch(error => {
          console.log(['exportTask error', error])
          this.setTaskExportStatus(exportTask.date, j, trackerId, false)

          this.exportingTaskCount--
          this.groupTasksRecompute()
        })
    },
    setTaskExportStatus: function (date, key, tracker, status) {
      return this.setTaskTrackerValue(date, key, tracker, 'status', status)
    },
    getTaskExportStatus: function (date, key, tracker) {
      return this.getTaskTrackerValue(date, key, tracker, 'status')
    },
    getTaskNeedExport (date, key, tracker) {
      return this.getTaskTrackerValue(date, key, tracker, 'needExport')
    },
    setTaskNeedExport: function (date, key, tracker, needExport) {
      return this.setTaskTrackerValue(date, key, tracker, 'needExport', needExport)
    },
    getTaskTrackerValue: function (date, key, tracker, codeValue) {
      if (this.taskTrackerData[date] === undefined) {
        return null
      }
      if (this.taskTrackerData[date][key] === undefined) {
        return null
      }
      if (this.taskTrackerData[date][key][tracker] === undefined) {
        return null
      }
      if (this.taskTrackerData[date][key][tracker][codeValue] === undefined) {
        return null
      }
      return this.taskTrackerData[date][key][tracker][codeValue]
    },
    setTaskTrackerValue: function (date, key, tracker, codeValue, value) {
      if (this.taskTrackerData[date] === undefined) {
        this.taskTrackerData[date] = {}
      }
      if (this.taskTrackerData[date][key] === undefined) {
        this.taskTrackerData[date][key] = {}
      }
      if (this.taskTrackerData[date][key][tracker] === undefined) {
        this.taskTrackerData[date][key][tracker] = {}
      }
      this.taskTrackerData[date][key][tracker][codeValue] = value
    },
    groupTasksRecompute: function () {
      this.$recompute('groupedTasks')
    },
    changeTrackerChecked: function (title, date) {
      var needCheckTracker = this.trackersSummary[title]['allChecked']

      var dates = Object.keys(this.groupedTasks)
      if (date) {
        dates = [date]
        needCheckTracker = this.trackersSummary[title][date]['allChecked']
      }

      for (var i = 0; i < dates.length; i++) {
        for (var taskKey = 0; taskKey < this.groupedTasks[dates[i]].tasks.length; taskKey++) {
          var task = this.groupedTasks[dates[i]].tasks[taskKey]
          for (var j = 0; j < this.groupedTasks[dates[i]].tasks[taskKey].trackers.length; j++) {
            var tracker = this.groupedTasks[dates[i]].tasks[taskKey].trackers[j]
            if (tracker.title === title && !tracker.disabled) {
              this.setTaskNeedExport(task['date'], taskKey, tracker.id, needCheckTracker)
            }
          }
        }
      }
      this.$recompute('groupedTasks')
      this.$recompute('trackersSummary')
    },
    alert (message) {
      this.alertMessage = message
      this.showAlert = true
    }
  },
  components: {
    Modal
  },
  created () {
    if (this.initialDate !== undefined) {
      this.selectedDate = this.initialDate
    }
    this.getTasks()
    this.getTrackers()
  }
}
</script>

<style>
  .calendar-root .input-date{
    margin: 0 auto;
  }
  .task-group{
    margin-top: 20px !important;
  }
  .task-group-date .md-list-item-content{
    font-weight: bold;
  }
  .md-list-item{
    z-index: 0;
  }
  .minimal-input input, .minimal-input textarea{
    font-size: 14px !important;
  }
  .minimal-input .md-field{
    margin: 0;
    padding: 0;
    min-height: 25px;
  }
  .tracker-badge{
    margin: 3px;
    display: flex;
    justify-content: center;
    background-color: lightgrey;
    border-radius: 3px;
    cursor: pointer;
  }
  .tracker-badge:hover{
    text-decoration: none;
  }
  .linked .tracker-badge{
    background-color: cornflowerblue;
  }
  .error .tracker-badge{
    background-color: tomato;
  }
  .exported .tracker-badge{
    background-color: lime;
  }
  .fatal .tracker-badge{
    background-color: black;
    color: white !important;
  }
  .warning .tracker-badge{
    background-color: orange;
  }
  .md-input.linked{
    color: green;
    -webkit-text-fill-color: green !important;
  }
  .md-input.error{
    color: red;
    -webkit-text-fill-color: red !important;
  }
  .tracker-checkbox {
    float: right !important;
    margin: 0 5px !important;
  }
  .tracker-checkbox .md-checkbox-container{
    height: 18px !important;
    width: 18px !important;
    min-width: 18px !important;
  }
  .tracker-checkbox .md-checkbox-container:after{
    width: 5px !important;
    height: 12px !important;
  }
  .tracker-checkbox.md-checkbox .md-checkbox-container:before {
    height: 18px !important;
    width: 18px !important;
  }
  .tracker-checkbox:first {
    top: 1px !important;
  }
  .column-task-number {
    max-width: 130px;
    width: 130px;
  }
  .column-task-time {
    max-width: 110px;
    width: 110px;
  }
  .column-task-name {
    max-width: 250px;
    width: 250px;
  }
  .column-task-trackers {
    min-width: 150px;
    width: 150px;
  }
  .column-task-time input, .column-task-number input{
    width: 100%;
  }
  .column-task-date {
    max-width: 130px;
    width: 130px;
  }
  .md-table-cell-container span:first-child .tracker-checkbox{
    margin-top: 3px !important;
  }
  .tracker-durations{
    width: 160px;
    margin-left: calc(100% - 160px);
  }
  .tracker-durations .md-list-item-content {
    font-size: 12px !important;
    padding: 0 !important;
    margin: 0 20px !important;
    min-height: 20px !important;
  }
  .tracker-check-all {
    margin: 0 !important;
    top: 5px !important;
    height: 26px !important;
  }
</style>
