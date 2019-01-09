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
                    <md-table-head>Номер задачи</md-table-head>
                    <md-table-head>Комментарий</md-table-head>
                    <md-table-head>Проект</md-table-head>
                    <md-table-head>Время</md-table-head>
                  </md-table-row>

                  <GroupedTaskItem
                    v-for="task in taskGroup.tasks"
                    :key="task.id"
                    :task="task"
                    @linkProject="linkProject(arguments[0], arguments[1])"
                  />

                </md-table>
              <md-list-item class="task-duration-list-item">
                  {{taskGroup.duration}}
                </md-list-item>
              </md-list>

        </template>
      </div>
    </div>

    <modal :show="showLink">
      <div class="modal-header">
        <h2>Укажите проект в {{currentTracker.title}}</h2>
      </div>
      <div class="modal-body">
        <input type="hidden" v-model="currentTracker.id" name="trackerId">
        <input type="hidden" v-model="currentProject" name="projectId">
        <v-select v-model="linkToProject" :options="trackerProjects[currentTracker.id]"/>
      </div>
      <div class="modal-footer text-right">
        <md-button class="md-primary" @click="closeLinkModal">отмена</md-button>
        <md-button class="md-accent" @click="saveLinkProject">сохранить</md-button>
      </div>
    </modal>
  </div>
</template>

<script>
import GroupedTaskItem from './GroupedTaskItem.vue'
import API from './api.js'
import Modal from './Modal.vue'

export default {
  data () {
    return {
      tasks: [],
      projects: [],
      trackers: [],
      selectedDate: {
        start: new Date(),
        end: new Date()
      },
      show: false,
      labelWidth: 200,

      currentTracker: [],
      currentProject: null,
      showLink: false,
      linkToProject: null,
      trackerProjects: {}
    }
  },
  props: {
    initialDate: {
      type: Object
    }
  },
  computed: {
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
          var tracker = this.trackers[j]
          task['trackers'].push({
            id: tracker['id'],
            type: tracker['type'],
            title: tracker['title'],
            status: (this.projects[task['project_id']] !== undefined &&
              this.projects[task['project_id']]['tracker_projects'][tracker['id']] !== undefined) ? 'linked' : ''
          })
        }

        groupedTasks[task['date']]['tasks'].push(task)
        groupedTasks[task['date']]['duration'] += task['delta']

        // со сложением вместе округление работать не хочет
        groupedTasks[task['date']]['duration'] = Math.round(groupedTasks[task['date']]['duration'] * 100) / 100
      }
      console.log(groupedTasks)
      return groupedTasks
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
            this.$forceUpdate()
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
      console.log([trackerId, this.trackers[trackerId]])
      for (var i = 0; i < this.trackers.length; i++) {
        if (trackerId === this.trackers[i]['id']) {
          this.currentTracker = this.trackers[i]
          break
        }
      }
      this.currentProject = projectId
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

    },
    getTrackerProjects: function (trackerId) {
      if (this.trackerProjects[trackerId] === undefined) {
        API.getTrackerProjects(trackerId)
        .then(response => {
          if (('status' in response.data && response.data.status) || !('status' in response.data)) {
            this.trackerProjects[trackerId] = response.data.projects
          }
        })
        .catch(error => {
          console.log(['getTrackerProjects error', error])
        })
      }
    }
  },
  components: {
    GroupedTaskItem, Modal
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
</style>
