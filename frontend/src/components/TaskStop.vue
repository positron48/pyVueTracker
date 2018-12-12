<template>
  <div v-if="current !== null">
      <form action="" method="post" class="md-layout md-gutter md-alignment-top-center" v-on:submit.prevent="stopTask()">
        <md-card class="md-layout-item md-large-size-50 md-xlarge-size-50 md-medium-size-70 md-small-size-100">
          <md-card-content>
            <div class="md-layout">
              <md-list class="md-layout-item md-size-80">
                <TaskItem
                  :task="current"
                />
              </md-list>
              <div class="md-layout-item md-size-20">
                <md-button type="submit" class="md-primary" style="margin-top: 12px;">Stop</md-button>
              </div>
            </div>
          </md-card-content>
        </md-card>
      </form>
    </div>
</template>

<script>
import TaskItem from './TaskItem.vue'
import axios from 'axios'

export default {
  data () {
    return {
      current: null
    }
  },
  methods: {
    getCurrentTask () {
      const path = this.$baseUrl + `/current`
      axios.get(path)
        .then(response => {
          this.current = response.data
        })
        .catch(error => {
          console.log(['getCurrentTask error', error])
        })
    },
    stopTask () {
      this.current = null
      const path = this.$baseUrl + `/stop`
      axios.post(path)
        .then(response => {
          this.$emit('stop-task')
        })
        .catch(error => {
          console.log(['getCompletitions error', error])
        })
    }
  },
  components: {
    TaskItem
  },
  mounted () {
    this.getCurrentTask()
  }
}
</script>
