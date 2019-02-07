// TaskItem.vue
<template>
  <md-list-item>
    <div v-if="edit" class="task-col task-edit" v-on:click="$emit('edit', task)">
      <md-tooltip md-direction="top">Редактировать</md-tooltip>
      <font-awesome-icon icon="edit"/>
    </div>
    <div v-if="edit && task.end_time" class="task-col task-resume" v-on:click="$emit('resume', task)">
      <font-awesome-icon icon="play-circle"/>
      <md-tooltip md-direction="top">Продолжить</md-tooltip>
    </div>
    <div v-if="edit && !task.end_time" class="task-col task-stop" v-on:click="$emit('stop', task)">
      <font-awesome-icon icon="stop-circle"/>
      <md-tooltip md-direction="top">Остановить</md-tooltip>
    </div>
    <div class="task-col task-start-time">{{task.start_time}}</div>
    <div class="task-col task-end-time">{{task.end_time}}</div>
    <div class="task-col task-name">{{task.name}}</div>
    <md-badge class="task-col task-category md-primary md-square" :md-content="task.category" v-if="task.category"/>
    <div class="task-col task-tags">
      <template v-for="tag in task.tags">
        <md-badge class="md-square" :md-content="tag" :key="tag"/>
      </template>
    </div>
    <div class="task-col task-description">{{task.description}}</div>
    <div class="task-col task-duration">{{deltaTime}}</div>
  </md-list-item>
</template>

<script>
import {deltaToHMM} from './helpers.js'
export default {
  computed: {
    deltaTime: function () {
      return deltaToHMM(this.task.delta)
    }
  },
  props: {
    task: {
      type: Object,
      required: true
    },
    edit: false
  }
}
</script>

<style>
  .task-edit, .task-resume, .task-stop{
    cursor: pointer;
  }
  .task-tags{
    display: flex;
  }
  .task-col, .task-tags .md-badge {
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
  .md-list-item-content{
    display: block !important;
    padding-top: 15px !important;
  }
  .task-duration-list-item .md-list-item-content{
    width: 90px;
    text-align: right;
    float: right;
    margin-right: 5px;
    font-weight: bold;
  }
</style>
