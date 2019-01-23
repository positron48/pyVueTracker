import Vue from 'vue'
import App from './App'
import router from './router'

import VueMaterial from 'vue-material'
import vSelect from 'vue-select'
import 'vue-material/dist/vue-material.min.css'
import 'vue-material/dist/theme/black-green-light.css'
import {library} from '@fortawesome/fontawesome-svg-core'
import {faEdit, faPlayCircle, faStopCircle, faQuestionCircle} from '@fortawesome/free-solid-svg-icons'
import {FontAwesomeIcon} from '@fortawesome/vue-fontawesome'

library.add(faEdit)
library.add(faPlayCircle)
library.add(faStopCircle)
library.add(faQuestionCircle)

Vue.component('font-awesome-icon', FontAwesomeIcon)
Vue.component('v-select', vSelect)

Vue.use(VueMaterial)

var id = 0
var data = {}

Vue.mixin({
  beforeCreate: function beforeCreate () {
    var this$1 = this

    if (!this.$options.recomputed) { return }
    var me = 'r' + id++
    this._$recomputeId = me
    Vue.util.defineReactive(
      data,
      me,
      Object.keys(this.$options.recomputed).reduce(function (r, key) {
        r[key] = 0
        return r
      }, {})
    )
    this.$options.computed = this.$options.computed || {}
    Object.keys(this.$options.recomputed).forEach(function (key) {
      this$1.$options.computed[key] = function (vm) {
        /* eslint-disable-next-line */
        data[me][key]
        return this$1.$options.recomputed[key].call(vm, vm)
      }
    })
    this.$options.methods = this.$options.methods || {}
    this.$options.methods.$recompute = function (key) {
      data[me][key]++
    }
  },

  destroyed: function destroyed () {
    if (!this._$recomputeId) { return }
    delete data[this._$recomputeId]
  }
})

Vue.config.productionTip = false

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  render: h => h(App)
})
