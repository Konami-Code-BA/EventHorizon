import store from '@/store.js'
axios.defaults.withCredentials = true
axios.defaults.xsrfHeaderName = "X-CSRFToken"
    //let csrftoken = JSON.parse('{"' + document.cookie.replaceAll('=', '": "').replaceAll('; ', '", "') + '"}')['XSRF-TOKEN']
    //axios.defaults.headers.common['X-CSRFToken'] = csrftoken
import axios from 'axios'
export default {
    get ApiBaseUrl() { return process.env.NODE_ENV == 'development' ? 'http://127.0.0.1:8000' : '' },
    axiosCall: {
        post: axios.post,
        patch: axios.patch,
        get: axios.get,
    },
    async userApiFunction(method, uri, data) {
        let output = store.defaultUser
        await this.axiosCall[method](this.ApiBaseUrl + uri, data)
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
    async lineApiFunction(method, uri, data) {
        let output = null
        await this.axiosCall[method](this.ApiBaseUrl + uri, data)
            .then(response => {
                console.log(`${data.command} SUCCESS:`, response.data)
                if (response.data !== '') {
                    output = response.data
                }
            })
            .catch(error => {
                console.log(`${data.command} ERROR:`, error)
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
    async sendEmail() {
        await this.userApiFunction('post', '/api/user/', {
            command: 'sendEmail',
        })
    },
    async sendWebhook() {
        await this.lineApiFunction('post', '/webhook/', {
            command: 'sendWebhook',
        })
    },
    async lineConsumption() {
        await this.lineApiFunction('post', '/api/line/', {
            command: 'consumption',
        })
    },
    async linePush() {
        await this.lineApiFunction('post', '/api/line/', {
            command: 'push',
            message: 'sup this is a push message',
            to: 'U09e3b108910c1711d2732a8b9ac8a19d',
        })
    },
    async lineBroadcast() {
        await this.lineApiFunction('post', '/api/line/', {
            command: 'broadcast',
            message: 'sup this is a broadcast message',
            to: 'U09e3b108910c1711d2732a8b9ac8a19d',
        })
    },
}