// Settings.vue
<template>
  <div>
    <div class="md-layout md-gutter md-alignment-top-center center">
      <div class="md-layout-item md-size-80">
        <md-list>
          <md-list-item>
            <h3>Трекеры</h3>
          </md-list-item>

          <md-table>
            <md-table-row>
              <md-table-head></md-table-head>
              <md-table-head>Название</md-table-head>
              <md-table-head>Url</md-table-head>
              <md-table-head>Тип</md-table-head>
              <md-table-head>Авторизация</md-table-head>
              <md-table-head>Пользователь</md-table-head>
            </md-table-row>
            <md-table-row v-bind:key="tracker.id" v-for="tracker in trackers">
              <md-table-head>
                <div v-on:click="editTracker(tracker)" class="edit-icon">
                  <font-awesome-icon icon="edit"/>
                  <md-tooltip md-direction="top">Редактировать</md-tooltip>
                </div>
              </md-table-head>
              <md-table-head>{{tracker.title}}</md-table-head>
              <md-table-head>{{tracker.api_url}}</md-table-head>
              <md-table-head>{{tracker.type}}</md-table-head>
              <md-table-head>
                <a class="simple-link" @click="showTokenModal(tracker)">
                  <md-tooltip md-direction="top">Авторизация на трекере</md-tooltip>
                  <span v-if="tracker.external_api_key">{{tracker.external_api_key}}</span>
                  <span v-if="!tracker.external_api_key">Авторизоваться</span>
                </a>
              </md-table-head>
              <md-table-head>
                <a class="simple-link" v-if="tracker.external_api_key && tracker.type === 'evo'"
                 @click="showUserModal(tracker)">
                  <span v-if="!tracker.external_user_id && tracker.type === 'evo'">Указать пользователя</span>
                  <span v-if="tracker.external_user_id">{{tracker.external_user_id}}</span>
                </a>
                <span v-if="tracker.external_user_id && (tracker.type === 'redmine' || tracker.type === 'jira')">{{tracker.external_user_id}}</span>
              </md-table-head>
            </md-table-row>
          </md-table>

          <md-list-item>
            <md-button @click="addTracker('redmine')">Добавить redmine</md-button>
            <md-button @click="addTracker('jira')">Добавить JIRA</md-button>
          </md-list-item>
        </md-list>
      </div>

      <br><br>

      <div class="md-layout-item md-size-80" v-if="projects">
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
              <md-table-head>Авторизация</md-table-head>
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
    <br>
    <div class="md-layout md-gutter md-alignment-top-center center">
      <div class="md-layout-item md-size-80">
        <md-list>
          <md-list-item>
            <h3>Формат выгрузки часов в evolution</h3>
          </md-list-item>

          <md-list-item>
            <b>Есть задача в redmine</b>
            <md-field>
              <label>формулировка</label>
              <md-input v-model="userSettings.evo_in_name" required></md-input>
            </md-field>
            <md-field>
              <label>комментарий</label>
              <md-input v-model="userSettings.evo_in_comment"></md-input>
            </md-field>
          </md-list-item>

          <md-list-item>
            <b>Нет задачи в redmine</b>
            <md-field>
              <label>формулировка</label>
              <md-input v-model="userSettings.evo_out_name" required></md-input>
            </md-field>
            <md-field>
              <label>комментарий</label>
              <md-input v-model="userSettings.evo_out_comment"></md-input>
            </md-field>
          </md-list-item>

          <md-list-item>
            <b>Допустимые подстановки:</b><br>
            <br><i>#redmine_name</i> - название задачи из редмайн
            <br><i>#redmine_id</i> - номер задачи из редмайн
            <br><i>#name</i> - название задачи из трекера
            <br><i>#comments</i> - комментарии к задаче из трекера
          </md-list-item>

          <md-list-item>
            <md-button class="md-accent" @click="saveSettings()">Сохранить</md-button>
            <md-button @click="restoreSettings()">По умолчанию</md-button>
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
        <md-button class="md-accent" @click="getToken">отправить</md-button>
      </div>
    </modal>

    <modal :show="showUser">
      <div class="modal-header">
        <h2>Выберите пользователя в {{currentTracker.title}}</h2>
      </div>
      <div class="modal-body">
        <input type="hidden" v-model="currentTracker.id" name=id>
        <v-select v-model="evoUser" :options="evoUsers"/>
      </div>
      <div class="modal-footer text-right">
        <md-button class="md-primary" @click="closeUserModal">отмена</md-button>
        <md-button class="md-accent" @click="saveEvoUser">сохранить</md-button>
      </div>
    </modal>
    <md-dialog-alert :md-active.sync="showAlert" :md-content="alertMessage" md-confirm-text="Ок" />
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
      showToken: false,

      showAlert: false,
      alertMessage: '',

      userSettings: {
        evo_in_name: '#redmine_name',
        evo_in_comment: '#comments',
        evo_out_name: '#comments',
        evo_out_comment: ''
      }
    }
  },
  methods: {
    getTrackers () {
      API.getTrackers()
        .then(response => {
          this.trackers = response.data.trackers
        })
        .catch(error => {
          console.log(['getTasks error', error])
        })
    },
    getEvoUsers () {
      API.getEvoUsers()
        .then(response => {
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
          this.getTrackers()
          this.showUser = false
        })
        .catch(error => {
          console.log(['saveTrackerUser error', error])
        })
    },
    addTracker (type) {
      this.currentTracker = {
        id: 0,
        title: '',
        api_url: '',
        type: type
      }
      this.showTrackerModal()
    },
    editTracker (tracker) {
      this.currentTracker = tracker
      this.showTrackerModal()
    },
    getSettings () {
      API.getSettings()
        .then(response => {
          for (var key in response.data.data) {
            this.userSettings[key] = response.data.data[key]
          }
        })
        .catch(error => {
          console.log(['getSettings error', error])
        })
    },
    saveSettings () {
      if (this.userSettings.evo_in_name.trim() === '' || this.userSettings.evo_out_name.trim() === '') {
        this.alert('<span style="color: red;">Формулировка обязательна!</span>')
        return false
      }
      API.saveSettings(this.userSettings)
        .then(response => {
          this.alert('Изменения сохранены!')
        })
        .catch(error => {
          console.log(['saveSettings error', error])
          this.alert('Ошибка:' + error)
        })
    },
    restoreSettings () {
      this.userSettings = {
        evo_in_name: '#redmine_name',
        evo_in_comment: '#comments',
        evo_out_name: '#comments',
        evo_out_comment: ''
      }
    },
    showTokenModal (tracker) {
      this.loginToken = ''
      this.passwordToken = ''
      this.currentTracker = tracker
      this.showToken = true
    },
    showUserModal (tracker) {
      if (tracker.type !== 'evo') {
        return
      }
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
          if (response.data.external_token !== undefined && response.data.external_token !== null) {
            this.getTrackers()

            if (this.currentTracker.type === 'evo') {
              this.getEvoUsers()
            }

            this.showToken = false
          } else {
            this.alert('Ошибка авторизации')
          }
        })
        .catch(error => {
          console.log(['getToken error', error])
        })
    },
    alert (message) {
      this.alertMessage = message
      this.showAlert = true
    }
  },
  components: {
    Modal
  },
  mounted () {
    this.getTrackers()
    this.getEvoUsers()
    this.getSettings()
  }
}
</script>

<style scoped>
.simple-link, .edit-icon {
  cursor: pointer;
}
</style>
