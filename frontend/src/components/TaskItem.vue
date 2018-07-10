// TaskItem.vue
<template>
  <div class="row">
    <div class="task-col task-start-time">{{task.start_time}}</div>
    <div class="task-col task-end-time">{{task.end_time}}</div>
    <div class="task-col task-name">{{task.name}}</div>
    <div class="task-col task-description">{{task.description}}</div>
    <div class="task-col task-category">{{task.category}}</div>
    <div class="task-col task-tags">
      <div class="task-tag" v-for="tag in task.tags" :key="tag.id">
        {{ tag }}
      </div>
    </div>
    <div class="task-col task-duration">{{task.delta}}</div>
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

<style>
  .task-col, .task-tag {
    float: left;
    margin-right: 5px;
  }
  .task-duration{
    float: right;
  }
  .task-start-time, .task-end-time{
    width: 45px;
    text-align: left;
    font-weight: bold;
  }
  .task-duration{
    width: 90px;
    text-align: right;
  }
</style>
