// GroupedTasks.vue
<template>
  <div>
    <div class="md-layout md-gutter md-alignment-top-center">
      <div class="md-layout-item  md-large-size-70 md-xlarge-size-60 md-medium-size-90 md-small-size-100 taskItems minimal-input" v-if="tasks.length">
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
                    <md-table-head>Номер задачи</md-table-head>
                    <md-table-head>Комментарий</md-table-head>
                    <md-table-head>Проект</md-table-head>
                    <md-table-head>Время</md-table-head>
                  </md-table-row>

                  <GroupedTaskItem
                    v-for="task in taskGroup.tasks"
                    :key="task.id"
                    :task="task"
                  />

                </md-table>
              <md-list-item class="task-duration-list-item">
                  {{taskGroup.duration}}
                </md-list-item>
              </md-list>

        </template>
      </div>
    </div>
  </div>
</template>

<script>
import GroupedTaskItem from './GroupedTaskItem.vue'
import API from './api.js'

export default {
  data () {
    return {
      tasks: [],
      selectedDate: {
        start: new Date(),
        end: new Date()
      },
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
      var groupedTasks = {}
      this.tasks.forEach(function (task, i) {
        // дни
        if (groupedTasks[task['date']] === undefined) {
          groupedTasks[task['date']] = {duration: 0, tasks: [], date: task['date']}
        }
        groupedTasks[task['date']]['tasks'].push(task)
        groupedTasks[task['date']]['duration'] += task['delta']

        // со сложением вместе округление работать не хочет
        groupedTasks[task['date']]['duration'] = Math.round(groupedTasks[task['date']]['duration'] * 100) / 100
      })
      console.log(groupedTasks)
      return groupedTasks
    }
  },
  methods: {
    getTasks () {
      API.getGroupedTasks(this.selectedDate.start, this.selectedDate.end)
        .then(response => {
          this.tasks = response.data.tasks
        })
        .catch(error => {
          console.log(['getTasks error', error])
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
    }
  },
  components: {
    GroupedTaskItem
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
</style>
