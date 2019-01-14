<template>
  <div v-if="current !== null">
      <form action="" method="post" class="md-layout md-gutter md-alignment-top-center center" v-on:submit.prevent="stopTask()">
        <md-card class="md-layout-item md-large-size-50 md-xlarge-size-50 md-medium-size-70 md-small-size-100">
          <md-card-content>
            <div class="md-layout">
              <md-list class="md-layout-item md-size-80">
                <TaskItem
                  :task="current"
                />
              </md-list>
              <div class="md-layout-item md-size-20">
                <md-button type="submit" class="md-primary" style="margin-top: 12px;">остановить</md-button>
              </div>
            </div>
          </md-card-content>
        </md-card>
      </form>
    </div>
</template>

<script>
import TaskItem from './TaskItem.vue'
import API from './api.js'

export default {
  data () {
    return {
      current: null
    }
  },
  methods: {
    getCurrentTask () {
      API.getCurrentTask()
        .then(response => {
          if (('status' in response.data && response.data.status) || !('status' in response.data)) {
            this.current = response.data
          } else {
            this.current = null
          }
        })
        .catch(error => {
          console.log(['getCurrentTask error', error])
        })
    },
    stopTask () {
      API.stopTask(this.current.id)
        .then(response => {
          this.$emit('stop-task')
          this.current = null
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
