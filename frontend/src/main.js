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
import axios from 'axios'

library.add(faEdit)
library.add(faPlayCircle)
library.add(faStopCircle)

Vue.component('font-awesome-icon', FontAwesomeIcon)

Vue.use(VueMaterial)
Vue.use(VueCookie)

Vue.config.productionTip = false

Vue.prototype.$host = 'http://localhost:5000'
Vue.prototype.$baseUrl = Vue.prototype.$host + '/api'
Vue.prototype.$axios = axios
Vue.prototype.$isLogin = function () {
  var token = Vue.prototype.$cookie.get('token')
  return token !== null && token !== ''
}
Vue.prototype.$logout = function () {
  Vue.prototype.$cookie.delete('token')
}

// передаем каждый запрос токен авторизации
Vue.prototype.$axios.interceptors.request.use(function (request) {
  request.headers['token'] = Vue.prototype.$cookie.get('token')
  return request
})
// проверяем каждый ответ на признак обновленного/невалидного токена
Vue.prototype.$axios.interceptors.response.use(function (response) {
  if (response.data.token !== undefined) {
    Vue.prototype.$cookie.set('token', response.data.token, {expires: '1Y'})
    delete response.data.token
  }
  return response
}, function (error) {
  if (error.response.status === 401 && Vue.prototype.$isLogin()) {
    Vue.prototype.$logout()
    location.reload()
  }
  return Promise.reject(error)
})

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  render: h => h(App)
})
