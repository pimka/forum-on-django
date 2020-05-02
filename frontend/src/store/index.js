import Vue from 'vue'
import Vuex from 'vuex'
import axios from 'axios'
import Axios from 'axios'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    status: '',
    token: localStorage.getItem('token') || '',
    user: {},
    refresh_token: localStorage.getItem('refresh_token') || '',
    token_type: '',
    access_token: localStorage.getItem('access_token') || '',
    user_uuid: localStorage.getItem('uuid') || '',
    is_staff: localStorage.getItem('is_staff') || false,
  },
  mutations: {
    auth_request(state) {
      state.status = 'loading'
    },
    auth_success(state, payload) {
      state.status = 'success'
      state.token = payload.token
      state.user = payload.user
      state.user_uuid = payload.uuid
      state.is_staff = payload.is_staff
    },
    auth_error(state) {
      state.status = 'error'
    },
    logout(state) {
      state.status = ''
      state.token = ''
      state.access_token = ''
      state.token_type = ''
      state.refresh_token = ''
      state.user_uuid = ''
      state.is_staff = false
    },
    oauth_success(state, payload) {
      state.status = 'success'
      state.access_token = payload.a_token
      state.token_type = payload.type
      state.refresh_token = payload.r_token
    }
  },
  actions: {
    login({ commit }, user) {
      return new Promise((resolve, reject) => {
        commit('auth_request')
        Axios.post('http://localhost:8080/user/login/', user)
          .then(resp => {
            const token = resp.data.token
            const user = resp.data.user
            const uuid = resp.data.uuid
            const is_staff = resp.data.is_staff
            localStorage.setItem('token', token)
            localStorage.setItem('uuid', uuid)
            localStorage.setItem('is_staff', is_staff)
            axios.defaults.headers.common['Authorization'] = token
            commit('auth_success', {'token':token, 'user':user, 'uuid':uuid, 'is_staff':is_staff})
            resolve(resp)
            console.log('success')
          })
          .catch(err => {
            commit('auth_error')
            localStorage.removeItem('token')
            console.log('auth_with_errors')
            console.log(err)
            reject(err)
          })
      })
    },
    oauth_login({ commit }, data) {
      const Atoken = data.access_token
      const Ttype = data.token_type
      const Rtoken = data.refresh_token
      const tokens = { 'a_token': Atoken, 't_type': Ttype, 'r_token': Rtoken }
      localStorage.setItem('access_token', Atoken)
      commit('oauth_success', tokens)
      axios.defaults.headers.common['Authorization'] = Ttype + ' ' + Atoken
    },
    logout({ commit }) {
      return new Promise((resolve, reject) => {
        try {
          commit('logout')
          localStorage.removeItem('token')
          localStorage.removeItem('uuid')
          localStorage.removeItem('is_staff')
          localStorage.removeItem('access_token')
          delete axios.defaults.headers.common['Authorization']
          resolve()
        }
        catch (err) {
          reject(err)
        }
      })
    }
  },
  modules: {
  },
  getters: {
    isLoggedIn: state => !!state.token || !!state.access_token,
    authStatus: state => state.status,
    userUUID: state => state.user_uuid,
    isStaff: state => state.is_staff,
    getToken: state => state.token
  }
})
