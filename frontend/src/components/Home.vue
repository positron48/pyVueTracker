// Home.vue
<template>
  <div>

    <form action="" method=post class=add-entry>
      <input type=text size=50 name=name>
      <input type=submit value=Submit>
    </form>

    <Tasks/>
  </div>
</template>

<script>
import Tasks from './Tasks.vue'

export default {
  data () {
    return {
      randomNumber: 0
    }
  },
  components: {
    Tasks
  }
}
</script>
