// Settings.vue
<template>
  <div>
    <div class="md-layout md-gutter md-alignment-top-center center">
      <div class="md-layout-item md-size-80">
        <md-list>
          <md-list-item>
            Трекеры
          </md-list-item>

          <md-table>
            <md-table-row>
              <md-table-head></md-table-head>
              <md-table-head>Название</md-table-head>
              <md-table-head>Url</md-table-head>
              <md-table-head>Тип</md-table-head>
              <md-table-head>Токен</md-table-head>
            </md-table-row>
            <md-table-row v-bind:key="tracker.id" v-for="tracker in trackers">
              <md-table-head>
                <div v-on:click="$emit('stop', tracker.id)">
                  <font-awesome-icon icon="edit"/>
                </div>
              </md-table-head>
              <md-table-head>{{tracker.title}}</md-table-head>
              <md-table-head>{{tracker.api_url}}</md-table-head>
              <md-table-head>{{tracker.type}}</md-table-head>
              <md-table-head>{{tracker.external_api_key}}</md-table-head>
            </md-table-row>
          </md-table>

          <md-list-item>
            <md-button>Добавить</md-button>
          </md-list-item>
        </md-list>
      </div>

      <br><br>

      <div class="md-layout-item md-size-80">
        <md-list>
          <md-list-item>
            Проекты
          </md-list-item>

          <md-table>
            <md-table-row>
              <md-table-head></md-table-head>
              <md-table-head>Название</md-table-head>
              <md-table-head>Url</md-table-head>
              <md-table-head>Тип</md-table-head>
              <md-table-head>Токен</md-table-head>
            </md-table-row>
            <md-table-row v-bind:key="project.id" v-for="project in projects">
              <md-table-head>
                <div v-on:click="$emit('stop', project.id)">
                  <font-awesome-icon icon="edit"/>
                </div>
              </md-table-head>
              <md-table-head>{{project.title}}</md-table-head>
              <md-table-head>{{project.api_url}}</md-table-head>
              <md-table-head>{{project.type}}</md-table-head>
              <md-table-head>{{project.external_api_key}}</md-table-head>
            </md-table-row>
          </md-table>

          <md-list-item>
            <md-button>Добавить</md-button>
          </md-list-item>
        </md-list>
      </div>
    </div>
  </div>
</template>

<script>
import API from './api.js'

export default {
  data () {
    return {
      trackers: [],
      projects: null,
    }
  },
  methods: {
    getTrackers () {
      API.getTrackers()
        .then(response => {
          console.log(response)
          this.trackers = response.data.trackers
        })
        .catch(error => {
          console.log(['getTasks error', error])
        })
    }
  },
  components: {},
  mounted () {
    this.getTrackers()
  }
}
</script>
