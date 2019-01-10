// Export.vue
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
          :shortcuts="shortcuts"
        >
        </date-picker>
      </div>
    </div>
    <ExportTasks :initialDate="selectedDate" ref="grouped_tasks" @update="refreshData()"/>
  </div>
</template>
uni
<script>
import DatePicker from 'vue2-datepicker'
import ExportTasks from './ExportTasks.vue'

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
      ],
      shortcuts: [
        {
          text: 'сегодня',
          start: new Date(),
          end: new Date()
        },
        {
          text: 'вчера',
          start: new Date(new Date().setDate(new Date().getDate() - 1)),
          end: new Date(new Date().setDate(new Date().getDate() - 1))
        },
        {
          text: 'эта неделя',
          start: new Date(new Date().setDate(new Date().getDate() - (new Date().getDay() || 7) + 1)),
          end: new Date(new Date().setDate(new Date().getDate() - (new Date().getDay() || 7) + 7))
        },
        {
          text: 'прошлая',
          start: new Date(new Date().setDate(new Date().getDate() - (new Date().getDay() || 7) - 6)),
          end: new Date(new Date().setDate(new Date().getDate() - (new Date().getDay() || 7)))
        },
        {
          text: 'месяц',
          start: new Date(new Date().setDate(1)),
          end: new Date(new Date(new Date(new Date().setDate(1)).setMonth(new Date().getMonth() + 1)).setDate(0))
        },
        {
          text: 'прошлый',
          start: new Date(new Date(new Date().setDate(1)).setMonth(new Date().getMonth() - 1)),
          end: new Date(new Date(new Date().setDate(1)).setDate(0))
        }
      ]
    }
  },
  methods: {
    onDateSelected: function (daterange) {
      this.selectedDate.start = daterange[0]
      this.selectedDate.end = daterange[1]
      this.$refs.grouped_tasks.selectedDate = this.selectedDate
      this.refreshData()
    },
    refreshData () {
      this.$refs.grouped_tasks.getTasks()
    }
  },
  components: {
    DatePicker, ExportTasks
  },
  mounted () {
    this.$refs.rangeDatePicker.dateRange = this.selectedDate
  }
}
</script>
