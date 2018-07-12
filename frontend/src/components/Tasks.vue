// Tasks.vue
<template>
  <div>
    <div class="md-layout md-gutter md-alignment-top-center">
      <div class="md-layout-item md-size-50 taskItems"  v-if="tasks.length">
        <template
          v-for="taskGroup in groupedTasks"
        >
          <md-list :key="taskGroup.date" class="task-group">
            <md-list-item class="task-group-date">
              {{taskGroup.date}}
            </md-list-item>
            <TaskItem
              v-for="task in taskGroup.tasks"
              :key="task.id"
              :task="task"
            />
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
import TaskItem from './TaskItem.vue'
import axios from 'axios'

export default {
  data () {
    return {
      tasks: [],
      selectedDate: {
        start: new Date(),
        end: new Date()
      }
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
        if (groupedTasks[task['date']] === undefined) {
          groupedTasks[task['date']] = {duration: 0, tasks: [], date: task['date']}
        }
        groupedTasks[task['date']]['tasks'].push(task)
        groupedTasks[task['date']]['duration'] += task['delta']

        // со сложением вместе округление работать не хочет
        groupedTasks[task['date']]['duration'] = Math.round(groupedTasks[task['date']]['duration'] * 100) / 100
      })
      return groupedTasks
    }
  },
  methods: {
    getTasks () {
      var formattedStart = ('0' + this.selectedDate.start.getDate()).slice(-2) +
        '.' + ('0' + (this.selectedDate.start.getMonth() + 1)).slice(-2) +
        '.' + this.selectedDate.start.getFullYear()
      var formattedEnd = ('0' + this.selectedDate.end.getDate()).slice(-2) +
        '.' + ('0' + (this.selectedDate.end.getMonth() + 1)).slice(-2) +
        '.' + this.selectedDate.end.getFullYear()

      const path = `http://localhost:5000/api/tasks?interval=` + formattedStart + '-' + formattedEnd
      axios.get(path)
        .then(response => {
          this.tasks = response.data.tasks
        })
        .catch(error => {
          console.log(error)
        })
    }
  },
  components: {
    TaskItem
  },
  created () {
    if (this.initialDate !== undefined) {
      this.selectedDate = this.initialDate
    }
    this.getTasks()
    console.log(this.selectedDate)
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
  .task-duration-list-item .md-list-item-content{
    width: 90px;
    text-align: right;
    float: right;
    margin-right: 5px;
    font-weight: bold;
  }
</style>
