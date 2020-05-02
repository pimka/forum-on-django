<template>
  <div>
    <h3>All Headings</h3>
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
      return formatter.format(dat)
    }
  }
};
</script>