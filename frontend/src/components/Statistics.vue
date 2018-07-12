// Statistics.vue
<template>
  <div>
    <div class="md-layout md-gutter md-alignment-top-center">
      <div class="md-layout-item md-size-50">
        <vue-rangedate-picker
          @selected="onDateSelected"
          ref="rangeDatePicker"
          i18n="EN"
          format="DD.MM.YYYY"
        >
        </vue-rangedate-picker>
      </div>
    </div>
    <Tasks :initialDate="selectedDate" ref="tasks"/>
  </div>
</template>

<script>
import VueRangedatePicker from 'vue-rangedate-picker'
import Tasks from './Tasks.vue'

export default {
  data () {
    return {
      selectedDate: {
        start: new Date(),
        end: new Date()
      }
    }
  },
  methods: {
    onDateSelected: function (daterange) {
      this.selectedDate = daterange
      this.$refs.tasks.selectedDate = daterange
      this.$refs.tasks.getTasks()
    }
  },
  components: {
    VueRangedatePicker, Tasks
  },
  mounted () {
    this.$refs.rangeDatePicker.dateRange = this.selectedDate
  }
}
</script>
