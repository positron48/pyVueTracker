import axios from 'axios'
import {isLogin, logout, getToken} from './auth.js'
import {urlEncode, formatDate} from './helpers.js'

const HTTP = axios.create({
  baseURL: 'https://time.skillum.ru',
  headers: {
    'Content-type': 'application/x-www-form-urlencoded'
  }
})

HTTP.interceptors.response.use(function (response) {
  if (typeof response.data === 'object' && response.data !== null && 'token' in response.data) {
    localStorage.setItem('token', response.data.token)
    delete response.data.token
  }
  return response
}, function (error) {
  if (error.response !== undefined && 'status' in error.response && error.response.status === 401 && isLogin()) {
    logout()
    location.reload()
  }
  return Promise.reject(error)
})

HTTP.interceptors.request.use(
  config => {
    config.headers.token = getToken()
    return config
  }
)

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

  // список заданий за период
  getGroupedTasks (dateStart, dateEnd) {
    var formattedStart = formatDate(dateStart)
    var formattedEnd = formatDate(dateEnd)

    const path = '/api/grouped_tasks?interval=' + formattedStart + '-' + formattedEnd
    return HTTP.get(path)
  },

  // последнее незавершенное задание
  getCurrentTask () {
    return HTTP.get('/api/current')
  },

  // список последних задач для автодополнения
  getCompletitions (text) {
    if (text) {
      return HTTP.get('/api/completitions?text=' + text)
    } else {
      return HTTP.get('/api/completitions')
    }
  },

  // список трекеров пользователя
  getTrackers () {
    return HTTP.get('/api/trackers')
  },

  // список проектов
  getProjects (ids) {
    return HTTP.get('/api/projects', {
      params: {
        projects: ids
      }
    })
  },

  // список проектов на трекере
  getTrackerProjects (trackerId) {
    return HTTP.get('/api/trackerProjects', {
      params: {
        id: trackerId
      }
    })
  },

  // список трекеров пользователя
  getEvoUsers () {
    return HTTP.get('/api/evoUsers')
  },

  // добавления задания
  addTask (taskName) {
    return HTTP.post('/api/task', urlEncode({name: taskName}))
  },

  // получение токена для трекера
  getToken (id, login, password) {
    return HTTP.post('/api/getToken', urlEncode({id: id, login: login, password: password}))
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

  // продолжение работы над заданием
  updateTask (task) {
    return HTTP.post('/api/task/edit',
      urlEncode({
        'id': task['id'],
        'name': task['name'],
        'category': task['category'],
        'date': task['date'],
        'start_time': task['start_time'],
        'end_time': task['end_time'],
        'description': task['description'],
        'tags': task['tags']
      }))
  },

  // удаление задания
  deleteTask (id) {
    return HTTP.post('/api/task/delete',
      urlEncode({
        id: id
      }))
  },

  // добавление/привязка трекера пользователю
  saveTracker (tracker) {
    return HTTP.post('/api/tracker',
      urlEncode({
        id: tracker.id,
        title: tracker.title,
        type: tracker.type,
        api_url: tracker.api_url
      }))
  },

  // привязка проекта к проекту на трекере
  linkProject (projectId, trackerId, trackerProject) {
    return HTTP.post('/api/linkProject',
      urlEncode({
        projectId: projectId,
        trackerId: trackerId,
        trackerProjectId: trackerProject !== null ? trackerProject.value : 0,
        trackerProjectTitle: trackerProject !== null ? trackerProject.label : 0
      }))
  },

  // добавление/привязка трекера пользователю
  saveEvoUser (evoUser) {
    return HTTP.post('/api/evoUser',
      urlEncode({
        id: evoUser['value']
      }))
  },

  // удаление/отвязка трекера пользователя
  deleteTracker (tracker) {
    return HTTP.post('/api/tracker/delete',
      urlEncode({
        id: tracker.id
      }))
  },

  // получение данных о задаче с трекера
  getTrackerTask (trackerId, externalTaskId) {
    return HTTP.get('/api/trackerTask', {
      params: {
        trackerId: trackerId,
        taskId: externalTaskId
      }
    })
  },

  // получение данных о задаче с трекера
  getVersion (version) {
    return HTTP.get('/api/version?version=' + version)
  },

  // обновление задания
  exportTask (exportTask) {
    return HTTP.post('/api/task/export',
      urlEncode(exportTask))
  }
}

export default API
