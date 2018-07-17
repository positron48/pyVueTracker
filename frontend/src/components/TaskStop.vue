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
  computed: {
    filteredSuggestion: function () {
      var filtered = []
      var nameForFilter = this.taskName.replace(this.getTimeDelta(this.taskName, '', 0), '').trim()
      var re = new RegExp(nameForFilter, 'i')
      for (let item of this.taskCompletitions) {
        if (item.match(re) && item !== nameForFilter) {
          filtered.push(item)
        }
        if (filtered.length >= 10) {
          break
        }
      }
      return filtered
    }
  },
  methods: {
    getCurrentTask () {
      const path = `http://localhost:5000/api/current`
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
      const path = `http://localhost:5000/api/stop`
      axios.post(path)
        .then(response => {
          this.$emit('stop-task')
        })
        .catch(error => {
          console.log(['getCompletitions error', error])
        })
    },
    urlEncode (obj) {
      return Object.keys(obj).reduce(function (a, k) { a.push(k + '=' + encodeURIComponent(obj[k])); return a }, []).join('&')
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
