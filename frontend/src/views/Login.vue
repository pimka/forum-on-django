<template>
  <div>
    <b-form>
      <h3>Sign In</h3>
      <b-form-group id="inputUsernameGroup" label="Username" label-for="inputUsername">
        <b-form-input id="inputUsername" v-model="username" placeholder="Enter your name" />
      </b-form-group>
      <b-form-group id="inputPasswordGroup" label="Password" label-for="inputPassword">
        <b-form-input
          id="inputPassword"
          v-model="password"
          type="password"
          placeholder="Enter your password"
        />
      </b-form-group>
      <b-button type="submit" variant="primary" v-on:click="login()">Sign In</b-button>
    </b-form>
  </div>
</template>

<script>
export default {
  data() {
    return {
      username: null,
      password: null,
      isSuccess: false
    };
  },

  methods: {
    login: function() {
      let username = this.username;
      let password = this.password;
      this.$store
        .dispatch("login", { username, password })
        .then(() => {
          this.$bvToast.toast("Login", {
            title: "Success",
            variant: "success"
          });
          this.$router.push("/");
        })
        .catch(error => {
          this.$bvToast.toast(error.message, {
            title: "Error",
            variant: "danger"
          });
        });
    }
  }
};
</script>