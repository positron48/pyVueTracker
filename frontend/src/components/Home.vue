// Home.vue
<template>
  <div>
    <TaskStop/>
    <TaskAdd/>
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
  components: {
    Tasks, TaskAdd, TaskStop
  }
}
</script>
