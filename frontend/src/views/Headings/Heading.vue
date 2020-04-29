<template>
  <div>
    <b-card-group flush>
      <b-card>
        <b-card-title>{{ heading.header }}</b-card-title>
        <b-card-text>{{ heading.body }}</b-card-text>
        <b-card-footer>Views: {{ heading.views }}</b-card-footer>
        <div v-for="tag in heading.tags" :key="tag">
          <b-badge>{{ tag }}</b-badge>
        </div>
        <b-button v-on:click="visibleAnswer=true" variant="primary">Answer</b-button>
        <b-button v-on:click="visibleEdit=true" variant="primary">Edit</b-button>
        <b-button v-on:click="deleteData()" variant="danger">Delete</b-button>
      </b-card>

      <template v-if="visibleEdit">
        <b-card>
          <b-card-title>Edit heading</b-card-title>
          <b-card-text>
            <b-form>
              <b-form-group id="inputHeadGroup" label="Title" label-for="inputHead">
                <b-form-input id="inputHead" v-model="heading.head" placeholder="Enter title" />
              </b-form-group>
              <b-form-group id="inputBodyGroup" label="Main Text" label-for="inputBody">
                <b-form-textarea id="inputBody" v-model="heading.body" rows="5" />
              </b-form-group>
              <b-form-group id="inputTagsGroup" label="Select Tags" label-for="inputTags">
                <b-form-select v-model="heading.tags" :options="tags" multiple id="inputTags" />
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
                <b-form-textarea id="inputBody" v-model="new_message.body" rows="5" />
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

  data() {
    return {
      head_uuid: this.$route.params.head_uuid,
      heading: {
        type: Object
      },
      messages: [],
      visibleEdit: false,
      visibleAnswer: false,
      tags: [],
      new_message: {
        type: Object
      }
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
          console.log(response.data);
          this.heading = response.data;
          this.getMessages();
        })
        .catch(err => {
          this.$bvToast.toast(err.message, {
            title: "Error",
            variant: "danger"
          });
        });
      this.getTags();
    },
    editData() {
      if (this.validData()) {
        this.visibleEdit = false;
        Axios.put(
          `http://localhost:8083/headings/${this.head_uuid}/`,
          this.heading,
          {
            headers: { Authorization: `Bearer ${this.$store.getters.getToken}` }
          }
        )
          .then(() => {
            this.$bvToast.toast("Heading edited", {
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
      if (this.heading.head.length == 0) {
        this.$bvToast.toast("Enter Title", {
          title: "Error",
          variant: "danger"
        });
      }
    },
    getMessages() {
      Axios.get(`http://localhost:8082/messages/`, {
        headers: { Authorization: `Bearer ${this.$store.getters.getToken}` }
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
          this.tags = response.data;
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