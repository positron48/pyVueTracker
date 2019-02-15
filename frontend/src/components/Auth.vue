<template>
  <div>
    <md-card class="md-layout-item md-size-20" style="margin: auto">
      <md-card-content>
        <md-field>
          <label>Логин</label>
          <md-input @keydown.native="onKeyDown" v-model.trim="login" type="text" required></md-input>
          <md-tooltip md-direction="right">Логин redmine</md-tooltip>
        </md-field>
        <md-field>
          <label>Пароль</label>
          <md-input @keydown.native="onKeyDown" v-model.trim="password" type="password" required></md-input>
          <md-tooltip md-direction="right">Пароль redmine</md-tooltip>
        </md-field>
        <div class="auth-buttons">
          <md-button @click="auth()">Войти</md-button>
        </div>
      </md-card-content>
    </md-card>
    <md-dialog-alert :md-active.sync="showAlert" :md-content="alertMessage" md-confirm-text="Ок" />
  </div>
</template>

<script>
import API from './api.js'
import {isLogin} from './auth.js'

export default {
  data () {
    return {
      login: '',
      password: '',
      isLogin: false,

      showAlert: false,
      alertMessage: ''
    }
  },
  computed: {},
  methods: {
    auth () {
      API.auth(this.login, this.password, 'login')
        .then(response => {
          if (response.data.message !== undefined) {
            this.alert(response.data.message)
          } else {
            this.isLogin = isLogin()
            this.$emit('login')
          }
        })
        .catch(error => {
          console.log(['auth error', error])
        })
    },
    onKeyDown (e) {
      if (e.keyCode === 13) { // enter
        this.auth()
      }
    },
    alert (message) {
      this.alertMessage = message
      this.showAlert = true
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
