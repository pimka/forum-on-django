<template>
  <div>
    <b-card-group flush>
      <b-card :header="item.parent">
        <b-card-text>{{ item.body }}</b-card-text>
        <template v-if="item.image">
          <b-img :src="server+item.image" alt="Image"></b-img>
        </template>
        <hr />
        <template v-if="item.file">
          <b-link :href="server+item.file">File</b-link>
          <hr />
        </template>
        <template v-if="isLoggedIn">
          <b-button v-on:click="visibleReply=true" variant="primary">Reply</b-button>
        </template>
        <template
          v-if="isLoggedIn & (this.$store.getters.userUUID==item.user_uuid || this.$store.getters.isStaff)"
        >
          <b-button v-on:click="visibleEdit=true" variant="primary">Edit</b-button>
          <b-button v-on:click="deleteData()" variant="danger">Delete</b-button>
        </template>
        <b-card-footer>
          <a>
            Creator: {{ author }}
            <br />
            Created {{ formatDate(item.created) }}
          </a>
        </b-card-footer>
      </b-card>

      <template v-if="visibleEdit">
        <b-card>
          <b-card-title>Edit message</b-card-title>
          <form>
            <b-form-group id="inputBodyGroup" label="Main text" label-for="inputBody">
              <b-form-input required id="inputBody" v-model="item.body" />
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
              <b-form-input id="inputBody" required v-model="new_item.body" />
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
            <b-button type="submit" variant="primary" v-on:click="replyData()">Save</b-button>
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
    },
    author: {
      type: String
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

  created() {
    this.getUsername();
  },

  methods: {
    editData() {
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
          this.$router.go()
        })
        .catch(err => {
          this.$bvToast.toast(err.message, {
            title: "Error",
            variant: "danger"
          });
        });
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
      let data = new FormData();
      data.append("body", this.new_item.body);
      data.append("user_uuid", this.$store.getters.userUUID);
      data.append("head_uuid", this.item.head_uuid);
      data.append("parent", this.item.uuid);
      if (this.new_item.file == null || this.new_item.file == undefined) {
        data.append("file", "");
      } else {
        data.append("file", this.new_item.file);
      }
      if (this.new_item.image == null || this.new_item.image == undefined) {
        data.append("image", "");
      } else {
        data.append("image", this.new_item.image);
      }
      Axios.post("http://localhost:8082/messages/", data, {
        headers: { Authorization: `Bearer ${this.$store.getters.getToken}` },
        "Content-Type": "multipart/form-data"
      })
        .then(() => {
          this.$bvToast.toast("Messages edited", {
            title: "Success",
            variant: "success"
          });
          this.$router.go()
        })
        .catch(err => {
          this.$bvToast.toast(err.message, {
            title: "Error",
            variant: "danger"
          });
        });
    },
    formatDate(date) {
      let dat = new Date(date);
      var formatter = new Intl.DateTimeFormat("en-gb", {
        weekday: "long",
        year: "numeric",
        month: "numeric",
        day: "numeric",
        hour: "numeric",
        minute: "numeric"
      });
      return formatter.format(dat);
    },
    getUsername() {
      var uuid = this.item.user_uuid;
      this.author = uuid;
      Axios.get(`http://localhost:8081/get_user/${uuid}/`, {
        headers: { Authorization: `Bearer ${this.$store.getters.getToken}` }
      }).then(response => {
        this.author = response.data.username;
      });
    }
  }
};
</script>