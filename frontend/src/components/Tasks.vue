// Tasks.vue
<template>
  <div>
    <div class="md-layout md-gutter md-alignment-top-center">
      <div class="md-layout-item md-large-size-50 md-xlarge-size-50 md-medium-size-70 md-small-size-100 taskItems" v-if="tasks.length">
        <bar-chart v-if="chartData.values.length" :chart-data="chartData.values" :labels="chartData.labels"/>
        <template
          v-for="taskGroup in groupedTasks.dates"
        >
          <md-list :key="taskGroup.date" class="task-group">
            <md-list-item class="task-group-date">
              {{taskGroup.date}}
            </md-list-item>
            <TaskItem
              v-for="task in taskGroup.tasks"
              :edit="true"
              :key="task.id"
              :task="task"
              @edit="editForm(arguments[0])"
              @stop="stopTask(arguments[0])"
              @resume="resumeTask(arguments[0])"
            />
            <md-list-item class="task-duration-list-item">
              {{taskGroup.duration}}
            </md-list-item>
          </md-list>
        </template>
        <horizontal-bar-chart :chart-data="chartActivities.values" :labels="chartActivities.labels" :labelsWidth="labelWidth"/>
        <horizontal-bar-chart :chart-data="chartCategories.values" :labels="chartCategories.labels" :labelsWidth="labelWidth"/>
        <horizontal-bar-chart :chart-data="chartTags.values" :labels="chartTags.labels" :labelsWidth="labelWidth"/>
      </div>
    </div>
    <modal :show="show" @close="close">
      <div class="modal-header">

      </div>
      <div class="modal-body">
        <div class="md-layout md-gutter">
          <input type="hidden" v-model="editTask.id" name=id>
          <div class="md-layout-item md-size-40">
            <md-field class="masked-input">
              <masked-input v-model="editTask.date" mask="11.11.1111" placeholder="дата" />
            </md-field>
          </div>
          <div class="md-layout-item md-size-30">
            <md-field class="masked-input">
              <masked-input v-model="editTask.start_time" mask="11:11" placeholder="начало" />
            </md-field>
          </div>
          <div class="md-layout-item md-size-30">
            <md-field class="masked-input">
              <masked-input v-model="editTask.end_time" mask="11:11" placeholder="окончание" />
            </md-field>
          </div>
        </div>
        <md-field>
          <label>задача</label>
          <md-input v-model="editTaskActivity"></md-input>
        </md-field>
        <md-field>
          <label>комментарий</label>
          <md-textarea v-model="editTask.description" md-autogrow></md-textarea>
        </md-field>
        <md-field>
          <label>теги</label>
          <md-input v-model="editTaskTags"></md-input>
        </md-field>
      </div>
      <div class="modal-footer text-right">
        <md-button class="md-primary" @click="deleteTask()">удалить</md-button>
        <md-button class="md-primary" @click="closeModal()">отмена</md-button>
        <md-button class="md-accent" @click="saveTask()">сохранить</md-button>
      </div>
    </modal>
  </div>
</template>

<script>
import TaskItem from './TaskItem.vue'
import BarChart from './BarChart.vue'
import Modal from './Modal.vue'
import {formatLabel, formatDate} from './helpers.js'
import HorizontalBarChart from './HorizontalBarChart.vue'
import API from './api.js'
import MaskedInput from 'vue-masked-input'

export default {
  data () {
    return {
      tasks: [],
      selectedDate: {
        start: new Date(),
        end: new Date()
      },
      showNewPostModal: false,
      editTask: {},
      show: false,
      labelWidth: 200
    }
  },
  props: {
    initialDate: {
      type: Object
    }
  },
  computed: {
    groupedTasks: function () {
      var groupedTasks = {'dates': {}, 'activities': {}, 'categories': {}, 'tags': {}}
      this.tasks.forEach(function (task, i) {
        // дни
        if (groupedTasks['dates'][task['date']] === undefined) {
          groupedTasks['dates'][task['date']] = {duration: 0, tasks: [], date: task['date']}
        }
        groupedTasks['dates'][task['date']]['tasks'].push(task)
        groupedTasks['dates'][task['date']]['duration'] += task['delta']

        // задачи
        if (groupedTasks['activities'][task['activity_id']] === undefined) {
          groupedTasks['activities'][task['activity_id']] = {duration: 0, name: task['name']}
        }
        groupedTasks['activities'][task['activity_id']]['duration'] += task['delta']

        // проекты
        if (groupedTasks['categories'][task['category']] === undefined) {
          groupedTasks['categories'][task['category']] = {duration: 0, name: task['category']}
        }
        groupedTasks['categories'][task['category']]['duration'] += task['delta']

        // теги
        task.tags.forEach(function (tag, j) {
          if (groupedTasks['tags'][tag] === undefined) {
            groupedTasks['tags'][tag] = {duration: 0, name: tag}
          }
          groupedTasks['tags'][tag]['duration'] += task['delta']
          groupedTasks['tags'][tag]['duration'] = Math.round(groupedTasks['tags'][tag]['duration'] * 100) / 100
        })

        // со сложением вместе округление работать не хочет
        groupedTasks['dates'][task['date']]['duration'] = Math.round(groupedTasks['dates'][task['date']]['duration'] * 100) / 100
        groupedTasks['activities'][task['activity_id']]['duration'] = Math.round(groupedTasks['activities'][task['activity_id']]['duration'] * 100) / 100
        groupedTasks['categories'][task['category']]['duration'] = Math.round(groupedTasks['categories'][task['category']]['duration'] * 100) / 100
      })

      return groupedTasks
    },
    chartData: function () {
      var labels = []
      var values = []

      if (this.selectedDate.start.getTime() !== this.selectedDate.end.getTime()) {
        var current = new Date(this.selectedDate.start)
        while (current <= this.selectedDate.end) {
          var formattedCurrent = formatDate(current)
          labels.push(formatDate(current, true))

          if (this.groupedTasks['dates'][formattedCurrent] !== undefined) {
            values.push(this.groupedTasks['dates'][formattedCurrent]['duration'])
          } else {
            values.push(0)
          }
          current.setDate(current.getDate() + 1)
        }
      } else {
        // группировка по часам, если отображаются задачи за 1 день
        var tasksCount = this.tasks.length
        var currentTask = 0
        var taskStart, taskEnd
        var hour = 5

        for (var i = 0; i < 24; i++) {
          hour = i + 5
          if (hour > 23) {
            hour -= 24
          }
          labels.push(hour)
          values.push(0)

          while (currentTask < tasksCount) {
            taskStart = this.convertToHours(this.tasks[currentTask].start_time)
            taskEnd = this.convertToHours(this.tasks[currentTask].end_time)

            if (taskStart >= (hour + 1)) {
              break
            } else if (taskStart >= hour && taskEnd <= (hour + 1)) {
              values[i] += taskEnd - taskStart
              currentTask++
            } else if (taskStart <= hour && taskEnd >= (hour + 1)) {
              values[i] += 1
              break
            } else if (taskStart >= hour && taskEnd >= (hour + 1)) {
              values[i] += hour + 1 - taskStart
              break
            } else if (taskStart <= hour && taskEnd <= (hour + 1)) {
              values[i] += taskEnd - hour
              currentTask++
            }
          }
          values[i] = Math.round(values[i] * 100) / 100
        }
      }
      return {labels: labels, values: values}
    },
    chartActivities: function () {
      var labels = []
      var values = []
      var tmpArr = []
      var cnt = 0
      var maxLength = this.labelWidth / 7

      for (var i in this.groupedTasks.activities) {
        tmpArr[cnt] = this.groupedTasks.activities[i]
        cnt++
      }

      tmpArr = tmpArr.sort(function (a, b) {
        return a.duration === b.duration ? 0 : +(a.duration < b.duration) || -1
      })

      tmpArr.forEach(function (item, i) {
        labels.push(formatLabel(item['name'], maxLength))
        values.push(item['duration'])
      })
      return {labels: labels, values: values}
    },
    chartCategories: function () {
      var labels = []
      var values = []
      var tmpArr = []
      var cnt = 0
      var maxLength = this.labelWidth / 5

      for (var i in this.groupedTasks.categories) {
        tmpArr[cnt] = this.groupedTasks.categories[i]
        cnt++
      }

      tmpArr = tmpArr.sort(function (a, b) {
        return a.duration === b.duration ? 0 : +(a.duration < b.duration) || -1
      })

      tmpArr.forEach(function (item, i) {
        labels.push(formatLabel(item['name'], maxLength))
        values.push(item['duration'])
      })

      return {labels: labels, values: values}
    },
    chartTags: function () {
      var labels = []
      var values = []
      var tmpArr = []
      var cnt = 0
      var maxLength = this.labelWidth / 5

      for (var i in this.groupedTasks.tags) {
        tmpArr[cnt] = this.groupedTasks.tags[i]
        cnt++
      }

      tmpArr = tmpArr.sort(function (a, b) {
        return a.duration === b.duration ? 0 : +(a.duration < b.duration) || -1
      })

      tmpArr.forEach(function (item, i) {
        labels.push(formatLabel(item['name'], maxLength))
        values.push(item['duration'])
      })

      return {labels: labels, values: values}
    },
    editTaskActivity: {
      get: function () {
        if (this.editTask.name === undefined) {
          return ''
        }

        var str = this.editTask.name
        if (this.editTask.category) {
          str += '@' + this.editTask.category
        }
        return str
      },
      set: function (value) {
        var data = value.split('@', 2)
        this.editTask.name = data[0]
        if (data[1] !== undefined) {
          this.editTask.category = data[1]
        } else {
          this.editTask.category = ''
        }
      }
    },
    editTaskTags: {
      get: function () {
        if (this.editTask.tags === undefined) {
          return ''
        }
        return this.editTask.tags.join(', ')
      },
      set: function (value) {
        var data = value.replace(/,\s*/g, ', ').split(', ')
        this.editTask.tags = data
      }
    }
  },
  methods: {
    getTasks () {
      API.getTasks(this.selectedDate.start, this.selectedDate.end)
        .then(response => {
          this.tasks = response.data.tasks
        })
        .catch(error => {
          console.log(['getTasks error', error])
        })
    },
    close: function () {
      this.show = false
    },
    editForm: function (task) {
      this.editTask = Object.assign({}, task)
      this.show = true
    },
    stopTask: function (task) {
      API.stopTask(task.id)
        .then(response => {
          this.$emit('update')
        })
        .catch(error => {
          console.log(['stopTask error', error])
        })
    },
    resumeTask: function (task) {
      API.resumeTask(task.id)
        .then(response => {
          this.$emit('update')
        })
        .catch(error => {
          console.log(['resumeTask error', error])
        })
    },
    deleteTask: function () {
      if (confirm('Вы действительно хотите удалить запись?')) {
        API.deleteTask(this.editTask.id)
          .then(response => {
            this.$emit('update')
            this.closeModal()
          })
          .catch(error => {
            console.log(['deleteTask error', error])
          })
      }
    },
    saveTask: function () {
      API.updateTask(this.editTask)
        .then(response => {
          if ('message' in response.data && response.data.message) {
            alert(response.data.message)
          }
          if (('status' in response.data && response.data.status) || !('status' in response.data)) {
            this.$emit('update')
            this.closeModal()
          }
        })
        .catch(error => {
          console.log(['savePost error', error])
        })
    },
    closeModal: function () {
      this.show = false
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
    refreshDate: function () {
      this.selectedDate = {
        start: new Date(),
        end: new Date()
      }
    }
  },
  components: {
    HorizontalBarChart, TaskItem, BarChart, Modal, MaskedInput
  },
  created () {
    if (this.initialDate !== undefined) {
      this.selectedDate = this.initialDate
    }
    this.getTasks()
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
  .masked-input input{
    width: 100%;
    background-color: white;
  }
</style>
