<template>
  <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
    <router-link class="navbar-brand" to="/">Forum</router-link>
    <button
      class="navbar-toggler"
      type="button"
      data-toggle="collapse"
      data-target="#navbarSupportedContent"
      aria-controls="navbarSupportedContent"
      aria-expanded="false"
      aria-label="Toggle navigation"
    >
      <span class="navbar-toggler-icon"></span>
    </button>

    <div class="collapse navbar-collapse" id="navbarSupportedContent">
      <ul class="navbar-nav mr-auto">
        <template v-if="!isLoggedIn">
          <li class="nav-item">
            <router-link class="nav-link" to="/login/">Sign In</router-link>
          </li>
          <li class="nav-item">
            <router-link class="nav-link" to="/register/">Sign Up</router-link>
          </li>
        </template>
        <template v-if="isLoggedIn">
          <li class="nav-item" v-if="isLoggedIn">
            <a class="nav-link" href="#" @click="logout">Logout</a>
          </li>
        </template>
        <template v-if="isStaff">
          <li class="nav-item">
            <router-link class="nav-link" to="/tags/">Tags</router-link>
          </li>
        </template>
      </ul>
      <b-navbar-nav class="ml-auto">
        <b-nav-form>
          <b-form-tags
            size="sm"
            class="mr-sm-2"
            v-model="searchTags"
            :tag-validator="isValidate"
            placeholder="Search"
            separator=" "
          ></b-form-tags>
          <b-button size="sm" class="my-2 my-sm-0" type="submit" v-on:click="search()">Search</b-button>
        </b-nav-form>
      </b-navbar-nav>
    </div>
  </nav>
</template>


<script>
import Axios from "axios";
export default {
  computed: {
    isLoggedIn: function() {
      return this.$store.getters.isLoggedIn;
    },
    isStaff: function() {
      return this.$store.getters.isStaff;
    }
  },

  data() {
    return {
      tags: [],
      searchTags: []
    };
  },

  created() {
    this.getTags();
  },

  methods: {
    logout: function() {
      this.$store.dispatch("logout").then(() => {
        this.$router.push("/auth/");
      });
    },
    search() {
      var tags_uuid = []
      this.searchTags.forEach(tag => {
        this.tags.forEach(element => {
          if (String(element.name.toLowerCase()) == String(tag.toLowerCase())) {
            tags_uuid.push(element.uuid)
          }
        });
      });
      this.$router.push({ name: "search", query: { searchTags: tags_uuid } });
    },
    getTags() {
      Axios.get("http://localhost:8083/tags/", {
        headers: { Authorization: `Bearer ${this.$store.getters.getToken}` }
      })
        .then(response => {
          this.tags = response.data;
        })
        .catch(err => {
          this.$bvToast.toast(err.message, {
            title: "Error",
            variant: "danger"
          });
        });
    },
    isValidate(tag) {
      var flag = false;
      this.tags.forEach(element => {
        if (String(element.name.toLowerCase()) == String(tag.toLowerCase())) {
          flag = true;
        }
      });
      return flag;
    }
  }
};
</script>