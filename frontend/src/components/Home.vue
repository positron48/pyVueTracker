// Home.vue
<template>
  <div>
    <TaskStop v-on:stop-task="refreshData" ref="taskStop"/>
    <TaskAdd v-on:add-task="refreshData" ref="taskAdd"/>
    <Tasks ref="tasks"/>
  </div>
</template>

<script>
import Tasks from './Tasks.vue'
import TaskAdd from './TaskAdd.vue'
import TaskStop from './TaskStop.vue'

export default {
  data () {
    return {}
  },
  methods: {
    refreshData () {
      this.$refs.taskStop.getCurrentTask()
      this.$refs.taskAdd.getCompletitions()
      this.$refs.tasks.getTasks()
    }
  },
  components: {
    Tasks, TaskAdd, TaskStop
  },
  mounted () {
    setInterval(this.refreshData, 60000)
  }
}
</script>
