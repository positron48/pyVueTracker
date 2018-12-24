import Vue from 'vue'
import App from './App'
import router from './router'

import VueMaterial from 'vue-material'
import 'vue-material/dist/vue-material.min.css'
import 'vue-material/dist/theme/black-green-light.css'
import {library} from '@fortawesome/fontawesome-svg-core'
import {faEdit, faPlayCircle, faStopCircle} from '@fortawesome/free-solid-svg-icons'
import {FontAwesomeIcon} from '@fortawesome/vue-fontawesome'
import VueCookie from 'vue-cookie'

library.add(faEdit)
library.add(faPlayCircle)
library.add(faStopCircle)

Vue.component('font-awesome-icon', FontAwesomeIcon)

Vue.use(VueMaterial)
Vue.use(VueCookie)

Vue.config.productionTip = false

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  render: h => h(App)
})
