import axios from 'axios'

const token = localStorage.getItem('token')
const keyword = 'Bearer '
export const HTTPUser = axios.create({
  baseURL: 'http://localhost:8081/',
  headers: {
    'Authorization': keyword + token
  }
})
export const HTTPAuth = axios.create({
  baseURL: 'http://localhost:8080/',
  headers: {
    'Authorization': keyword + token
  }
})
export const HTTPMessages = axios.create({
  baseURL: 'http://localhost:8082/',
  headers: {
    'Authorization': keyword + token
  }
})
export const HTTPHeading = axios.create({
  baseURL: 'http://localhost:8083/',
  headers: {
    'Authorization': keyword + token
  }
})