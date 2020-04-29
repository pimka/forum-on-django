<template>
  <div class="home">
    <TopHeads :items="items" v-if="items.length > 0" />
    <div class="text-center" v-if="err === ''">
      <b-spinner />
    </div>
  </div>
</template>

<script>
// @ is an alias to /src
import { HTTPHeading } from "../api/common";
import TopHeads from "../components/TopSearchHeadTable.vue";

export default {
  name: "Home",
  components: {
    TopHeads
  },

  created() {
    this.getJSON();
  },

  data() {
    return {
      items: [],
      err: ""
    };
  },

  methods: {
    getJSON() {
      HTTPHeading.get("/headings/")
        .then(response => {
          this.items = response.data;
        })
        .catch(err => {
          this.err = err.message;
          this.$bvToast.toast(err.message, {
            title: "Error",
            variant: "danger"
          });
        });
      function compare(a, b) {
        if (a.views < b.views) {
          return -1;
        }
        if (a.views > b.views) {
          return 1;
        }
        return 0;
      }
      this.items.sort(compare);
      this.items = this.items.slice(10);
    }
  }
};
</script>
