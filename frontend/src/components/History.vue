// History.vue
<template>
  <div>
    <div class="md-layout md-gutter md-alignment-top-center center">
      <div class="md-layout-item md-size-50">
        <date-picker
          @change="onDateSelected"
          :first-day-of-week="1"
          v-model="time"
          confirm
          ref="rangeDatePicker"
          lang="ru"
          range
          format="DD.MM.YYYY"
        >
        </date-picker>
      </div>
    </div>
    <Tasks :initialDate="selectedDate" ref="tasks" @update="refreshData()"/>
  </div>
</template>

<script>
import DatePicker from 'vue2-datepicker'
import Tasks from './Tasks.vue'

export default {
  data () {
    return {
      selectedDate: {
        start: new Date(),
        end: new Date()
      },
      time: [
        new Date(),
        new Date()
      ]
    }
  },
  methods: {
    onDateSelected: function (daterange) {
      this.selectedDate.start = daterange[0]
      this.selectedDate.end = daterange[1]
      this.$refs.tasks.selectedDate = this.selectedDate
      this.$refs.tasks.getTasks()
    },
    refreshData () {
      this.$refs.tasks.getTasks()
    }
  },
  components: {
    DatePicker, Tasks
  },
  mounted () {
    this.$refs.rangeDatePicker.dateRange = this.selectedDate
  }
}
</script>
