<template>
  <div>
    <b-form>
      <h3>Create Heading</h3>
      <b-form-group id="inputHeadGroup" label="Title" label-for="inputHead">
        <b-form-input id="inputHead" required v-model="head" placeholder="Enter title" />
      </b-form-group>
      <b-form-group id="inputBodyGroup" label="Main Text" label-for="inputBody">
        <b-form-textarea id="inputBody" required v-model="body" rows="5" />
      </b-form-group>
      <b-form-group id="inputTagsGroup" label="Select Tags" label-for="inputTags">
        <b-form-select v-model="selected" :options="tags" multiple id="inputTags" />
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
      head: "",
      body: "",
      selected: null,
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
          "http://localhost:8083/headings_add/",
          {
            header: this.head,
            body: this.body,
            user_uuid: this.$store.getters.userUUID,
            tags: this.selected
          },
          {
            headers: {
              Authorization: `Bearer ${this.$store.getters.getToken}`
            }
          }
        )
          .then(response => {
            this.items = response.data;
            this.err = "";
            this.$bvToast.toast("Heading created", {
              title: "Success",
              variant: "success"
            });
            this.$router.push("/");
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
      if (this.selected.length == 0) {
        this.$bvToast.toast("Select tag", {
          title: "Error",
          variant: "danger"
        });
        return false;
      }
      return true;
    },
    getJSON() {
      Axios.get("http://localhost:8083/tags/", {
        headers: { Authorization: `Bearer ${this.$store.getters.getToken}` }
      })
        .then(response => {
          for (let index = 0; index < response.data.length; index++) {
            const element = response.data[index];
            this.tags.push({ value: element.uuid, text: element.name });
          }
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