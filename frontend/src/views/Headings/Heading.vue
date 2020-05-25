<template>
  <div>
    <b-card-group flush>
      <b-card>
        <b-card-title>{{ heading.header }}</b-card-title>
        <b-card-text>{{ heading.body }}</b-card-text>
        <template>
          <b-badge v-for="tag in head_tags" :key="tag">{{ tag }}</b-badge>
        </template>
        <br />
        <template v-if="isLoggedIn">
          <b-button v-on:click="visibleAnswer=true" variant="primary">Answer</b-button>
        </template>
        <template
          v-if="isLoggedIn & (this.$store.getters.userUUID==heading.user_uuid || this.$store.getters.isStaff)"
        >
          <b-button v-on:click="visibleEdit=true" variant="primary">Edit</b-button>
          <b-button v-on:click="deleteData()" variant="danger">Delete</b-button>
        </template>
        <b-card-footer>
          <a>
            Views: {{ heading.views }}
            <br />
            Creator: {{ author }}
            <br />
            Created: {{ formatDate(heading.created) }}
          </a>
        </b-card-footer>
      </b-card>

      <template v-if="visibleEdit">
        <b-card>
          <b-card-title>Edit heading</b-card-title>
          <b-card-text>
            <b-form>
              <b-form-group id="inputHeadGroup" label="Title" label-for="inputHead">
                <b-form-input
                  id="inputHead"
                  v-model="new_heading.header"
                  placeholder="Enter title"
                  required
                />
              </b-form-group>
              <b-form-group id="inputBodyGroup" label="Main Text" label-for="inputBody">
                <b-form-textarea id="inputBody" required v-model="new_heading.body" rows="5" />
              </b-form-group>
              <b-form-group id="inputTagsGroup" label="Select Tags" label-for="inputTags">
                <b-form-select v-model="new_tags" :options="tags" multiple id="inputTags" />
              </b-form-group>
              <b-button type="submit" variant="primary" v-on:click="editData()">Save</b-button>
            </b-form>
          </b-card-text>
        </b-card>
      </template>

      <template v-if="visibleAnswer">
        <b-card>
          <b-card-title>Create message</b-card-title>
          <b-card-text>
            <b-form>
              <b-form-group id="inputBodyGroup" label="Main text" label-for="inputBody">
                <b-form-textarea id="inputBody" required v-model="new_message.body" rows="5" />
              </b-form-group>
              <b-form-group id="inputFileGroup" label="File" label-for="inputFile">
                <b-form-file
                  id="inputFile"
                  v-model="new_message.file"
                  placeholder="Choose a file or drop it here..."
                />
              </b-form-group>
              <b-form-group id="inputImageGroup" label="Image" label-for="inputImage">
                <b-form-file
                  id="inputImage"
                  v-model="new_message.image"
                  placeholder="Choose a image or drop it here..."
                  accept="image/*"
                />
              </b-form-group>
              <b-button type="submit" variant="primary" v-on:click="createMessage()">Save</b-button>
            </b-form>
          </b-card-text>
        </b-card>
      </template>
    </b-card-group>
    <div v-for="mes in messages" :key="mes">
      <Messages :item="mes" />
    </div>
  </div>
</template>

<script>
import Messages from "../../components/Messages.vue";
import Axios from "axios";

export default {
  name: "Heading",
  components: {
    Messages
  },

  computed: {
    isLoggedIn: function() {
      return this.$store.getters.isLoggedIn;
    }
  },
  watch: {
    $route: function() {
      this.getData();
    }
  },

  props: {
    heading: {
      type: Object
    },
    visibleEdit: {
      type: Boolean,
      default: false
    },
    visibleAnswer: {
      type: Boolean,
      default: false
    },
    messages: {
      type: Array
    },
    author: {
      type: String
    },
    head_tags: {
      type: Array
    }
  },

  data() {
    return {
      head_uuid: this.$route.params.head_uuid,
      tags: [],
      new_message: {
        type: Object
      },
      new_heading: {
        type: Object,
        default: this.heading
      },
      new_tags: null
    };
  },

  created() {
    this.getData();
  },

  methods: {
    getData() {
      Axios.get(`http://localhost:8083/heading/${this.head_uuid}/`, {
        headers: { Authorization: `Bearer ${this.$store.getters.getToken}` }
      })
        .then(response => {
          this.heading = response.data;
          this.getUsername(response.data.user_uuid);
          this.getMessages();
          this.getTags();
          this.getTagsNames(response.data.tags);
        })
        .catch(err => {
          this.$bvToast.toast(err.message, {
            title: "Error",
            variant: "danger"
          });
        });
    },
    editData() {
      if (this.validData()) {
        this.new_heading.tags = this.new_tags;
        this.new_heading.user_uuid = this.heading.user_uuid;
        this.visibleEdit = false;
        Axios.patch(
          `http://localhost:8083/headings/${this.head_uuid}/`,
          this.new_heading,
          {
            headers: { Authorization: `Bearer ${this.$store.getters.getToken}` }
          }
        )
          .then(() => {
            this.$bvToast.toast("Heading edited", {
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
      }
    },
    deleteData() {
      Axios.delete(`http://localhost:8083/headings/${this.head_uuid}/`, {
        headers: { Authorization: `Bearer ${this.$store.getters.getToken}` }
      })
        .then(() => {
          this.$bvToast.toast("Heading deleted", {
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
    },
    validData() {
      if (this.new_tags.length == 0) {
        this.$bvToast.toast("Select tag", {
          title: "Error",
          variant: "danger"
        });
        return false;
      }
      return true;
    },
    getMessages() {
      Axios.get(`http://localhost:8082/messages/`, {
        headers: { Authorization: `Bearer ${this.$store.getters.getToken}` },
        params: { heading: this.$route.params.head_uuid }
      })
        .then(response => {
          this.messages = response.data;
        })
        .catch(err => {
          this.$bvToast.toast(err.message, {
            title: "Error",
            variant: "danger"
          });
        });
    },
    getTags() {
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
    },
    createMessage() {
      let data = new FormData();
      data.append("body", this.new_message.body);
      data.append("user_uuid", this.$store.getters.userUUID);
      data.append("head_uuid", this.head_uuid);
      data.append("file", this.new_message.file);
      data.append("image", this.new_message.image);
      Axios.post("http://localhost:8082/messages/", data, {
        headers: {
          Authorization: `Bearer ${this.$store.getters.getToken}`,
          "Content-Type": "multipart/form-data"
        }
      })
        .then(() => {
          this.$bvToast.toast("Message created", {
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
    getUsername(uuid) {
      this.author = uuid;
      Axios.get(`http://localhost:8081/get_user/${uuid}/`, {
        headers: { Authorization: `Bearer ${this.$store.getters.getToken}` }
      }).then(response => {
        this.author = response.data.username;
      });
    },
    getTagsNames(uuids) {
      this.head_tags = [];
      uuids.forEach(element => {
        Axios.get(`http://localhost:8083/get_tags/${element}/`, {
          headers: { Authorization: `Bearer ${this.$store.getters.getToken}` }
        }).then(response => {
          this.head_tags.push(response.data.name);
        });
      });
    }
  }
};
</script>