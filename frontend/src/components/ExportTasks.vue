// GroupedTasks.vue
<template>
  <div>
    <div class="md-layout md-gutter md-alignment-top-center">
      <div class="md-layout-item  md-medium-size-90 md-small-size-100 taskItems minimal-input" v-if="tasks.length">
        <template
            v-for="taskGroup in groupedTasks"
          >
            <md-list :key="taskGroup.date" class="task-group">
              <md-list-item class="task-group-date">
                {{taskGroup.date}}
              </md-list-item>
                <md-table>
                  <md-table-row>
                    <md-table-head>Дата</md-table-head>
                    <md-table-head>Задача</md-table-head>
                    <md-table-head>
                      Номер задачи
                      <md-tooltip md-direction="top">Номер задачи из редмайна</md-tooltip>
                    </md-table-head>
                    <md-table-head>Комментарий</md-table-head>
                    <md-table-head>
                      Проект
                      <md-tooltip md-direction="top">Название проекта в таймтрекере</md-tooltip>
                    </md-table-head>
                    <md-table-head>Время</md-table-head>
                    <md-table-head>
                      Трекеры
                      <md-tooltip md-direction="top">Список трекеров, привязанных к проекту</md-tooltip>
                    </md-table-head>
                  </md-table-row>

                  <template v-for="task in taskGroup.tasks">
                    <md-table-row :key="task.id">
                      <md-table-cell>
                        <md-field>
                          <label></label>
                          <md-input v-model="task.date"></md-input>
                        </md-field>
                      </md-table-cell>
                      <md-table-cell>
                        <div>{{task.name}}</div>
                      </md-table-cell>
                      <md-table-cell>
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
                      <md-table-cell>
                        <md-field>
                          <label></label>
                          <md-input v-model="task.delta" type="number" min="0" step="0.05"></md-input>
                        </md-field>
                      </md-table-cell>
                      <md-table-cell>
                        <template v-for="tracker in task.trackers">
                          <span v-bind:key="tracker.id + '_' + task.id" :class="tracker.status">
                            <a class="tracker-badge" @click="linkProject(tracker.id, task.project_id)">
                              {{tracker.title}}
                            </a>
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
              </md-list>

        </template>
      </div>
    </div>

    <div class="md-layout md-gutter md-alignment-top-center center" v-if="Object.keys(groupedTasks).length">
      <div class="md-layout-item md-size-50">
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
      exportDisabled: false,
      exportingTaskCount: 0,
      exportStatus: {},

      currentTracker: [],
      currentProject: null,
      showLink: false,
      linkToProject: null,
      trackerProjects: {},
      currentTrackerProjects: []
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
      for (var i = 0; i < this.tasks.length; i++) {
        var task = this.tasks[i]

        // дни
        if (groupedTasks[task['date']] === undefined) {
          groupedTasks[task['date']] = {duration: 0, tasks: [], date: task['date']}
        }
        task['delta'] = parseFloat(task['delta'])

        task['trackers'] = []
        for (var j = 0; j < this.trackers.length; j++) {
          var tracker = {
            id: this.trackers[j]['id'],
            type: this.trackers[j]['type'],
            title: this.trackers[j]['title'],
            status: (this.projects[task['project_id']] !== undefined &&
              this.projects[task['project_id']]['tracker_projects'][this.trackers[j]['id']] !== undefined) ? 'linked' : ''
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
          }

          // todo: status: ?warning? часы за этот день по проекту уже выгружались
          var exportStatus = this.getTaskExportStatus(task['date'], groupedTasks[task['date']].tasks.length, tracker.id)
          if (exportStatus === true) {
            tracker['status'] = 'exported'
            tracker['message'] = 'задача выгружена'
          } else if (exportStatus === false) {
            tracker['status'] = 'fatal'
            tracker['message'] = 'при выгрузке произошла ошибка'
          } else if (
            tracker['status'] === 'linked' &&
            tracker['type'] === 'redmine' &&
            !task['task_id']
          ) {
            tracker['status'] = 'error'
            tracker['message'] = 'не указан номер задачи'
          } else if (
            tracker['status'] === 'linked' &&
            tracker['type'] === 'evo' &&
            (externalTask === false || externalTask === undefined) &&
            task['description'] === ''
          ) {
            tracker['status'] = 'error'
            tracker['message'] = 'не заполнен комментарий'
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
          } else {
            tracker['message'] = tracker['status'] === 'linked'
              ? this.projects[task['project_id']]['tracker_projects'][this.trackers[j]['id']]['external_project_title']
              : 'проект не сопоставлен'
          }
          task['trackers'].push(tracker)
        }

        groupedTasks[task['date']]['tasks'].push(task)
        groupedTasks[task['date']]['duration'] += task['delta']

        // со сложением вместе округление работать не хочет
        groupedTasks[task['date']]['duration'] = Math.round(groupedTasks[task['date']]['duration'] * 100) / 100
      }
      // console.log(groupedTasks)
      return groupedTasks
    }
  },
  computed: {
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
            this.$recompute('groupedTasks')
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
            this.$recompute('groupedTasks')
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
      if (this.projects[projectId]['tracker_projects'][trackerId] !== undefined) {
        this.linkToProject = {
          value: this.projects[projectId]['tracker_projects'][trackerId]['external_project_id'],
          label: this.projects[projectId]['tracker_projects'][trackerId]['external_project_title']
        }
      } else {
        this.linkToProject = null
      }
      this.getTrackerProjects(trackerId)

      this.showLinkModal()
    },
    closeLinkModal: function () {
      this.showLink = false
    },
    showLinkModal: function () {
      this.showLink = true
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
      if (this.trackerProjects[trackerId] === undefined) {
        API.getTrackerProjects(trackerId)
          .then(response => {
            if (('status' in response.data && response.data.status) || !('status' in response.data)) {
              this.trackerProjects[trackerId] = response.data.projects
              this.currentTrackerProjects = this.trackerProjects[trackerId]
            }
          })
          .catch(error => {
            console.log(['getTrackerProjects error', error])
          })
      } else {
        this.currentTrackerProjects = this.trackerProjects[trackerId]
      }
    },
    getTrackerTask: function (trackerId, externalTaskId) {
      API.getTrackerTask(trackerId, externalTaskId)
        .then(response => {
          if (response !== undefined && (('status' in response.data && response.data.status) || !('status' in response.data))) {
            this.trackerTasks[trackerId][externalTaskId] = response.data.task
          } else {
            this.trackerTasks[trackerId][externalTaskId] = false
          }
          this.$recompute('groupedTasks')
        })
        .catch(error => {
          console.log(['getTrackerProjects error', error])
          this.trackerTasks[trackerId][externalTaskId] = false
          this.$recompute('groupedTasks')
        })
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
            tracker_id: null,
            date: task['date'],
            hours: task.delta,
            comment: task.description,
            project_id: 0,
            external_id: task.task_id,
            external_name: task.external_name !== undefined ? task.external_name : ''
          }

          for (var k = 0; k < task.trackers.length; k++) {
            if (task.trackers[k].status === 'linked' || task.trackers[k].status === 'warning') {
              exportTask.tracker_id = task.trackers[k].id
              exportTask.project_id = this.projects[task.project_id]['tracker_projects'][exportTask.tracker_id]['external_project_id']

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
            this.setTaskExportStatus(exportTask.date, j, trackerId, false)
          }
          this.exportingTaskCount--
          this.$recompute('groupedTasks')
        })
        .catch(error => {
          console.log(['exportTask error', error])
          this.setTaskExportStatus(exportTask.date, j, trackerId, false)

          this.exportingTaskCount--
          this.$recompute('groupedTasks')
        })
    },
    setTaskExportStatus: function (date, key, tracker, status) {
      if (this.exportStatus[date] === undefined) {
        this.exportStatus[date] = {}
      }
      if (this.exportStatus[date][key] === undefined) {
        this.exportStatus[date][key] = {}
      }
      this.exportStatus[date][key][tracker] = status
    },
    getTaskExportStatus: function (date, key, tracker) {
      if (this.exportStatus[date] === undefined) {
        return null
      }
      if (this.exportStatus[date][key] === undefined) {
        return null
      }
      if (this.exportStatus[date][key][tracker] === undefined) {
        return null
      }
      return this.exportStatus[date][key][tracker]
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
    margin-top: 20px;
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
</style>
