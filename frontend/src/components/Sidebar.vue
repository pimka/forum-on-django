<template>
  <div>
    <template v-if="isLoggedIn">
      <b-button v-b-toggle.sidebar-backdrop>Your Headings</b-button>
      <b-sidebar
        id="sidebar-backdrop"
        title="Headings"
        bg-variant="dark"
        text-variant="light"
        backdrop
        shadow
      >
        <div class="p-3">
          <router-link to="/new-heading/">Create Heading</router-link>
          <div v-for="head in heads" :key="head">
            <template v-if="head.user_uuid == userUUID">
              <router-link
                :to="{ name: 'concrete_heading', params: { head_uuid : head.uuid }}"
              >{{ head.header }}</router-link>
            </template>
          </div>
        </div>
      </b-sidebar>
    </template>
  </div>
</template>

<script>
import { HTTPHeading } from "../api/common";

export default {
  created() {
    this.getHeads();
  },

  computed: {
    isLoggedIn: function() {
      return this.$store.getters.isLoggedIn;
    },
    userUUID: function() {
      return this.$store.getters.userUUID
    }
  },

  data() {
    return {
      heads: []
    };
  },

  methods: {
    getHeads() {
      HTTPHeading.get("/headings/")
        .then(response => {
          this.heads = response.data;
        })
        .catch(err => {
          this.$bvToast.toast(err.message, {
            title: "Error",
            variant: "danger"
          });
        });
    }
  }
};
</script>