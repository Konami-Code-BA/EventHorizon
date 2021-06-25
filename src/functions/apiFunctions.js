import store from '@/store.js'
axios.defaults.withCredentials = true
axios.defaults.xsrfHeaderName = "X-CSRFToken"
    //let csrftoken = JSON.parse('{"' + document.cookie.replaceAll('=', '": "').replaceAll('; ', '", "') + '"}')['XSRF-TOKEN']
    //axios.defaults.headers.common['X-CSRFToken'] = csrftoken
import axios from 'axios'
export default {
    get ApiBaseUrl() { return process.env.NODE_ENV == 'development' ? 'http://127.0.0.1:8000' : '' },
    async userApiFunction(method, uri, data) {
        let output = store.defaultUser
        let axiosCall = {}
        axiosCall['post'] = axios.post
        axiosCall['patch'] = axios.patch
        await axiosCall[method](this.ApiBaseUrl + uri, data)
            .then(response => {
                console.log(`${data.command} SUCCESS:`, response.data)
                if (response.data !== '' && data.command !== 'logout') {
                    output = response.data
                }
            })
            .catch(error => {
                console.log(`${data.command} ERROR:`, error)
            })
            .finally(() => {
                store.user = output
            })
    },
    async authenticateFromSession() {
        await this.userApiFunction('post', '/api/user/', {
            command: 'authenticateFromSession',
        })
    },
    async register(username, email, password) {
        await this.userApiFunction('post', '/api/user/', {
            command: 'registration',
            username: username,
            email: email,
            password: password,
            language: store.user.language,
            groups: [2],
        })
    },
    async login(username, password) {
        await this.userApiFunction('post', '/api/user/', {
            command: 'login',
            username: username,
            password: password,
        })
    },
    async logout() {
        await this.userApiFunction('post', '/api/user/', {
            command: 'logout',
            username: store.user.username,
        })
    },
    async updateUserLanguage() {
        await this.userApiFunction('patch', '/api/user/' + store.user.id + '/', {
            command: 'updateUserLanguage',
            language: store.user.language,
        })
    },
    async updateUserGetEmails() {
        await this.userApiFunction('patch', '/api/user/' + store.user.id + '/', {
            command: 'updateUserGetEmails',
            getEmails: store.user.getEmails,
        })
    },
}