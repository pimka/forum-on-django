<template>
  <div>
    <b-form>
      <h3>Create Tag</h3>
      <b-badge v-for="tag in tags" :key="tag">{{ tag.name }}</b-badge>
      <b-form-group id="inputNameGroup" label="Tag name" label-for="inputName">
        <b-form-input id="inputName" v-model="name" placeholder="Enter tag name" />
      </b-form-group>
      <b-button type="submit" variant="primary" v-on:click="sendData()">Create</b-button>
    </b-form>
  </div>
</template>

<script>
import Axios from "axios";

export default {
  data() {
    return {
      name: "",
      tags: []
    };
  },

  created() {
    this.getJSON();
  },

  methods: {
    sendData() {
      if (this.validData()) {
        Axios.post(
          "http://localhost:8083/tags_add/",
          {
            name: this.name
          },
          {
            headers: { Authorization: `Bearer ${this.$store.getters.getToken}` }
          }
        )
          .then(() => {
            this.$bvToast.toast("Tag created", {
              title: "Success",
              variant: "success"
            });
          })
          .catch(err => {
            this.$bvToast.toast(err.message, {
              title: "Error",
              variant: "danger"
            });
          });
      }
    },
    validData() {
      for (let index = 0; index < this.tags.length; index++) {
        const element = this.tags[index];
        if (element.name == this.name) {
          this.$bvToast.toast("Tag exist", {
            title: "Error",
            variant: "danger"
          });
          return false;
        }
      }
        return true;
    },
    getJSON() {
      Axios.get("http://localhost:8083/tags/", {
        headers: { Authorization: `Bearer ${this.$store.getters.getToken}` }
      })
        .then(response => {
          this.tags = response.data
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