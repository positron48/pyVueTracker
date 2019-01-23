<template>
  <div>
    <md-card class="md-layout-item md-size-20" style="margin: auto">
      <md-card-content>
        <md-field>
          <label>Логин</label>
          <md-input v-model.trim="login" type="text" required></md-input>
        </md-field>
        <md-field>
          <label>Пароль</label>
          <md-input v-model.trim="password" type="password" required></md-input>
        </md-field>
        <div class="auth-buttons">
          <md-button @click="register()">Регистрация</md-button>
          <md-button @click="auth()">Вход</md-button>
        </div>
      </md-card-content>
    </md-card>
  </div>
</template>

<script>
import API from './api.js'
import {isLogin, logout} from './auth.js'

export default {
  data () {
    return {
      login: '',
      password: '',
      isLogin: false
    }
  },
  computed: {},
  methods: {
    auth () {
      API.auth(this.login, this.password, 'login')
        .then(response => {
          if (response.data.message !== undefined) {
            alert(response.data.message)
          } else {
            this.isLogin = isLogin()
            this.$emit('login')
          }
        })
        .catch(error => {
          console.log(['auth error', error])
        })
    },
    register () {
      API.auth(this.login, this.password, 'registration')
        .then(response => {
          if (response.data.message !== undefined) {
            alert(response.data.message)
          } else {
            this.isLogin = isLogin()
            this.$emit('login')
          }
        })
        .catch(error => {
          console.log(['auth error', error])
        })
    }
  },
  mounted: function () {
    this.isLogin = isLogin()
  }
}
</script>

<style>
.auth-buttons{
  text-align: center;
}
</style>
