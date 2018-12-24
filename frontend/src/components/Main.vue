// Main.vue
<template>
  <div>
    <nav>
      <div class="md-toolbar md-accent md-theme-demo-light md-elevation-1">
        <div class="md-title main-title">Time tracker</div>
        <button type="button" class="md-button md-theme-demo-light" @click="currentComponent='Auth'">
          <div class="md-ripple">
              <div class="md-button-content">Авторизация</div>
          </div>
        </button>
        <button type="button" class="md-button md-theme-demo-light" @click="currentComponent='Home'">
          <div class="md-ripple">
              <div class="md-button-content">Главный экран</div>
          </div>
        </button>
        <button type="button" class="md-button md-theme-demo-light">
          <div class="md-ripple">
              <div class="md-button-content" @click="currentComponent='Statistics'">Статистика</div>
          </div>
        </button>
      </div>
    </nav>

    <div class="container" id="main">
      <component v-bind:is="currentComponent"></component>
    </div>
  </div>
</template>

<script>
import Home from './Home.vue'
import Statistics from './Statistics.vue'
import Auth from './Auth.vue'

export default {
  data () {
    return {
      currentComponent: 'Home'
    }
  },
  components: {
    Home, Statistics, Auth
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
