<template>
  <div>
      <form action="" method="post" class="md-layout md-gutter md-alignment-top-center center" v-on:submit.prevent="addTask()">
        <md-card class="md-layout-item md-large-size-50 md-xlarge-size-50 md-medium-size-70 md-small-size-100">
          <md-card-content>
            <div class="md-layout">
              <div class="md-layout-item md-size-80">
                <Autocomplete
                  v-model="taskName"
                  :suggestions="filteredSuggestion"
                  @input="getCompletitions()"
                  ref="autocomplete"
                />
              </div>

              <div class="md-layout-item md-size-20">
                <md-button type="submit" class="md-primary" style="margin-top: 18px;">добавить</md-button>
              </div>
            </div>
          </md-card-content>
        </md-card>
      </form>
      <md-dialog-alert :md-active.sync="showAlert" :md-content="alertMessage" md-confirm-text="Ок" />
    </div>
</template>

<script>
import Autocomplete from './Autocomplete.vue'
import {API} from './api.js'

export default {
  data () {
    return {
      taskName: '',
      taskCompletitions: [],
      showSuggestion: false,

      showAlert: false,
      alertMessage: ''
    }
  },
  props: {
    tags: {
      type: Array
    },
    projects: {
      type: Array
    }
  },
  components: {
    Autocomplete
  },
  computed: {
    filteredSuggestion: function () {
      var filtered = []
      var name = this.taskName.toLowerCase()
      var re
      var partBefore
      var part

      if (!/[@#,]/.test(name)) {
        var timeDelta = this.getTimeDelta(name, '', 0)
        var nameForFilter = name.replace(timeDelta, '').trim().replace(/[[\]{}()*+?.,\\^$|#\s]/g, '\\$&')
        re = new RegExp(nameForFilter, 'i')
        for (var item of this.taskCompletitions) {
          if (re.test(item) && item !== nameForFilter) {
            if (timeDelta.length > 0) {
              filtered.push(timeDelta + ' ' + item)
            } else {
              filtered.push(item)
            }
          }
          if (filtered.length >= 10) {
            break
          }
        }
      } else if (/@/.test(name) && !/[#,]/.test(name)) {
        partBefore = name.replace(/^(.*@).*$/, '$1')
        part = name.replace(/^.*@(.*)$/, '$1')
        re = new RegExp(part, 'i')
        for (var project of this.projects) {
          if (re.test(project) && project !== part) {
            filtered.push(partBefore + project)
          }
          if (filtered.length >= 10) {
            break
          }
        }
      } else if (/#/.test(name) && !/[,]/.test(name)) {
        partBefore = name.replace(/^(.*#).*$/, '$1')
        part = name.replace(/^.*#(.*)$/, '$1')
        re = new RegExp(part, 'i')
        for (var tag of this.tags) {
          if (re.test(tag) && tag !== part) {
            filtered.push(partBefore + tag)
          }
          if (filtered.length >= 10) {
            break
          }
        }
      }
      return filtered
    }
  },
  methods: {
    getCompletitions () {
      var name = this.taskName.toLowerCase()
      var timeDelta = this.getTimeDelta(name, '', 0)
      var nameForFilter = name.replace(timeDelta, '').trim()
      API.getCompletitions(nameForFilter)
        .then(response => {
          this.taskCompletitions = response.data.values
        })
        .catch(error => {
          console.log(['getCompletitions error', error])
        })
    },
    addTask () {
      API.addTask(this.taskName)
        .then(response => {
          if (response.data.status) {
            this.taskName = ''
            this.$emit('add-task')
            this.$refs.autocomplete.clear()
          } else if ('message' in response.data) {
            this.alert(response.data.message)
          }
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
    },
    alert (message) {
      this.alertMessage = message
      this.showAlert = true
    }
  },
  mounted () {
    this.getCompletitions()
  }
}
</script>
