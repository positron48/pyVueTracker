// Main.vue
<template>
  <div>
    <nav>
      <div class="md-toolbar md-accent md-theme-demo-light md-elevation-1">
        <div class="md-title main-title">Time tracker</div>
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
import {isLogin, logout} from './auth.js'

export default {
  data () {
    return {
      currentComponent: 'Auth',
      loginText: 'Выйти',
      isLogin: false
    }
  },
  components: {
    Home, History, Auth, Export, Settings
  },
  methods: {
    updateLogin () {
      this.isLogin = isLogin()
      this.loginText = this.isLogin ? 'Выйти' : 'Войти'
      this.currentComponent = this.isLogin ? 'Home' : 'Auth'
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
</style>
