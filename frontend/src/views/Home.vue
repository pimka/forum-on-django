<template>
  <div class="home">
    <TopHeads :items="items" v-if="items.length > 0" />
    <b-pagination-nav :link-gen="linkGen" :number-of-pages="pagesCount" use-router></b-pagination-nav>
    <AllHeads :items="allItems" v-if="allItems.length > 0" />
    <div class="text-center" v-if="err === '' & items.length == 0">
      <b-spinner />
    </div>
  </div>
</template>

<script>
// @ is an alias to /src
import { HTTPHeading } from "../api/common";
import TopHeads from "../components/TopSearchHeadTable.vue";
import AllHeads from "../components/AllHeads.vue";

export default {
  name: "Home",
  components: {
    TopHeads,
    AllHeads
  },

  created() {
    this.getTop();
    this.getAll();
  },

  props: {
    items: {
      type: Array
    },
    allItems: {
      type: Array
    },
    pagesCount: {
      type: typeof 25
    }
  },

  data() {
    return {
      err: ""
    };
  },

  methods: {
    linkGen(pageNum) {
      HTTPHeading.get(`/headings/${pageNum === 1 ? "?" : `?page=${pageNum}`}`, {
        params: { paginate: true }
      })
        .then(response => {
          this.allItems = response.data.results;
        })
        .catch(err => {
          this.err = err.message;
          this.$bvToast.toast(err.message, {
            title: "Error",
            variant: "danger"
          });
        });
    },
    getAll() {
      HTTPHeading.get("/headings/", { params: { paginate: true } })
        .then(response => {
          this.allItems = response.data.results;
          this.pagesCount = response.data.count / 20 + 1;
        })
        .catch(err => {
          this.err = err.message;
          this.$bvToast.toast(err.message, {
            title: "Error",
            variant: "danger"
          });
        });
    },
    getTop() {
      HTTPHeading.get("/headings/", { params: { top: true } })
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
    }
  }
};
</script>
