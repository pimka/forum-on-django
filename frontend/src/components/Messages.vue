<template>
  <div>
    <b-card-group flush>
      <b-card
        :header="item.parent"
        :footer="[item.created, item.user_uuid]"
        :img-scr="item.image"
      >
        <b-card-text>{{ item.body }}</b-card-text>
        <b-card-text>{{ item.file }}</b-card-text>
        <template v-if="isLoggedIn">
          <b-button v-on:click="visibleEdit=true" variant="primary">Edit</b-button>
          <b-button v-on:click="deleteData()" variant="danger">Delete</b-button>
          <b-button v-on:click="visibleReply=true" variant="danger">Reply</b-button>
        </template>
      </b-card>

      <template v-if="visibleEdit">
        <b-card>
          <b-card-title>Edit message</b-card-title>
          <form>
            <b-form-group id="inputBodyGroup" label="Main text" label-for="inputBody">
              <b-form-input id="inputBody" v-model="item.body" />
            </b-form-group>
            <b-form-group id="inputFileGroup" label="File" label-for="inputFile">
              <b-form-file
                id="inputFile"
                v-model="item.file"
                placeholder="Choose a file or drop it here..."
              />
            </b-form-group>
            <b-form-group id="inputImageGroup" label="Image" label-for="inputImage">
              <b-form-file
                id="inputImage"
                v-model="item.image"
                placeholder="Choose a image or drop it here..."
              />
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
import { HTTPMessages } from "../api/common";

export default {
  props: {
    item: {
      type: Object
    }
  },

  computed: {
    isLoggedIn: function() {
      return this.$store.getters.isLoggedIn;
    }
  },

  data() {
    return {
      visibleEdit: false,
      visibleReply: false,
      new_item: {
        type: Object
      }
    };
  },

  methods: {
    editData() {
      if (this.validData()) {
        this.visibleEdit = false;
        HTTPMessages.put(`/messages/${this.item.uuid}/`, this.item)
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
      HTTPMessages.delete(`/messages/${this.item.uuid}/`)
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
        HTTPMessages.post("/messages/", this.new_item)
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