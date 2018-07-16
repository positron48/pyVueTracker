<template>
  <div>
      <form action="" method="post" class="md-layout md-gutter md-alignment-top-center" v-on:submit.prevent="addTask()">
        <md-card class="md-layout-item md-large-size-50 md-xlarge-size-50 md-medium-size-70 md-small-size-100">
          <md-card-content>
            <div class="md-layout">
              <md-field class="md-layout-item md-size-80" md-clearable>
                <label>Task</label>
                <md-input v-model="taskName" @focus.native="onFocus"></md-input>
              </md-field>

              <div class="md-layout-item md-size-20">
                <md-button type="submit" class="md-primary" style="margin-top: 18px;">Add</md-button>
              </div>
            </div>
          </md-card-content>
        </md-card>
      </form>

      <div class="md-layout md-gutter md-alignment-top-center" v-if="filteredSuggestion.length && showSuggestion">
        <md-list class="md-layout-item md-large-size-50 md-xlarge-size-50 md-medium-size-70 md-small-size-100">
          <md-list-item
              @click="setTaskBody(suggestion)"
              v-for="suggestion in filteredSuggestion"
              :key="suggestion.id">
            <span class="md-list-item-text">{{suggestion}}</span>
          </md-list-item>
        </md-list>
      </div>
    </div>
</template>

<script>
import axios from 'axios'

export default {
  data () {
    return {
      taskName: '',
      taskCompletitions: [],
      showSuggestion: false
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
          this.taskName = ''
          this.$refs.tasks.getTasks()
        })
        .catch(error => {
          console.log(['getCompletitions error', error])
        })
    },
    urlEncode (obj) {
      return Object.keys(obj).reduce(function (a, k) { a.push(k + '=' + encodeURIComponent(obj[k])); return a }, []).join('&')
    },
    getTimeDelta (task, currentTimeDelta, step) {
      var timeDelta = ''

      var re = [
        new RegExp(/^-[0-9]{0,3}/),
        new RegExp(/^([0-1]?[0-9]|[2][0-3]):([0-5][0-9])/),
        new RegExp(/^([0-1]?[0-9]|[2][0-3]):([0-5][0-9])-([0-1]?[0-9]|[2][0-3]):([0-5][0-9])/)
      ]

      if (step === 0) {
        if (task.match(re[2])) {
          return task.match(re[2])[0]
        }
      }

      if (task.match(re[0])) {
        timeDelta = task.match(re[0])[0]
      } else if (task.match(re[1])) {
        timeDelta = task.match(re[1])[0]
      }

      if (timeDelta !== '' && step === 0) {
        return this.getTimeDelta(
          task.replace(timeDelta, '').trim(),
          timeDelta,
          1
        )
      }
      if (currentTimeDelta !== '' && timeDelta !== '') {
        timeDelta = currentTimeDelta + ' ' + timeDelta
      } else if (currentTimeDelta !== '' && timeDelta === '') {
        return currentTimeDelta
      }

      console.log(timeDelta)
      return timeDelta
    },
    setTaskBody (name) {
      var timeDelta = this.getTimeDelta(this.taskName, '', 0)
      console.log(timeDelta)
      if (timeDelta !== '') {
        this.taskName = timeDelta + ' ' + name
      } else {
        this.taskName = name
      }
    },
    onFocus () {
      this.showSuggestion = true
    }
  },
  mounted () {
    this.getCompletitions()
  }
}
</script>
