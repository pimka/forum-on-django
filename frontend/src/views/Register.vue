<template>
    <div>
        <form>
            <h3>Sign Up</h3>
            <b-form-group id="inputUsernameGroup" label="Username" label-for="inputUsername">
                <b-form-input id="inputUsername" v-model="username" placeholder="Enter your name"/>
            </b-form-group>
            <b-form-group id="inputPasswordGroup" label="Password" label-for="inputPassword">
                <b-form-input id="inputPassword" v-model="password" type="password" placeholder="Enter your password"/>
            </b-form-group>
            <b-button type="submit" variant="primary" v-on:click="register()">Create Account</b-button>
        </form>
    </div>
</template>

<script>
import { HTTPUser } from '../api/common'

export default {
    data () {
        return {
            username: null,
            password: null,
            isSuccess: false
        }
    },

    methods: {
        login: function () {
            let username = this.username
            let password = this.password
            this.$store.dispatch('login', { username, password })
                .then(() => {
                    this.$bvToast.toast('Login', {
                        title: 'Success',
                        variant: 'success'
                    })
                })
                .catch(error => { 
                    this.$bvToast.toast(error.message, {
                        title: 'Error',
                        variant: 'danger'
                    })
                })
        },
        register: function () {
            HTTPUser.post('/user/', {
                'username': this.username,
                'password': this.password
            }).then(response => {
                this.items = response.data
                this.isSuccess = true
                this.$bvToast.toast('Account created', {
                    title: 'Success',
                    variant: 'success'
                })
                this.login()
            }).catch(err => {
                this.$bvToast.toast(err.message, {
                    title: 'Error',
                    variant: 'danger'
                })
            })
        }
    }
}
</script>