import axios from 'axios'
import {isLogin, logout, getToken} from './auth.js'
import {urlEncode, formatDate} from './helpers.js'

const HTTP = axios.create({
  baseURL: 'http://localhost:5000',
  headers: {
    'token': getToken(),
    'Content-type': 'application/x-www-form-urlencoded'
  }
})

HTTP.interceptors.response.use(function (response) {
  if (response.data.token !== undefined) {
    localStorage.setItem('token', response.data.token)
    delete response.data.token
  }
  return response
}, function (error) {
  if (error.response.status === 401 && isLogin()) {
    logout()
    location.reload()
  }
  return Promise.reject(error)
})

export var API = {
  /** ------------------------------------ авторизация  ------------------------------------ */
  auth (login, password, radio) {
    const path = '/api/auth'
    var data = {login: login, password: password, action: radio}
    return HTTP.post(path, urlEncode(data))
  },

  /** ------------------------------------ тайм-трекинг  ------------------------------------ */
  // список заданий за период
  getTasks (dateStart, dateEnd) {
    var formattedStart = formatDate(dateStart)
    var formattedEnd = formatDate(dateEnd)

    const path = '/api/tasks?interval=' + formattedStart + '-' + formattedEnd
    return HTTP.get(path)
  },

  // последнее незавершенное задание
  getCurrentTask () {
    return HTTP.get('/api/current')
  },

  // список последних задач для автодополнения
  getCompletitions () {
    return HTTP.get('/api/completitions')
  },

  // добавления задания
  addTask (taskName) {
    return HTTP.post('/api/task', urlEncode({name: taskName}))
  },

  // остановка задания
  stopTask (id) {
    return HTTP.post('/api/task/stop',
      urlEncode({
        id: id
      }))
  },

  // продолжение работы над заданием
  resumeTask (id) {
    return HTTP.post('/api/task/resume',
      urlEncode({
        id: id
      }))
  },

  // удаление задания
  deleteTask (id) {
    return HTTP.post('/api/task/delete',
      urlEncode({
        id: id
      }))
  },

  // обновление задания
  updateTask (task) {
    return HTTP.post('/api/task/edit',
      urlEncode({
        id: task.id,
        name: task.name,
        category: task.category,
        date: task.date,
        start_time: task.start_time,
        end_time: task.end_time,
        description: task.description,
        tags: task.tags
      }))
  }
}

export default API