// TaskItem.vue
<template>
  <md-table-row>
    <md-table-cell>
      <md-field>
        <label></label>
        <md-input v-model="task.date"></md-input>
      </md-field>
    </md-table-cell>
    <md-table-cell>
      <div>{{task.name}}</div>
    </md-table-cell>
    <md-table-cell>
      <md-field>
        <label></label>
        <md-input v-model="task.task_id" type="number" min="1"></md-input>
      </md-field>
    </md-table-cell>
    <md-table-cell>
      <md-field>
        <label></label>
        <md-textarea v-model="task.description" md-autogrow></md-textarea>
      </md-field>
    </md-table-cell>
    <md-table-cell>
      <md-field>
        <label></label>
        <md-input v-model="task.category"></md-input>
      </md-field>
    </md-table-cell>
    <md-table-cell>
      <md-field>
        <label></label>
        <md-input v-model="task.delta" type="number" min="0" step="0.05"></md-input>
      </md-field>
    </md-table-cell>
    <md-table-cell>
      <div v-bind:key="tracker.id" v-for="tracker in task.trackers">
        <span :class="tracker.status">
          <a class="tracker-badge" @click="$emit('linkProject', tracker.id, task.project_id)">
            {{tracker.title}}
          </a>
        </span>
      </div>
    </md-table-cell>
  </md-table-row>
</template>

<script>
export default {
  props: {
    task: {
      type: Object,
      required: true
    },
    edit: false
  }
}
</script>

<style scoped>
.minimal-input input, .minimal-input textarea{
  font-size: 14px !important;
}
.minimal-input .md-field{
  margin: 0;
  padding: 0;
  min-height: 25px;
}
.tracker-badge{
  margin: 3px;
  display: flex;
  justify-content: center;
  background-color: lightgrey;
  border-radius: 3px;
  cursor: pointer;
}
.tracker-badge:hover{
  text-decoration: none;
}
.linked .tracker-badge{
  background-color: lime;
}
</style>
