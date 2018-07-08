// TaskItem.vue
<template>
  <div class="row">
    <div class="task-start-time">{{task.start}}</div>
    <div class="task-end-time">{{task.end}}</div>
    <div class="task-name">{{task.name}}</div>
    <div class="task-category">{{task.category}}</div>
    <div class="task-duration">{{task.duration}}</div>
    <div class="task-tags">
      <div class="task-tag" v-for="tag in task.tags" :key="tag.id">
        {{ tag.name }}
      </div>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    task: {
      type: Object,
      required: true
    }
  }
}
</script>
