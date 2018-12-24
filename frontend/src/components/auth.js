export function isLogin () {
  var token = localStorage.getItem('token')
  return token !== null && token !== ''
}

export function logout () {
  localStorage.removeItem('token')
}

export function getToken () {
  return localStorage.getItem('token')
}

export default {isLogin, logout, getToken}
