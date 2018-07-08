// Tasks.vue
<template>
  <div class="row">
    <ul v-if="tasks.length">
      <TaskItem
        v-for="task in tasks"
        :key="task.id"
        :task="task"
      />
    </ul>
    <p v-else>
      Nothing
    </p>
  </div>
</template>

<script>
import TaskItem from './TaskItem.vue'

export default {
  data () {
    return {
      tasks: [
        {id: 1, start: '10:00', end: '10:30', duration: '30 minutes', category: 'multisite', tags: [{id: 0, name: 'support'}], name: '12345 test1'},
        {id: 2, start: '10:30', end: '11:30', duration: '1 hour', category: 'invoz', tags: [{id: 0, name: 'support'}, {id: 1, name: 'learning'}], name: 'support'},
        {id: 3, start: '11:30', end: '12:15', duration: '45 minutes', category: 'multisite', tags: [{id: 0, name: 'support'}], name: '123456'}
      ]
    }
  },
  components: {
    TaskItem
  }
}
</script>
