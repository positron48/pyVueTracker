// TaskItem.vue
<template>
  <md-list-item>
    <div class="task-col task-start-time">{{task.start_time}}</div>
    <div class="task-col task-end-time">{{task.end_time}}</div>
    <div class="task-col task-name">{{task.name}}</div>
    <md-badge class="task-col task-category md-primary md-square" :md-content="task.category"/>
    <div class="task-col task-tags">
      <template v-for="tag in task.tags">
        <md-badge class="md-square" :md-content="tag" :key="tag"/>
      </template>
    </div>
    <div class="task-col task-description">{{task.description}}</div>
    <div class="task-col task-duration">{{task.delta}}</div>
  </md-list-item>
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
  .task-start-time, .task-end-time{
    width: 45px;
    text-align: left;
    font-weight: bold;
  }
  .task-duration{
    width: 90px;
    text-align: right;
    float: right;
  }
  .task-description{
    color: #b2b2b2;
    font-size: 14px;
    width: initial;
    white-space: normal;
  }
  .taskItems{
    justify-content: none
  }
  .taskItems .md-list-item-content{
    display: block;
    padding-top: 15px;
  }
</style>
