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
              <md-table-head>Пользователь</md-table-head>
            </md-table-row>
            <md-table-row v-bind:key="tracker.id" v-for="tracker in trackers">
              <md-table-head>
                <div v-on:click="editTracker(tracker)">
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
              <md-table-head>
                <span v-if="tracker.external_user_id">{{tracker.external_user_id}}</span>
                <a class="simple-link" v-if="!tracker.external_user_id && tracker.external_api_key && tracker.type == 'evo'"
                 @click="showUserModal(tracker)">Указать пользователя</a>
              </md-table-head>
            </md-table-row>
          </md-table>

          <md-list-item>
            <md-button @click="addTracker()">Добавить redmine</md-button>
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

    <modal :show="showUser">
      <div class="modal-header">
        <h2>Выберите пользователя в {{currentTracker.title}}</h2>
      </div>
      <div class="modal-body">
        <input type="hidden" v-model="currentTracker.id" name=id>
        <md-autocomplete v-model="evoUser" :md-options="evoUsers" md-dense>
        </md-autocomplete>
      </div>
      <div class="modal-footer text-right">
        <md-button class="md-primary" @click="closeUserModal">отмена</md-button>
        <md-button class="md-accent" @click="saveEvoUser">сохранить</md-button>
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
      evoUsers: [],
      evoUser: '',
      projects: null,
      loginToken: '',
      passwordToken: '',
      currentTracker: {
        id: 0,
        title: '',
        api_url: '',
        type: 'redmine'
      },
      showTracker: false,
      showUser: false,
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
    getEvoUsers () {
      API.getEvoUsers()
        .then(response => {
          console.log(response)
          this.evoUsers = response.data.users
        })
        .catch(error => {
          console.log(['getEvoUsers error', error])
        })
    },
    showTrackerModal () {
      this.showTracker = true
    },
    closeTrackerModal () {
      this.showTracker = false
    },
    deleteTracker (id) {
      if (confirm('вы действительно хотите удалить трекер из списка?')) {
        API.deleteTracker(this.currentTracker)
          .then(response => {
            console.log(response)
            this.getTrackers()
            this.showTracker = false
          })
          .catch(error => {
            console.log(['getToken error', error])
          })
      }
    },
    saveTracker () {
      // todo сообщение о невозможности редактирвоания, если трекер привязан еще к кому-то
      API.saveTracker(this.currentTracker)
        .then(response => {
          console.log(response)
          this.getTrackers()
          this.showTracker = false
        })
        .catch(error => {
          console.log(['getToken error', error])
        })
    },
    saveEvoUser () {
      API.saveEvoUser(this.evoUser)
        .then(response => {
          console.log(response)
          this.getTrackers()
          this.showUser = false
        })
        .catch(error => {
          console.log(['saveTrackerUser error', error])
        })
    },
    addTracker () {
      this.currentTracker = {
        id: 0,
        title: '',
        api_url: '',
        type: 'redmine'
      }
      this.showTrackerModal()
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
    showUserModal (tracker) {
      this.currentTracker = tracker
      this.showUser = true
    },
    closeTokenModal () {
      this.showToken = false
    },
    closeUserModal () {
      this.showUser = false
    },
    getToken () {
      API.getToken(this.currentTracker.id, this.loginToken, this.passwordToken)
        .then(response => {
          console.log(response)
          if (response.data.external_token !== undefined && response.data.external_token !== '') {
            this.getTrackers()
            this.showToken = false
          } else {
            alert('Токен не получен')
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
    this.getEvoUsers()
  }
}
</script>

<style scoped>
.simple-link {
  cursor: pointer;
}
</style>
