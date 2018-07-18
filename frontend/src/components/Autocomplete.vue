<template>
    <div class="autocomplete">
        <input id="autocompletedIntput" type="text" name="myCountry" placeholder="Country" @keydown="this.onKeydown" v-model="taskName" @focus="onFocus()">
        <div id="myInputautocomplete-list" class="autocomplete-items">
          <div
             v-if="showSuggestion"
             v-for="(suggest, index) in filteredSuggestion"
             :class="currentFocus === index ? 'autocomplete-active' : ''"
             v-bind:key="index"
             :data-id="index"
             @click="select(index)"
          >
            {{suggest}}
            <input type="hidden" :value="suggest">
          </div>
        </div>
    </div>
</template>

<style>
* {
  box-sizing: border-box;
}
.autocomplete {
  /* the container must be positioned relative: */
  width: 100%;
  position: relative;
  display: inline-block;
}
input {
  border: 1px solid transparent;
  background-color: #f1f1f1;
  padding: 10px;
  font-size: 16px;
}
input[type=text] {
  background-color: #f1f1f1;
  width: 100%;
}
input[type=submit] {
  background-color: DodgerBlue;
  color: #fff;
  cursor: pointer;
}
.autocomplete-items {
  position: absolute;
  border: 1px solid #d4d4d4;
  border-bottom: none;
  border-top: none;
  z-index: 99;
  /* position the autocomplete items to be the same width as the container: */
  top: 100%;
  left: 0;
  right: 0;
}
.autocomplete-items div {
  padding: 10px;
  cursor: pointer;
  background-color: #fff;
  border-bottom: 1px solid #d4d4d4;
}
.autocomplete-items div:hover {
  /* when hovering an item: */
  background-color: #e9e9e9;
}
.autocomplete-active {
  /* when navigating through the items using the arrow keys: */
  background-color: DodgerBlue !important;
  color: #ffffff;
}
</style>

<script>
import axios from 'axios'

export default {
  data () {
    return {
      taskName: '',
      taskCompletitions: [],
      showSuggestion: true,
      input: document.getElementById('autocompletedIntput'),
      currentFocus: -1
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
      const path = 'http://localhost:5000/api/completitions'
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
          this.$emit('add-task')
          this.$refs.tasks.getTasks()
        })
        .catch(error => {
          console.log(['getCompletitions error', error])
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
    setTaskBody (name) {
      var timeDelta = this.getTimeDelta(this.taskName, '', 0)
      if (timeDelta !== '') {
        this.taskName = timeDelta + ' ' + name
      } else {
        this.taskName = name
      }
    },
    onKeydown (e) {
      if (e.keyCode === 40) { // down
        this.currentFocus++
        if (this.currentFocus >= this.filteredSuggestion.length - 1) {
          this.currentFocus = this.filteredSuggestion.length - 1
        }
      } else if (e.keyCode === 38) { // up
        this.currentFocus--
        if (this.currentFocus < -1) {
          this.currentFocus = -1
        }
      } else if (e.keyCode === 13) { // enter
        if (this.currentFocus > -1) {
          this.select(this.currentFocus)
          e.preventDefault()
        }
      }
      console.log(this.currentFocus)
    },
    onFocus () {
      this.showSuggestion = true
    },
    onClickOut (e) {
      console.log(e.target.id)
      if (e.target.id !== 'autocompletedIntput') {
        this.showSuggestion = false
      }
    },
    select (index) {
      this.taskName = this.filteredSuggestion[index]
      this.currentFocus = -1
    },
    urlEncode (obj) {
      return Object.keys(obj).reduce(function (a, k) { a.push(k + '=' + encodeURIComponent(obj[k])); return a }, []).join('&')
    }
  },
  mounted () {
    this.getCompletitions()

    /* execute a function when someone clicks in the document: */
    document.addEventListener('click', this.onClickOut)
  }
}
</script>
