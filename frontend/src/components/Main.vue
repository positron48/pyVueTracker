// Main.vue
<template>
  <div>
    <nav>
      <div class="md-toolbar md-accent md-theme-demo-light md-elevation-1">
        <div class="md-title main-title">Time tracker</div>
        <button type="button" class="md-button md-theme-demo-light" @click="go('Home')">
          <div class="md-ripple">
              <div class="md-button-content">Главный экран</div>
          </div>
        </button>
        <button type="button" class="md-button md-theme-demo-light">
          <div class="md-ripple">
              <div class="md-button-content" @click="go('Statistics')">Статистика</div>
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
import Statistics from './Statistics.vue'
import Auth from './Auth.vue'
import {isLogin, logout} from './auth.js'

export default {
  data () {
    return {
      currentComponent: 'Auth',
      loginText: 'Выйти'
    }
  },
  components: {
    Home, Statistics, Auth
  },
  methods: {
    updateLogin () {
      this.loginText = isLogin() ? 'Выйти' : 'Войти'
      this.currentComponent = isLogin() ? 'Home' : 'Auth'
    },
    go (screen) {
      var isAuthorized = isLogin()
      if (screen === 'Auth') {
        if (isAuthorized) {
          logout()
        }
        this.updateLogin()
      } else {
        if (isAuthorized) {
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
