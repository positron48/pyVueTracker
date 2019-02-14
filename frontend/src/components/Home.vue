// Home.vue
<template>
  <div>
    <div class="md-layout md-gutter md-alignment-top-center">
      <div class="md-layout-item md-large-size-50 md-xlarge-size-50 md-medium-size-70 md-small-size-100">
      </div>
    </div>

    <TaskStop v-on:stop-task="onStopTask" ref="taskStop"/>
    <TaskAdd v-on:add-task="onAddTask" ref="taskAdd" :projects="userProjects" :tags="userTags"/>
    <Tasks ref="tasks" @update="onEditTask()"/>
  </div>
</template>

<script>
import Tasks from './Tasks.vue'
import TaskAdd from './TaskAdd.vue'
import TaskStop from './TaskStop.vue'
import {API} from './api.js'

export default {
  data () {
    return {
      timer: null,

      userProjects: [],
      userTags: []
    }
  },
  methods: {
    refreshData () {
      this.$refs.taskStop.getCurrentTask()
      this.$refs.taskAdd.getCompletitions()
      this.$refs.tasks.refreshDate()
      this.$refs.tasks.getTasks()
    },
    onStopTask () {
      this.refreshData()
      this.getUserProjects()
      this.getUserTags()
    },
    onAddTask () {
      this.refreshData()
      this.getUserProjects()
      this.getUserTags()
    },
    onEditTask () {
      this.refreshData()
      this.getUserProjects()
      this.getUserTags()
    },
    getUserProjects () {
      API.getUserProjects()
        .then(response => {
          this.userProjects = response.data.projects
        })
        .catch(error => {
          console.log(['getUserProjects error', error])
        })
    },
    getUserTags () {
      API.getUserTags()
        .then(response => {
          this.userTags = response.data.tags
        })
        .catch(error => {
          console.log(['getUserTags error', error])
        })
    }
  },
  components: {
    Tasks, TaskAdd, TaskStop
  },
  mounted () {
    this.timer = setInterval(this.refreshData, 60000)
    this.getUserProjects()
    this.getUserTags()
  },
  destroyed () {
    clearInterval(this.timer)
  }
}
</script>
