import axios from 'axios'
import {urlEncode, formatDate} from './helpers.js'

const HTTP = axios.create({
  baseURL: 'http://localhost:5000',
  headers: {
    'Authorization': '123',
    'Content-type': 'application/x-www-form-urlencoded'
  }
})

var API = {
  getTasks (dateStart, dateEnd) {
    var formattedStart = formatDate(dateStart)
    var formattedEnd = formatDate(dateEnd)

    const path = '/api/tasks?interval=' + formattedStart + '-' + formattedEnd
    return HTTP.get(path)
  },

  getCurrentTask () {
    return HTTP.get('/api/current')
  },

  getCompletitions () {
    return HTTP.get('/api/completitions')
  },

  addTask (taskName) {
    return HTTP.post('/api/task', urlEncode({name: taskName}))
  },

  stopTask (id) {
    return HTTP.post('/api/task/stop',
      urlEncode({
        id: id
      }))
  },

  resumeTask (id) {
    return HTTP.post('/api/task/resume',
      urlEncode({
        id: id
      }))
  },

  deleteTask (id) {
    return HTTP.post('/api/task/delete',
      urlEncode({
        id: id
      }))
  },

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
