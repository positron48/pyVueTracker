// Main.vue
<template>
  <div>
    <nav>
      <div class="md-toolbar md-accent md-theme-demo-light md-elevation-1">
        <div class="md-title main-title">
          <a @click="go('Home')">Time tracker</a>
        </div>

        <button v-if="isLogin" type="button" class="md-button md-theme-demo-light short" @click="go('Help')">
          <font-awesome-icon icon="question-circle"/>
        </button>
        <button v-if="isLogin" type="button" class="md-button md-theme-demo-light" @click="go('Home')">
          <div class="md-ripple">
              <div class="md-button-content">Главный экран</div>
          </div>
        </button>
        <button v-if="isLogin" type="button" class="md-button md-theme-demo-light">
          <div class="md-ripple">
              <div class="md-button-content" @click="go('History')">История</div>
          </div>
        </button>
        <button v-if="isLogin" type="button" class="md-button md-theme-demo-light">
          <div class="md-ripple">
              <div class="md-button-content" @click="go('Export')">Экспорт</div>
          </div>
        </button>
        <button v-if="isLogin" type="button" class="md-button md-theme-demo-light">
          <div class="md-ripple">
              <div class="md-button-content" @click="go('Settings')">Настройки</div>
          </div>
        </button>
        <button type="button" class="md-button md-theme-demo-light">
          <div class="md-ripple">
              <div class="md-button-content" @click="go('Auth')">{{loginText}}</div>
          </div>
        </button>
      </div>
    </nav>

    <div class="container" id="main">
      <component v-bind:is="currentComponent" @login="updateLogin"></component>
    </div>
  </div>
</template>

<script>
import Home from './Home.vue'
import History from './History.vue'
import Auth from './Auth.vue'
import Export from './Export.vue'
import Settings from './Settings.vue'
import Help from './Help.vue'
import {isLogin, logout} from './auth.js'
import API from './api.js'

export default {
  data () {
    return {
      currentComponent: 'Auth',
      loginText: 'Выйти',
      isLogin: false,
      version: null,
      timer: null
    }
  },
  components: {
    Home, History, Auth, Export, Settings, Help
  },
  methods: {
    updateLogin () {
      this.isLogin = isLogin()
      this.loginText = this.isLogin ? 'Выйти' : 'Войти'
      this.currentComponent = this.isLogin ? 'Home' : 'Auth'
    },
    getVersion () {
      API.getVersion(this.version)
        .then(response => {
          if (this.version === null) {
            this.version = response.data.version
          } else if (this.version < parseFloat(response.data.version)) {
            // вывод уведомления пользователю с просьбой обновить страницу
            clearInterval(this.timer)
            if (confirm('Доступна новая версия!\nОбновить страницу?\nИзменения:\n' + response.data.changes.join('\n'))) {
              location.reload()
            } else {
              this.timer = setInterval(this.getVersion, 300000)
            }
          }
        })
        .catch(error => {
          console.log(['getVersion error', error])
        })
    },
    go (screen) {
      if (screen === 'Auth') {
        if (this.isLogin) {
          logout()
        }
        this.updateLogin()
      } else {
        if (this.isLogin) {
          this.currentComponent = screen
        } else {
          this.updateLogin()
        }
      }
    }
  },
  mounted: function () {
    this.updateLogin()
    this.getVersion()
    this.timer = setInterval(this.getVersion, 300000)
  }
}
</script>

<style>
  #main{
    margin-top: 60px;
  }
  .main-title{
    flex: 1;
    text-align: left;
  }
  .main-title a{
    cursor: pointer;
  }
  .main-title a:hover{
    text-decoration: none !important;
  }
  .mx-datepicker input{
    background-color: #ffffff !important;
  }
  .md-button.short{
    width: 36px;
    min-width: 36px;
  }
</style>
