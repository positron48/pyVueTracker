<template>
  <div>
      <form action="" method="post" class="md-layout md-gutter md-alignment-top-center" v-on:submit.prevent="addTask()">
        <md-card class="md-layout-item md-large-size-50 md-xlarge-size-50 md-medium-size-70 md-small-size-100">
          <md-card-content>
            <div class="md-layout">
              <div class="md-layout-item md-size-80">
                <Autocomplete
                  v-model="taskName"
                  :suggestions="filteredSuggestion"
                  ref="autocomplete"
                />
              </div>

              <div class="md-layout-item md-size-20">
                <md-button type="submit" class="md-primary" style="margin-top: 18px;">Add</md-button>
              </div>
            </div>
          </md-card-content>
        </md-card>
      </form>
    </div>
</template>

<script>
import axios from 'axios'
import Autocomplete from './Autocomplete.vue'
import {urlEncode} from './helpers.js'

export default {
  data () {
    return {
      taskName: '',
      taskCompletitions: [],
      showSuggestion: false
    }
  },
  components: {
    Autocomplete
  },
  computed: {
    filteredSuggestion: function () {
      var filtered = []
      var name = this.taskName.toLowerCase()
      var timeDelta = this.getTimeDelta(name, '', 0)
      var nameForFilter = name.replace(timeDelta, '').trim()
      var re = new RegExp(nameForFilter, 'i')
      for (var item of this.taskCompletitions) {
        if (item.match(re) && item !== nameForFilter) {
          filtered.push(timeDelta + ' ' + item)
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
      const path = this.$baseUrl + `/completitions`
      axios.get(path)
        .then(response => {
          this.taskCompletitions = response.data.values
        })
        .catch(error => {
          console.log(['getCompletitions error', error])
        })
    },
    addTask () {
      const path = this.$baseUrl + `/task`
      axios.post(path, urlEncode({name: this.taskName}),
        {
          headers: {
            'Content-type': 'application/x-www-form-urlencoded'
          }
        })
        .then(response => {
          this.taskName = ''
          this.$emit('add-task')
          this.$refs.autocomplete.clear()
        })
        .catch(error => {
          console.log(['addTask error', error])
        })
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

      return timeDelta
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
