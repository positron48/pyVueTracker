// Home.vue
<template>
  <div>

    <form action="" method="post" class="md-layout md-gutter md-alignment-top-center" v-on:submit.prevent="addTask()">
      <md-card class="md-layout-item md-size-50 md-small-size-100">
        <md-card-content>
          <div class="md-layout">
            <md-field class="md-layout-item md-size-80">
              <label>Task</label>
              <md-input v-model="taskName"></md-input>
            </md-field>

            <div class="md-layout-item md-size-20">
              <md-button type="submit" class="md-primary" style="margin-top: 18px;">Add</md-button>
            </div>
          </div>
        </md-card-content>
      </md-card>
    </form>

    <div class="md-layout md-gutter md-alignment-top-center" v-if="filteredSuggestion.length">
      <md-list  class="md-layout-item md-size-50 md-small-size-100">
        <md-list-item
            v-for="suggestion in filteredSuggestion"
            :key="suggestion.id">
          <span class="md-list-item-text">{{suggestion}}</span>
        </md-list-item>
      </md-list>
    </div>

    <Tasks/>
  </div>
</template>

<script>
import Tasks from './Tasks.vue'
import axios from 'axios'

export default {
  data () {
    return {
      taskName: '',
      taskCompletitions: []
    }
  },
  computed: {
    filteredSuggestion: function () {
      var filtered = []
      var re = new RegExp(this.taskName, 'i')
      for (let item of this.taskCompletitions) {
        if (item.match(re)) {
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
    getCompletitions () {
      const path = `http://localhost:5000/api/completitions`
      axios.get(path)
        .then(response => {
          this.taskCompletitions = response.data.values
        })
        .catch(error => {
          console.log(['getCompletitions error', error])
        })
    },
    addTask () {
      const path = `http://localhost:5000/api/task`
      axios.post(path, this.urlEncode({name: this.taskName}),
        {
          headers: {
            'Content-type': 'application/x-www-form-urlencoded'
          }
        })
        .then(response => {

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
    Tasks
  },
  mounted () {
    this.getCompletitions()
  }
}
</script>
