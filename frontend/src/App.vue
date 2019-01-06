<template>
  <div id="app">
    <router-view/>
  </div>
</template>

<script>
export default {
  name: 'App'
}
</script>

<style>
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
}

.md-menu-content-bottom-start{
  z-index: 10000 !important;
  width: auto !important;
  max-width: fit-content !important;
}
.center{
  text-align: center;
}
</style>
