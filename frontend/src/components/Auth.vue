<template>
  <div>
    <form v-on:submit.prevent="log_in()">
      <md-card class="md-layout-item md-size-15" style="margin: auto">
        <md-card-content>
          <md-field>
            <label>Login</label>
            <md-input v-model.trim="login" type="text" required></md-input>
          </md-field>
          <md-field>
            <label>Password</label>
            <md-input v-model.trim="password" type="password" required></md-input>
          </md-field>
          <md-radio v-model="radio" value="registration">Registration</md-radio>
          <md-radio v-model="radio" value="login">Login</md-radio>
          <md-button type="submit" v-bind:disabled="isLogin">Send</md-button>
          <md-button v-bind:disabled="!isLogin" v-on:click="log_out()">Logout</md-button>
        </md-card-content>
      </md-card>
    </form>
  </div>
</template>

<script>
  import {urlEncode} from './helpers.js'

  export default {
    data() {
      return {
        login: 'login',
        password: 'password',
        radio: 'login',
        isLogin: false
      }
    },
    computed: {
    },
    methods: {
      log_out() {
        this.$cookie.delete('token')
        this.isLogin = false
      },
      log_in() {
        const path = this.$baseUrl + `/auth`
        var data = {login: this.login, password: this.password, action: this.radio}
        var options = {headers: {'Content-type': 'application/x-www-form-urlencoded'}}
        this.$axios.post(path, urlEncode(data), options)
          .then(response => {
            //только сообщаем об ошибках, редиректы и авторизация в main.js
            if (response.data.message !== undefined){
              alert(response.data.message)
            } else {
              this.isLogin = true;
            }
          })
          .catch(error => {
            console.log(['auth error', error])
          })
      }
    },
    mounted: function () {
      this.isLogin = !!this.$cookie.get('token')
    }
  }
</script>
