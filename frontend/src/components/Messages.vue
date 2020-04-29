<template>
  <div>
    <b-card-group flush>
      <b-card :header="item.parent" :footer="[item.created, item.user_uuid]">
        <b-card-text>{{ item.body }}</b-card-text>
        <b-img :src="server+item.image" alt="Image"></b-img>
        <hr />
        <b-link :href="server+item.file">File</b-link>
        <hr />
        <template v-if="isLoggedIn">
          <b-button v-on:click="visibleReply=true" variant="primary">Reply</b-button>
        </template>
        <template v-if="isLoggedIn & this.$store.getters.userUUID==item.user_uuid">
          <b-button v-on:click="visibleEdit=true" variant="primary">Edit</b-button>
          <b-button v-on:click="deleteData()" variant="danger">Delete</b-button>
        </template>
      </b-card>

      <template v-if="visibleEdit">
        <b-card>
          <b-card-title>Edit message</b-card-title>
          <form>
            <b-form-group id="inputBodyGroup" label="Main text" label-for="inputBody">
              <b-form-input id="inputBody" v-model="item.body" />
            </b-form-group>
            <b-button type="submit" variant="primary" v-on:click="editData()">Save</b-button>
          </form>
        </b-card>
      </template>

      <template v-if="visibleReply">
        <b-card>
          <b-card-title>Reply</b-card-title>
          <form>
            <b-form-group id="inputBodyGroup" label="Main text" label-for="inputBody">
              <b-form-input id="inputBody" v-model="new_item.body" />
            </b-form-group>
            <b-form-group id="inputFileGroup" label="File" label-for="inputFile">
              <b-form-file
                id="inputFile"
                v-model="new_item.file"
                placeholder="Choose a file or drop it here..."
              />
            </b-form-group>
            <b-form-group id="inputImageGroup" label="Image" label-for="inputImage">
              <b-form-file
                id="inputImage"
                v-model="new_item.image"
                placeholder="Choose a image or drop it here..."
              />
            </b-form-group>
            <b-button type="submit" variant="primary" v-on:click="editData()">Save</b-button>
          </form>
        </b-card>
      </template>
    </b-card-group>
  </div>
</template>

<script>
import Axios from "axios";

export default {
  props: {
    item: {
      type: Object
    },
    visibleEdit: {
      type: Boolean,
      default: false
    },
    visibleReply: {
      type: Boolean,
      default: false
    },
    server: {
      type: String,
      default: "http://localhost:8082"
    }
  },

  computed: {
    isLoggedIn: function() {
      return this.$store.getters.isLoggedIn;
    }
  },

  data() {
    return {
      new_item: {
        type: Object
      }
    };
  },

  methods: {
    editData() {
      if (this.validData()) {
        this.visibleEdit = false;
        var temp = this.item;
        delete temp.file;
        delete temp.image;
        Axios.patch(`http://localhost:8082/messages/${this.item.uuid}/`, temp, {
          headers: { Authorization: `Bearer ${this.$store.getters.getToken}` }
        })
          .then(() => {
            this.$bvToast.toast("Messages edited", {
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
    deleteData() {
      Axios.delete(`http://localhost:8082/messages/${this.item.uuid}/`, {
        headers: { Authorization: `Bearer ${this.$store.getters.getToken}` }
      })
        .then(() => {
          this.$bvToast.toast("Message deleted", {
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
    },
    replyData() {
      this.visibleReply = false;
      this.new_item.parent = this.item.uuid;
      if (this.validData()) {
        Axios.post("http://localhost:8082/messages/", this.new_item, {
          headers: { Authorization: `Bearer ${this.$store.getters.getToken}` }
        })
          .then(() => {
            this.$bvToast.toast("Messages edited", {
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
      return true;
    }
  }
};
</script>