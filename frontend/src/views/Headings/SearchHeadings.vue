<template>
  <div>
    <h3>Search results</h3>
    <b-table id="headsTable" :fields="fields" :items="items" head-variant="light" :striped="true">
      <template v-slot:cell(header)="{value, item}">
        <router-link :to="{name:'concrete_heading', params:{head_uuid:item.uuid}}">{{item.header}}</router-link>
      </template>
      <template v-slot:cell(created)="{value, item}">
        <time>{{formatDate(item.created)}}</time>
      </template>
    </b-table>
  </div>
</template>

<script>
import { HTTPHeading } from '../../api/common';
export default {
  data() {
    return {
      fields: [
        { key: "header", label: "Heading" },
        { key: "views", label: "Views" },
        { key: "created", label: "Created" }
      ]
    };
  },
  props: {
    items: {
      type: Array
    }
  },
watch: {
  $route: function() {
    this.getData(this.$route.query.searchTags)
  }},
  created() {
    this.getData(this.$route.query.searchTags);
  },

  methods: {
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
    getData(tags) {
      HTTPHeading.get("/headings/", { params: { search: tags } })
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