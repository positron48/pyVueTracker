// Tasks.vue
<template>
  <div class="md-layout md-gutter md-alignment-top-center">
    <div class="md-layout-item md-size-50" v-if="useDatePicker">
      <vue-rangedate-picker
        @selected="onDateSelected"
        ref="rangeDatePicker"
        i18n="EN"
        format="DD.MM.YYYY"
      >
      </vue-rangedate-picker>
    </div>
    <ul class="md-layout-item md-size-100"  v-if="tasks.length">
      <TaskItem
        v-for="task in tasks"
        :key="task.id"
        :task="task"
      />
    </ul>
  </div>
</template>

<script>
import TaskItem from './TaskItem.vue'
import VueRangedatePicker from 'vue-rangedate-picker'
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
    useDatePicker: {
      type: Boolean
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
    },
    onDateSelected: function (daterange) {
      this.selectedDate = daterange
      this.getTasks()
    }
  },
  components: {
    TaskItem, VueRangedatePicker
  },
  created () {
    this.getTasks()
  },
  mounted () {
    if (this.useDatePicker) {
      this.$refs.rangeDatePicker.dateRange = this.selectedDate
    }
  }
}
</script>

<style>
  .calendar-root .input-date{
    margin: 0 auto;
  }
</style>
