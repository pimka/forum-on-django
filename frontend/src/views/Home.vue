<template>
  <div class="home">
    <form>
      <TopHeads :items="items" v-if="items.length > 0"/>
      <div class="text-center" v-if="err === ''">
        <b-spinner/>
      </div>
      <div class="alert alert-danger" role="alert" v-if="err !== ''">{{ err }}</div>
    </form>
  </div>
</template>

<script>
// @ is an alias to /src
import { HTTP } from '../api/common'
import TopHeads from '../components/TopSearchHeadTable.vue'

export default {
  name: 'Home',
  components: {
    TopHeads
  },

  created () {
    this.getJSON()
  },

  data () {
    return {
      items: [],
      err: ''
    }
  },

  methods: {
    getJSON () {
      HTTP.get('/headings/').then(response => {
        this.items = response.data
        console.log(response.data)
      }).catch(err => { this.err = err.message })
      function compare (a, b) {
        if (a.views < b.views) {
          return -1;
        }
        if (a.views > b.views) {
          return 1;
        }
        return 0;
      }
      this.items.sort(compare)
      this.items = this.items.slice(10)
    }
  }
}
</script>
