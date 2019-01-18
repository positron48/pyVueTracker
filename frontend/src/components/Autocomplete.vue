<template>
  <div class="autocomplete">
    <input
      id="autocompletedIntput"
      type="text"
      autocomplete="off"
      placeholder="задача@проект #тег, комментарий"
      @keydown="this.onKeydown"
      v-model="inputValue"
      @input="$emit('input', $event.target.value)"
      @focus="onFocus"
    >
    <div id="myInputautocomplete-list" class="autocomplete-items">
      <div
        v-if="showSuggestion"
        v-for="(suggest, index) in suggestions"
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

<script>
export default {
  data () {
    return {
      showSuggestion: false,
      input: document.getElementById('autocompletedIntput'),
      currentFocus: -1,
      inputValue: ''
    }
  },
  props: {
    taskName: {
      type: String
    },
    suggestions: {
      type: Array
    }
  },
  methods: {
    onKeydown (e) {
      if (e.keyCode === 40) { // down
        this.currentFocus++
        if (this.currentFocus >= this.suggestions.length - 1) {
          this.currentFocus = this.suggestions.length - 1
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
    },
    onFocus () {
      this.showSuggestion = true
    },
    onClickOut (e) {
      if (e.target.id !== 'autocompletedIntput') {
        this.showSuggestion = false
      }
    },
    select (index) {
      this.inputValue = this.suggestions[index]

      this.$emit('input', this.inputValue)
      this.currentFocus = -1
    },
    clear () {
      this.inputValue = ''
      this.$emit('input', this.inputValue)
    },
    urlEncode (obj) {
      return Object.keys(obj).reduce(function (a, k) { a.push(k + '=' + encodeURIComponent(obj[k])); return a }, []).join('&')
    }
  },
  mounted () {
    /* execute a function when someone clicks in the document: */
    document.addEventListener('click', this.onClickOut)
  }
}
</script>

<style>
  * {
    box-sizing: border-box;
  }
  .autocomplete {
    width: 100%;
    position: relative;
    display: inline-block;
    margin-top: 15px;
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
    text-align: left;
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
