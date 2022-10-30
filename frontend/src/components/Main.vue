// Main.vue
<template>
  <div>
    <nav>
      <div class="md-toolbar md-accent md-theme-demo-light md-elevation-1">
        <div class="md-title main-title">
          <a @click="go('Home')">Time tracker</a>
        </div>

        <button type="button" class="md-button md-theme-demo-light short" @click="go('Help')">
          <font-awesome-icon icon="question-circle" :class="currentComponent=='Help' ? 'current' : ''"/>
        </button>
        <button v-if="isLogin" type="button" class="md-button md-theme-demo-light" @click="go('Home')">
          <div class="md-ripple">
              <div class="md-button-content" :class="currentComponent=='Home' ? 'current' : ''">Главный экран</div>
          </div>
        </button>
        <button v-if="isLogin" type="button" class="md-button md-theme-demo-light" @click="go('History')">
          <div class="md-ripple">
              <div class="md-button-content" :class="currentComponent=='History' ? 'current' : ''">История</div>
          </div>
        </button>
        <button v-if="isLogin" type="button" class="md-button md-theme-demo-light" @click="go('Export')">
          <div class="md-ripple">
              <div class="md-button-content" :class="currentComponent=='Export' ? 'current' : ''">Экспорт</div>
          </div>
        </button>
        <button v-if="isLogin" type="button" class="md-button md-theme-demo-light" @click="go('Settings')">
          <div class="md-ripple">
              <div class="md-button-content" :class="currentComponent=='Settings' ? 'current' : ''">Настройки</div>
          </div>
        </button>
        <button type="button" class="md-button md-theme-demo-light" @click="go('Auth')">
          <div class="md-ripple">
              <div class="md-button-content" :class="currentComponent=='Auth' ? 'current' : ''">{{loginText}}</div>
          </div>
        </button>
      </div>
    </nav>

    <div class="container" id="main">
      <component v-bind:is="currentComponent" @login="updateLogin"></component>
    </div>

    <md-dialog-confirm
      :md-active.sync="dialog.show"
      :md-title="dialog.title"
      :md-content="dialog.content"
      md-confirm-text="Да"
      md-cancel-text="Обновлю позже"
      @md-cancel="onCancel"
      @md-confirm="onConfirm" />
  </div>
</template>

<script>
import Home from './Home.vue'
import History from './History.vue'
import Auth from './Auth.vue'
import Export from './Export.vue'
import Settings from './Settings.vue'
import Help from './Help.vue'
import NotFound from './NotFound.vue'
import {isLogin, logout} from './auth.js'
import API from './api.js'

export default {
  data () {
    return {
      currentComponent: null,
      loginText: 'Выйти',
      isLogin: false,
      version: null,
      timer: null,
      dialog: {
        show: false,
        title: 'Доступна новая версия!',
        content: ''
      }
    }
  },
  components: {
    Home, History, Auth, Export, Settings, Help, NotFound
  },
  methods: {
    updateLogin () {
      this.isLogin = isLogin()
      this.loginText = this.isLogin ? 'Выйти' : 'Войти'
      var component = location.pathname.substr(1)
      component = component.charAt(0).toUpperCase() + component.slice(1)
      if (this.isLogin) {
        if (component === 'Auth' || component === '') {
          this.go('Home')
        } else if (['Home', 'History', 'Export', 'Help', 'Settings'].indexOf(component) !== -1) {
          this.go(component)
        } else {
          this.go('NotFound')
        }
      } else {
        if (component === 'Help') {
          this.go(component)
        } else {
          this.go('Auth')
        }
      }
    },
    getVersion () {
      API.getVersion(this.version)
        .then(response => {
          if (this.version === null) {
            this.version = response.data.version
          } else if (this.version < parseFloat(response.data.version)) {
            // вывод уведомления пользователю с просьбой обновить страницу
            this.dialog.content = 'Изменения:<br>' + response.data.changes.join('<br>') + '<br><br>Обновить страницу?'
            this.dialog.show = true
          }
        })
        .catch(error => {
          console.log(['getVersion error', error])
        })
    },
    go (screen) {
      if (screen !== this.currentComponent) {
        if (['Auth', 'Help'].indexOf(screen) !== -1) {
          if (screen === 'Auth' && this.isLogin) {
            logout()
            this.isLogin = isLogin()
            this.loginText = this.isLogin ? 'Выйти' : 'Войти'
          }
          this.currentComponent = screen
          this.changeUrl(screen)
        } else {
          if (this.isLogin) {
            this.currentComponent = screen
            this.changeUrl(screen)
          } else {
            this.updateLogin()
          }
        }
      }
    },
    changeUrl (screen) {
      if (window.history.replaceState) {
        window.history.replaceState(screen, screen, '/' + screen.toLowerCase())
      } else {
        window.history.pushState(screen, screen, '/' + screen.toLowerCase())
      }
    },
    onConfirm () {
      location.reload(true)
    },
    onCancel () {
      this.dialog.show = false
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
    padding: 0 20px;
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
  .current{
    color: #20a000;
  }
  .dropdown.v-select button.clear span{
    position: relative !important;
    top: 4px !important;
  }
  .dropdown.v-select button.open-indicator span{
    top: -1px;
    position: relative;
  }
  .md-list-item-content {
    display: block !important;
    padding-top: 15px !important;
  }
  .task-duration-list-item .md-list-item-content{
    width: 120px;
    text-align: right;
    float: right;
    margin-right: 5px;
    font-weight: bold;
  }
  .md-overlay{
    z-index: 7 !important;
  }
  .md-dialog {
    z-index: 10000 !important;
  }
  .md-overlay {
    z-index: 9999 !important;
  }
</style>
