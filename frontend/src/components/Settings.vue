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
                <div v-on:click="deleteTracker(tracker.id)">
                  <font-awesome-icon icon="edit"/>
                </div>
              </md-table-head>
              <md-table-head>{{tracker.title}}</md-table-head>
              <md-table-head>{{tracker.api_url}}</md-table-head>
              <md-table-head>{{tracker.type}}</md-table-head>
              <md-table-head>
                <span v-if="tracker.external_api_key">{{tracker.external_api_key}}</span>
                <a class="simple-link" v-if="!tracker.external_api_key" @click="showTokenModal(tracker)">Получить токен</a>
              </md-table-head>
            </md-table-row>
          </md-table>

          <md-list-item>
            <md-button @click="showTrackerModal()">Добавить redmine</md-button>
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
                <div v-on:click="editProject(project.id)">
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

    <modal :show="showTracker" @close="closeTrackerModal">
      <div class="modal-header">

      </div>
      <div class="modal-body">
        <input type="hidden" v-model="currentTracker.id" name=id>
        <input type="hidden" v-model="currentTracker.type" name=type>
        <md-field>
          <label>Название</label>
          <md-input v-model="currentTracker.title"></md-input>
        </md-field>
        <md-field>
          <label>Url</label>
          <md-input v-model="currentTracker.api_url"></md-input>
        </md-field>
      </div>
      <div class="modal-footer text-right">
        <md-button class="md-primary" @click="deleteTracker">удалить</md-button>
        <md-button class="md-primary" @click="closeTrackerModal">отмена</md-button>
        <md-button class="md-accent" @click="saveTracker">сохранить</md-button>
      </div>
    </modal>

    <modal :show="showToken" @close="closeTokenModal">
      <div class="modal-header">
        <h2>Данные для авторизации в {{currentTracker.title}}</h2>
      </div>
      <div class="modal-body">
        <input type="hidden" v-model="currentTracker.id" name=id>
        <input type="hidden" v-model="currentTracker.type" name=type>
        <md-field>
          <label>Логин</label>
          <md-input v-model="loginToken"></md-input>
        </md-field>
        <md-field>
          <label>Пароль</label>
          <md-input v-model="passwordToken" type="password"></md-input>
        </md-field>
      </div>
      <div class="modal-footer text-right">
        <md-button class="md-primary" @click="closeTokenModal">отмена</md-button>
        <md-button class="md-accent" @click="getToken">получить</md-button>
      </div>
    </modal>
  </div>
</template>

<script>
import API from './api.js'
import Modal from './Modal.vue'

export default {
  data () {
    return {
      trackers: [],
      projects: null,
      loginToken: '',
      passwordToken: '',
      currentTracker: {
        id: null,
        title: '',
        api_url: '',
        type: 'redmine'
      },
      showTracker: false,
      showToken: false
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
    },
    showTrackerModal () {
      this.showTracker = true
    },
    closeTrackerModal () {
      this.showTracker = false
    },
    deleteTracker (id) {

    },
    saveTracker () {

    },
    editTracker (tracker) {
      this.currentTracker = tracker
      this.showTrackerModal()
    },
    showTokenModal (tracker) {
      this.loginToken = ''
      this.passwordToken = ''
      this.currentTracker = tracker
      this.showToken = true
    },
    closeTokenModal () {
      this.showToken = false
    },
    getToken () {
      API.getToken(this.currentTracker.id, this.loginToken, this.passwordToken)
        .then(response => {
          console.log(response)
          if (response.data.external_token != undefined && response.data.external_token != "") {
            this.getTrackers()
            this.showToken = false
          } else {
            alert ('Токен не получен')
          }
        })
        .catch(error => {
          console.log(['getToken error', error])
        })
    }
  },
  components: {
    Modal
  },
  mounted () {
    this.getTrackers()
  }
}
</script>

<style scoped>
.simple-link {
  cursor: pointer;
}
</style>
