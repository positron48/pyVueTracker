// Home.vue
<template>
  <div>

    <form action="" method="post" class="md-layout md-gutter md-alignment-top-center">
      <md-card class="md-layout-item md-size-50 md-small-size-100">
        <md-card-content>
          <div class="md-layout md-gutter">
            <div class="md-layout-item md-size-80">
              <md-field>
                <label>Task</label>
                <md-input v-model="taskName"></md-input>
              </md-field>
            </div>

            <div class="md-layout-item md-size-20">
              <md-button type="submit" class="md-primary" style="margin-top: 18px;">Add</md-button>
            </div>
          </div>
        </md-card-content>
      </md-card>
    </form>

    <Tasks/>
  </div>
</template>

<script>
import Tasks from './Tasks.vue'

export default {
  data () {
    return {
      taskName: ''
    }
  },
  components: {
    Tasks
  }
}
</script>
